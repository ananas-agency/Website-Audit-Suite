"""All network I/O of the security step: page fetches, file probes, TLS inspection and DNS TXT lookups.

Passive only. Standard library only. Every HTTP request sends the step's User-Agent. Nothing here follows a
redirect, and the contents of an exposed file are never read, stored or printed: `probe` records only the
status, content type and length.
"""
from __future__ import annotations

import datetime as dt
import http.client
import os
import socket
import ssl
import struct
import threading
import time
import warnings
from dataclasses import dataclass
from typing import List, Optional, Tuple
from urllib.parse import urlsplit

from . import USER_AGENT
from .checks import Response

MAX_BODY = 262144
DEFAULT_TIMEOUT = 10.0
DNS_TIMEOUT = 3.0


@dataclass
class ProbeResult:
    status: int
    content_type: Optional[str]
    length: Optional[int]


@dataclass
class TlsInfo:
    version: Optional[str]
    not_after: Optional[dt.datetime]
    issuer: Optional[str]
    error: Optional[str]            # None, "expired", "name-mismatch", "untrusted" or "unreachable"
    old_protocols: Optional[List[str]]   # "TLSv1"/"TLSv1.1" accepted; None when OpenSSL can't try them
    not_before: Optional[dt.datetime] = None


# ---------------------------------------------------------------- HTTP

class _Budget:
    """One overall deadline for a request. A timer shuts down every tracked socket when it passes, which
    wakes any blocked connect, handshake, status-line, header or body read (per-operation timeouts alone
    restart on every byte a slow server sends)."""

    def __init__(self, seconds: float) -> None:
        self.end = time.monotonic() + seconds
        self.expired = False
        self._socks: list = []
        self._lock = threading.Lock()
        self._timer = threading.Timer(max(seconds, 0.0), self._fire)
        self._timer.daemon = True
        self._timer.start()

    def left(self) -> float:
        return self.end - time.monotonic()

    def track(self, sock) -> None:
        with self._lock:
            self._socks.append(sock)
            if self.expired:
                self._kill(sock)

    @staticmethod
    def _kill(sock) -> None:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except (OSError, ValueError):
            pass

    def _fire(self) -> None:
        with self._lock:
            self.expired = True
            for sock in self._socks:
                self._kill(sock)

    def done(self) -> None:
        self._timer.cancel()
        with self._lock:
            socks, self._socks = self._socks, []
        for sock in socks:
            try:
                sock.close()
            except OSError:
                pass


def _secure_socket(host: str, port: int, ctx, budget: "_Budget"):
    """Connect (and, with a context, TLS-handshake) inside the budget. The caller closes via budget.done()."""
    left = budget.left()
    if left <= 0:
        raise TimeoutError("deadline passed")
    sock = socket.create_connection((host, port), timeout=left)
    budget.track(sock)
    if ctx is None:
        return sock
    sock.settimeout(max(budget.left(), 0.001))
    tls = ctx.wrap_socket(sock, server_hostname=host)
    budget.track(tls)
    return tls


def _open(url: str, method: str, budget: "_Budget", extra=None):
    """Return (connection, response) or raise; every socket is tracked by `budget`."""
    parts = urlsplit(url)
    host = parts.hostname or ""
    https = parts.scheme.lower() == "https"
    port = parts.port or (443 if https else 80)
    target = parts.path or "/"
    if parts.query:
        target += "?" + parts.query
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    headers.update(extra or {})
    ctx = ssl.create_default_context() if https else None
    try:
        sock = _secure_socket(host, port, ctx, budget)
    except ssl.SSLCertVerificationError:
        # The page is still public; tls_info reports the certificate problem. Read it without verifying.
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = _secure_socket(host, port, ctx, budget)
    cls = http.client.HTTPSConnection if https else http.client.HTTPConnection
    conn = cls(host, parts.port, timeout=max(budget.left(), 0.001))
    conn.sock = sock
    sock.settimeout(max(budget.left(), 0.001))
    conn.request(method, target, headers=headers)
    return conn, conn.getresponse()


def _close(conn, resp) -> None:
    for obj in (resp, conn):
        try:
            if obj is not None:
                obj.close()
        except OSError:
            pass


def get(url: str, timeout: float = DEFAULT_TIMEOUT) -> Optional[Response]:
    """One GET. No redirects are followed; at most 262144 bytes of body are read. None on any failure.

    `timeout` is one overall deadline for the whole request (connect, TLS, status line, headers, body).
    If it passes at any point the page is incomplete and None is returned."""
    budget = _Budget(timeout)
    conn = resp = None
    try:
        conn, resp = _open(url, "GET", budget)
        chunks, size = [], 0
        while size < MAX_BODY:
            if budget.left() <= 0:
                return None
            chunk = resp.read1(min(8192, MAX_BODY - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
        if budget.expired:   # a socket shut down by the timer can look like a normal end of data
            return None
        body = b"".join(chunks)
        return Response(url, resp.status, list(resp.getheaders()), body.decode("utf-8", "replace"))
    except (OSError, http.client.HTTPException, ValueError):
        return None
    finally:
        _close(conn, resp)
        budget.done()


def _digits(text: Optional[str]) -> Optional[int]:
    text = (text or "").strip()
    return int(text) if text.isascii() and text.isdigit() else None


def _length(resp, status: int) -> Optional[int]:
    cr = resp.getheader("Content-Range")
    if cr and "/" in cr and cr.lower().startswith("bytes") and "-" in cr.split("/")[0]:
        total = _digits(cr.rsplit("/", 1)[1])
        if total is not None:
            return total
    if status != 206:
        return _digits(resp.getheader("Content-Length"))
    return None


def probe(url: str, timeout: float = DEFAULT_TIMEOUT) -> Optional[ProbeResult]:
    """HEAD the URL; on 405/501 GET one byte (Range: bytes=0-0). Records status, content type, length only.

    Each of the two requests has its own overall deadline of `timeout` seconds; None when it passes."""
    budget = _Budget(timeout)
    conn = resp = None
    try:
        conn, resp = _open(url, "HEAD", budget)
        if budget.expired:   # http.client treats EOF inside the headers as their end: never trust that
            return None
        if resp.status not in (405, 501):
            return ProbeResult(resp.status, resp.getheader("Content-Type"), _length(resp, resp.status))
    except (OSError, http.client.HTTPException, ValueError):
        return None
    finally:
        _close(conn, resp)
        budget.done()
    budget = _Budget(timeout)
    conn = resp = None
    try:
        conn, resp = _open(url, "GET", budget, {"Range": "bytes=0-0"})
        resp.read(1)   # never more than one byte, and it is discarded
        if budget.expired:
            return None
        status = 200 if resp.status == 206 else resp.status   # a satisfied range request means the file exists
        return ProbeResult(status, resp.getheader("Content-Type"), _length(resp, resp.status))
    except (OSError, http.client.HTTPException, ValueError):
        return None
    finally:
        _close(conn, resp)
        budget.done()


# ---------------------------------------------------------------- TLS

_OLD = (("TLSv1", "TLSv1"), ("TLSv1.1", "TLSv1_1"))


def _issuer(cert: dict) -> Optional[str]:
    found = {}
    for rdn in cert.get("issuer", ()):
        for k, v in rdn:
            found[k] = v
    return found.get("organizationName") or found.get("commonName")


def _date(cert: dict, key: str) -> Optional[dt.datetime]:
    if key not in cert:
        return None
    return dt.datetime.fromtimestamp(ssl.cert_time_to_seconds(cert[key]), dt.timezone.utc)


def _error_kind(exc: ssl.SSLCertVerificationError) -> str:
    code = getattr(exc, "verify_code", None)
    if code == 10:
        return "expired"
    if code == 62:
        return "name-mismatch"
    return "untrusted"


def _try_old(host: str, port: int, timeout: float) -> Optional[List[str]]:
    try:
        return _try_old_inner(host, port, timeout)
    except Exception:   # whatever the local OpenSSL does, the answer is "couldn't try"
        return None


def _try_old_inner(host: str, port: int, timeout: float) -> Optional[List[str]]:
    """Which of TLSv1 / TLSv1.1 the server accepts; None when the local OpenSSL can't try them."""
    accepted: List[str] = []
    tried = 0
    for name, attr in _OLD:
        try:
            version = getattr(ssl.TLSVersion, attr)
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with warnings.catch_warnings():   # Python 3.10+ deprecates these versions
                warnings.simplefilter("ignore", DeprecationWarning)
                ctx.minimum_version = version
                ctx.maximum_version = version
            try:
                ctx.set_ciphers("ALL:@SECLEVEL=0")
            except ssl.SSLError:
                pass
        except (ValueError, ssl.SSLError, AttributeError):
            continue
        try:
            budget = _Budget(timeout)
            try:
                _secure_socket(host, port, ctx, budget)
                accepted.append(name)
                tried += 1
            finally:
                budget.done()
        except ssl.SSLError as exc:
            if "NO_PROTOCOLS_AVAILABLE" in str(exc) or "UNSUPPORTED_PROTOCOL" in str(exc).upper() and \
                    getattr(exc, "reason", "") == "NO_PROTOCOLS_AVAILABLE":
                continue            # refused locally, not by the server
            tried += 1
        except OSError:
            tried += 1
    return accepted if tried else None


def tls_info(host: str, port: int = 443, timeout: float = DEFAULT_TIMEOUT) -> TlsInfo:
    """Inspect the certificate. Each connection (the verified one, the unverified retry, each old-protocol
    try) has its own overall deadline of `timeout` seconds; when it passes the result is "unreachable"."""
    ctx = ssl.create_default_context()
    version = issuer = None
    not_after = not_before = None
    error = None
    budget = _Budget(timeout)
    try:
        s = _secure_socket(host, port, ctx, budget)
        version = s.version()
        cert = s.getpeercert() or {}
        issuer, not_after, not_before = _issuer(cert), _date(cert, "notAfter"), _date(cert, "notBefore")
    except ssl.SSLCertVerificationError as exc:
        error = _error_kind(exc)
        budget.done()
        budget = _Budget(timeout)
        try:  # read the protocol version without verifying
            raw = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            raw.check_hostname = False
            raw.verify_mode = ssl.CERT_NONE
            version = _secure_socket(host, port, raw, budget).version()
        except (OSError, ssl.SSLError):
            pass
    except (OSError, ssl.SSLError, ValueError):
        return TlsInfo(None, None, None, "unreachable", None)
    finally:
        budget.done()
    return TlsInfo(version, not_after, issuer, error, _try_old(host, port, timeout), not_before)


# ---------------------------------------------------------------- DNS

def build_txt_query(name: str, qid: int) -> bytes:
    out = struct.pack(">HHHHHH", qid & 0xFFFF, 0x0100, 1, 0, 0, 0)
    labels = name.rstrip(".").split(".")
    total = 0
    for label in labels:
        raw = label.encode("idna") if not label.isascii() else label.encode("ascii")
        if not 1 <= len(raw) <= 63:
            raise ValueError("invalid DNS label")
        total += len(raw) + 1
        out += bytes([len(raw)]) + raw
    if total > 254:   # 253 characters of name plus the root byte
        raise ValueError("DNS name too long")
    return out + b"\x00" + struct.pack(">HH", 16, 1)


def _skip_name(data: bytes, pos: int) -> int:
    while True:
        n = data[pos]
        if n == 0:
            return pos + 1
        if n & 0xC0 == 0xC0:
            return pos + 2
        pos += 1 + n


def parse_txt_answer(data: bytes) -> Tuple[List[str], bool]:
    """(records, truncated); each record's strings are joined. ValueError for a malformed or failed answer."""
    try:
        _, flags, qd, an, _, _ = struct.unpack(">HHHHHH", data[:12])
        if not flags & 0x8000 or (flags >> 11) & 0xF:
            raise ValueError("not a DNS response")
        if flags & 0x000F not in (0, 3):      # anything but NOERROR / NXDOMAIN is "no answer"
            raise ValueError("DNS error code %d" % (flags & 0xF))
        truncated = bool(flags & 0x0200)
        pos = 12
        for _ in range(qd):
            pos = _skip_name(data, pos) + 4
        records: List[str] = []
        for _ in range(an):
            pos = _skip_name(data, pos)
            rtype, _, _, rdlen = struct.unpack(">HHIH", data[pos:pos + 10])
            pos += 10
            rdata = data[pos:pos + rdlen]
            if len(rdata) != rdlen:
                raise ValueError("short answer")
            pos += rdlen
            if rtype != 16:
                continue
            parts, i = [], 0
            while i < len(rdata):
                n = rdata[i]
                parts.append(rdata[i + 1:i + 1 + n])
                i += 1 + n
            records.append(b"".join(parts).decode("utf-8", "replace"))
        return records, truncated
    except (struct.error, IndexError) as exc:
        raise ValueError("malformed DNS answer") from exc


def _udp(resolver: str, port: int, query: bytes, timeout: float) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(timeout)
        s.sendto(query, (resolver, port))
        return s.recvfrom(4096)[0]


def _tcp(resolver: str, port: int, query: bytes, timeout: float) -> bytes:
    with socket.create_connection((resolver, port), timeout=timeout) as s:
        s.settimeout(timeout)
        s.sendall(struct.pack(">H", len(query)) + query)
        head = b""
        while len(head) < 2:
            chunk = s.recv(2 - len(head))
            if not chunk:
                raise OSError("closed")
            head += chunk
        want, buf = struct.unpack(">H", head)[0], b""
        while len(buf) < want:
            chunk = s.recv(want - len(buf))
            if not chunk:
                raise OSError("closed")
            buf += chunk
        return buf


def dns_txt(name: str, resolvers=("1.1.1.1", "8.8.8.8"), timeout: float = DNS_TIMEOUT,
            port: int = 53) -> Optional[List[str]]:
    """TXT records of `name`. [] for NXDOMAIN or an empty answer; None when no resolver answered at all."""
    qid = int.from_bytes(os.urandom(2), "big")
    try:
        query = build_txt_query(name, qid)
    except ValueError:
        return None
    for resolver in resolvers:
        try:
            data = _udp(resolver, port, query, timeout)
            if data[:2] != query[:2]:
                continue
            records, truncated = parse_txt_answer(data)
            if truncated:
                data = _tcp(resolver, port, query, timeout)
                if data[:2] != query[:2]:
                    continue
                records, _ = parse_txt_answer(data)
            return records
        except (OSError, ValueError):
            continue
    return None
