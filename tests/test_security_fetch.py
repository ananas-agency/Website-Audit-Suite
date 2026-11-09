"""Network layer (scripts/security/fetch.py) against a local server, plus transport/email/probe checks."""
import datetime as dt
import http.client
import pathlib
import socket
import struct
import sys
import threading
import time
import unittest
import warnings
from unittest import mock
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from security import USER_AGENT  # noqa: E402
from security.paths import CORE_PATHS as EXPOSED_PATHS  # noqa: E402
from security import checks as c  # noqa: E402
from security import fetch  # noqa: E402

HTTPS_ROW = "HTTPS & TLS (version, cert validity, HSTS)"
EMAIL_ROW = "Email/domain spoofing protection (SPF/DMARC)"
PAGE = b"<html>" + b"x" * 888 + b"</html>"  # 900 bytes


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, ctype="text/plain", body=b"", extra=(), head=False):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def _handle(self):
        srv = self.server
        srv.log.append((self.command, self.path, dict(self.headers)))
        head = self.command == "HEAD"
        if srv.mode == "nohead" and head:
            return self._send(405, head=True)
        if self.path == "/ua":
            return self._send(200, body=self.headers.get("User-Agent", "").encode(), head=head)
        if self.path == "/redir":
            return self._send(302, extra=[("Location", "/elsewhere")], head=head)
        if srv.mode == "catch-all":
            return self._send(200, "text/html", PAGE, head=head)
        if srv.mode == "nohead" and self.path == "/.env":
            return self._send(200, body=b"S" * 5000, head=head)
        if self.path == "/.env":
            return self._send(200, "text/plain", b"S" * 20, head=head)
        return self._send(404, "text/html", b"nope", head=head)

    do_GET = do_HEAD = _handle


class TestNetwork(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.srv.daemon_threads = True
        cls.srv.mode = "real"
        cls.srv.log = []
        cls.thread = threading.Thread(target=cls.srv.serve_forever, kwargs={"poll_interval": 0.05})
        cls.thread.start()
        cls.base = "http://127.0.0.1:%d" % cls.srv.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()
        cls.thread.join()

    def setUp(self):
        self.srv.mode = "real"
        self.srv.log.clear()

    def probe_all(self):
        return {p: fetch.probe(self.base + p, timeout=3) for p, _ in EXPOSED_PATHS}

    def test_exposed_env_found(self):
        res = self.probe_all()
        base = fetch.probe(self.base + "/zz-no-such-page-7f3a", timeout=3)
        out = c.classify_probes(res, {"": base})
        self.assertEqual([h.check for h in out.hits], ["exposed-secrets"])
        self.assertIn("/.env 200 text/plain 20", out.hits[0].evidence)
        self.assertEqual({m for m, _, _ in self.srv.log}, {"HEAD"})

    def test_head_rejected_uses_one_byte_range(self):
        self.srv.mode = "nohead"
        amounts = []
        real_read, real_read1 = http.client.HTTPResponse.read, http.client.HTTPResponse.read1

        def rec_read(self_, amt=None):
            amounts.append(amt)
            return real_read(self_, amt)

        def rec_read1(self_, n=-1):
            amounts.append(n)
            return real_read1(self_, n)
        with mock.patch.object(http.client.HTTPResponse, "read", rec_read),                 mock.patch.object(http.client.HTTPResponse, "read1", rec_read1):
            r = fetch.probe(self.base + "/.env", timeout=3)
        self.assertEqual(r.status, 200)
        self.assertEqual(r.length, 5000)
        self.assertTrue(amounts and all(a is not None and 0 <= a <= 1 for a in amounts), amounts)
        gets = [h for m, p, h in self.srv.log if m == "GET"]
        self.assertEqual(len(gets), 1)
        self.assertEqual(gets[0].get("Range"), "bytes=0-0")

    def test_catch_all_site_is_unclear_not_exposed(self):
        self.srv.mode = "catch-all"
        res = self.probe_all()
        base = fetch.probe(self.base + "/zz-no-such-page-7f3a", timeout=3)
        out = c.classify_probes(res, {"": base})
        self.assertEqual([h.check for h in out.hits], ["exposed-unclear"])
        self.assertEqual(out.strengths, [])

    def test_user_agent_sent(self):
        r = fetch.get(self.base + "/ua", timeout=3)
        self.assertEqual(r.body, USER_AGENT)
        fetch.probe(self.base + "/x", timeout=3)
        self.assertTrue(all(h.get("User-Agent") == USER_AGENT for _, _, h in self.srv.log))

    def test_get_does_not_follow_redirects(self):
        r = fetch.get(self.base + "/redir", timeout=3)
        self.assertEqual(r.status, 302)
        self.assertIn(("Location", "/elsewhere"), r.headers)
        self.assertEqual(len(self.srv.log), 1)

    def test_unreachable_is_none(self):
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        self.assertIsNone(fetch.get("http://127.0.0.1:%d/" % port, timeout=2))
        self.assertIsNone(fetch.probe("http://127.0.0.1:%d/" % port, timeout=2))


def raw_server(payload, per_byte_delay=0.0, fast=0, hold=0.0):
    """One-shot raw-socket HTTP server; returns (port, thread, listening socket)."""
    ls = socket.socket()
    ls.bind(("127.0.0.1", 0))
    ls.listen(5)
    ls.settimeout(5)

    def run():
        try:
            for _ in range(2):
                conn, _ = ls.accept()
                with conn:
                    conn.settimeout(5)
                    conn.recv(4096)
                    try:
                        conn.sendall(payload[:fast])
                        for i in range(fast, len(payload)):
                            conn.sendall(payload[i:i + 1])
                            if per_byte_delay:
                                time.sleep(per_byte_delay)
                    except OSError:
                        pass
                    time.sleep(hold)   # keep the connection open before closing it
        except OSError:
            pass
    t = threading.Thread(target=run)
    t.start()
    return ls.getsockname()[1], t, ls


class TestRobustness(unittest.TestCase):
    def test_bad_content_length_does_not_crash_probe(self):
        port, t, ls = raw_server(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: \xb2\r\n\r\n")
        try:
            r = fetch.probe("http://127.0.0.1:%d/.env" % port, timeout=2)
        finally:
            ls.close()
            t.join()
        self.assertEqual((r.status, r.length), (200, None))

    def test_slow_trickle_hits_overall_deadline(self):
        payload = b"HTTP/1.1 200 OK\r\nContent-Length: 1000\r\n\r\n" + b"a" * 1000
        port, t, ls = raw_server(payload, per_byte_delay=0.05, fast=payload.index(b"a"))
        start = time.monotonic()
        try:
            r = fetch.get("http://127.0.0.1:%d/" % port, timeout=0.6)
        finally:
            ls.close()
            t.join()
        self.assertIsNone(r)
        self.assertLess(time.monotonic() - start, 2.5)

    def _trickled(self, call, payload):
        port, t, ls = raw_server(payload, per_byte_delay=0.05)
        start = time.monotonic()
        try:
            res = call(port)
        finally:
            elapsed = time.monotonic() - start
            ls.close()
            t.join()
        return res, elapsed

    def test_trickled_headers_hit_deadline_in_get(self):
        res, took = self._trickled(lambda port: fetch.get("http://127.0.0.1:%d/" % port, timeout=0.6),
                                   b"HTTP/1.1 200 OK\r\nX-Slow: " + b"a" * 400 + b"\r\n\r\n")
        self.assertIsNone(res)
        self.assertLess(took, 1.4)

    def test_trickled_headers_hit_deadline_in_probe(self):
        res, took = self._trickled(lambda port: fetch.probe("http://127.0.0.1:%d/.env" % port, timeout=0.6),
                                   b"HTTP/1.1 200 OK\r\nX-Slow: " + b"a" * 400 + b"\r\n\r\n")
        self.assertIsNone(res)
        self.assertLess(took, 1.4)

    def test_cut_off_headers_are_not_a_reply(self):
        # Headers cut off by the deadline must never become a successful reply, on any OS (where the timer's
        # shutdown makes a blocked read return EOF, http.client would treat it as the end of the headers).
        partial = b"HTTP/1.1 200 OK\r\nX-Slow: a"
        for call in (lambda port: fetch.probe("http://127.0.0.1:%d/.env" % port, timeout=0.4),
                     lambda port: fetch.get("http://127.0.0.1:%d/" % port, timeout=0.4)):
            port, t, ls = raw_server(partial, hold=1.0)
            start = time.monotonic()
            try:
                res = call(port)
            finally:
                took = time.monotonic() - start
                ls.close()
                t.join()
            self.assertIsNone(res)
            self.assertLess(took, 1.0)

    def test_expired_budget_voids_a_clean_looking_reply(self):
        real_open = fetch._open

        def expiring(url, method, budget, extra=None):
            out = real_open(url, method, budget, extra)
            budget.expired = True   # as if the timer fired just as the reply was read
            return out
        port, t, ls = raw_server(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
        try:
            with mock.patch.object(fetch, "_open", expiring):
                self.assertIsNone(fetch.probe("http://127.0.0.1:%d/.env" % port, timeout=2))
                self.assertIsNone(fetch.get("http://127.0.0.1:%d/" % port, timeout=2))
        finally:
            ls.close()
            t.join()

    def test_trickled_handshake_hits_deadline_in_tls_info(self):
        res, took = self._trickled(lambda port: fetch.tls_info("127.0.0.1", port, timeout=0.6),
                                   b"\x16\x03\x03\x04\x00" + b"\x00" * 1024)
        self.assertEqual(res.error, "unreachable")
        self.assertLess(took, 1.4)

    def test_try_old_survives_deprecation_warnings_as_errors(self):
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            res = fetch._try_old("127.0.0.1", port, 1)
        self.assertTrue(res is None or res == [])

    def test_try_old_exception_becomes_none(self):
        with mock.patch.object(fetch, "_try_old_inner", side_effect=RuntimeError("boom")):
            self.assertIsNone(fetch._try_old("127.0.0.1", 1, 1))


def R(url, status=200, headers=()):
    return c.Response(url, status, list(headers), "")


NOW = dt.datetime(2026, 11, 8, tzinfo=dt.timezone.utc)


def tls(**kw):
    d = dict(version="TLSv1.3", not_before=NOW - dt.timedelta(days=30), not_after=NOW + dt.timedelta(days=60),
             issuer="Test CA", error=None, old_protocols=[])
    d.update(kw)
    return fetch.TlsInfo(**d)


class TestTransport(unittest.TestCase):
    def run_t(self, http, https, t):
        return c.check_transport("example.com", http, https, t, now=NOW)

    def ids(self, o):
        return [h.check for h in o.hits]

    def test_redirect_to_www_twin_counts(self):
        https = R("https://example.com/")
        ok = self.run_t(R("http://example.com/", 301, [("Location", "https://www.example.com/")]), https, tls())
        self.assertNotIn("no-https-redirect", self.ids(ok))
        self.assertIn("https-valid", ok.strengths)
        bad = self.run_t(R("http://example.com/", 301, [("Location", "https://other.com/")]), https, tls())
        self.assertIn("no-https-redirect", self.ids(bad))
        plain = self.run_t(R("http://example.com/", 200), https, tls())
        self.assertIn("no-https-redirect", self.ids(plain))
        nohttp = self.run_t(None, https, tls())
        self.assertNotIn("no-https-redirect", self.ids(nohttp))
        tohttp = self.run_t(R("http://example.com/", 302, [("Location", "http://example.com/x")]), https, tls())
        self.assertIn("no-https-redirect", self.ids(tohttp))

    def test_no_https(self):
        o = self.run_t(R("http://example.com/"), None, None)
        self.assertEqual(self.ids(o), ["no-https"])
        self.assertEqual(self.ids(self.run_t(None, None, None)), [])

    def test_silent_https_behind_an_https_redirect_is_not_checked(self):
        note = "HTTPS: not checked, because the secure version of the site didn't answer in time."
        for loc in ("https://example.com/", "https://www.example.com/x"):
            with self.subTest(loc=loc):
                o = self.run_t(R("http://example.com/", 301, [("Location", loc)]), None, None)
                self.assertEqual((self.ids(o), o.not_checked), ([], [(HTTPS_ROW, note)]))
        for http in (R("http://example.com/", 301, [("Location", "https://other.com/")]),
                     R("http://example.com/", 301, [("Location", "http://www.example.com/")]),
                     R("http://example.com/", 200)):
            with self.subTest(http=http.headers):
                o = self.run_t(http, None, None)
                self.assertEqual((self.ids(o), o.not_checked), (["no-https"], []))

    def test_cert_outcomes(self):
        https = R("https://example.com/")
        e = self.run_t(None, https, tls(error="expired", not_after=NOW - dt.timedelta(days=2)))
        self.assertIn("cert-expired", self.ids(e))
        self.assertNotIn("https-valid", e.strengths)
        self.assertIn("cert-name-mismatch", self.ids(self.run_t(None, https, tls(error="name-mismatch"))))
        self.assertIn("cert-untrusted", self.ids(self.run_t(None, https, tls(error="untrusted"))))
        old = self.run_t(None, https, tls(old_protocols=["TLSv1", "TLSv1.1"]))
        self.assertIn("old-tls", self.ids(old))
        # 90-day certificate warns at 15 days, not at 20
        life = dict(not_before=NOW - dt.timedelta(days=75))
        soon = self.run_t(None, https, tls(not_after=NOW + dt.timedelta(days=14), **life))
        self.assertIn("cert-expiring", self.ids(soon))
        later = self.run_t(None, https, tls(not_after=NOW + dt.timedelta(days=20), **life))
        self.assertNotIn("cert-expiring", self.ids(later))
        # 6-day certificate only near its end (one third = 2 days)
        short = dict(not_before=NOW - dt.timedelta(days=4))
        mid = self.run_t(None, https, tls(not_after=NOW + dt.timedelta(days=2.5), **short))
        self.assertNotIn("cert-expiring", self.ids(mid))
        end = self.run_t(None, https, tls(not_after=NOW + dt.timedelta(days=1.5), **short))
        self.assertIn("cert-expiring", self.ids(end))

    def test_cert_not_inspectable(self):
        https = R("https://example.com/")
        note = "Certificate: not checked, because the secure connection couldn't be inspected."
        for t in (None, tls(error="unreachable")):
            o = self.run_t(None, https, t)
            self.assertEqual(self.ids(o), [])
            self.assertEqual(o.not_checked, [(HTTPS_ROW, note)])
        o = self.run_t(None, https, tls(old_protocols=None))
        self.assertEqual((self.ids(o), o.not_checked), ([], []))


class TestEmail(unittest.TestCase):
    def ids(self, o):
        return [h.check for h in o.hits]

    def test_dns_failure_is_not_checked(self):
        o = c.check_email(None, None)
        self.assertEqual(o.hits, [])
        self.assertEqual([r for r, _ in o.not_checked], [EMAIL_ROW])

    def test_email_rules(self):
        o = c.check_email(["v=spf1 include:x.com -all"], ["v=DMARC1; p=reject; rua=mailto:a@b.c"])
        self.assertEqual((o.hits, o.strengths), ([], ["email-protected"]))
        self.assertEqual(self.ids(c.check_email(["v=spf1 +all"], ["v=DMARC1; p=reject"])), ["weak-spf"])
        self.assertEqual(self.ids(c.check_email(["v=spf1 ?all"], ["v=DMARC1; p=quarantine"])), ["weak-spf"])
        self.assertEqual(self.ids(c.check_email(["v=spf1 -all"], [])), ["no-dmarc"])
        self.assertEqual(self.ids(c.check_email([], ["v=DMARC1; p=none"])), ["no-spf", "dmarc-monitor-only"])
        self.assertEqual(c.check_email(["v=spf1 ~all"], ["v=DMARC1; p=none"]).strengths, [])


def dns_answer(records, tc=False, rcode=0, qid=7, name="example.com"):
    q = b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\x00" + struct.pack(">HH", 16, 1)
    flags = 0x8180 | (0x0200 if tc else 0) | rcode
    out = struct.pack(">HHHHHH", qid, flags, 1, len(records), 0, 0) + q
    for strings in records:
        rdata = b"".join(bytes([len(s)]) + s for s in strings)
        out += b"\xc0\x0c" + struct.pack(">HHIH", 16, 1, 60, len(rdata)) + rdata
    return out


class TestDns(unittest.TestCase):
    def test_txt_strings_joined(self):
        data = dns_answer([[b"v=spf1 include:a", b".com -all"], [b"other"]])
        self.assertEqual(fetch.parse_txt_answer(data), (["v=spf1 include:a.com -all", "other"], False))

    def test_truncated_and_empty(self):
        self.assertEqual(fetch.parse_txt_answer(dns_answer([], tc=True)), ([], True))
        self.assertEqual(fetch.parse_txt_answer(dns_answer([], rcode=3)), ([], False))
        with self.assertRaises(ValueError):
            fetch.parse_txt_answer(dns_answer([], rcode=2))
        with self.assertRaises(ValueError):
            fetch.parse_txt_answer(b"\x00\x01")

    def test_build_query(self):
        q = fetch.build_txt_query("_dmarc.example.com", 0x1234)
        self.assertEqual(q[:2], b"\x12\x34")
        self.assertEqual(struct.unpack(">HHHHH", q[2:12]), (0x0100, 1, 0, 0, 0))
        self.assertEqual(q[12:], b"\x06_dmarc\x07example\x03com\x00\x00\x10\x00\x01")

    def test_echoed_query_is_not_an_answer(self):
        q = fetch.build_txt_query("example.com", 7)
        with self.assertRaises(ValueError):
            fetch.parse_txt_answer(q)
        with self.assertRaises(ValueError):   # response bit set but a non-zero opcode
            fetch.parse_txt_answer(dns_answer([], rcode=0)[:2] + struct.pack(">H", 0x8980) + dns_answer([])[4:])

    def test_invalid_names(self):
        for bad in ("a" * 64 + ".com", "a" * 300 + ".com", "a..com", ".".join(["a" * 60] * 5)):
            with self.assertRaises(ValueError):
                fetch.build_txt_query(bad, 1)
            self.assertIsNone(fetch.dns_txt(bad, resolvers=("127.0.0.1",), timeout=0.2, port=9))
        fetch.build_txt_query("a" * 63 + ".com", 1)

    def test_no_resolver_answers_is_none(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        self.assertIsNone(fetch.dns_txt("example.com", resolvers=("127.0.0.1",), timeout=0.3, port=port))

    def test_local_udp_resolver(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("127.0.0.1", 0))
        s.settimeout(3)
        port = s.getsockname()[1]

        def serve():
            data, addr = s.recvfrom(512)
            s.sendto(dns_answer([[b"hello"]], qid=struct.unpack(">H", data[:2])[0]), addr)
        t = threading.Thread(target=serve)
        t.start()
        try:
            got = fetch.dns_txt("example.com", resolvers=("127.0.0.1",), timeout=2, port=port)
            self.assertEqual(got, ["hello"])
        finally:
            t.join()
            s.close()


class TestClassify(unittest.TestCase):
    P = fetch.ProbeResult

    def test_rules(self):
        base = self.P(200, "text/html", 1000)
        res = {"/.env": self.P(200, "text/html", 1040), "/.git/HEAD": self.P(200, "text/plain", 23),
               "/robots.php": None, "/.svn/entries": self.P(404, "text/html", 5)}
        out = c.classify_probes(res, {"": base})
        self.assertEqual([h.check for h in out.hits], ["exposed-unclear", "exposed-secrets"])
        self.assertIn("/.git/HEAD 200 text/plain 23", out.hits[1].evidence)
        self.assertTrue(all(len(h.evidence) <= 200 for h in out.hits))
        far = c.classify_probes({"/.env": self.P(200, "text/html", 1100)}, {"": base})
        self.assertEqual([h.check for h in far.hits], ["exposed-secrets"])
        unknown = c.classify_probes({"/.env": self.P(200, "text/html", None)}, {"": base})
        self.assertEqual([h.check for h in unknown.hits], ["exposed-unclear"])
        four = self.P(404, "text/html", 4)
        clean = c.classify_probes({"/.env": four}, {"": four})
        self.assertEqual((clean.hits, clean.strengths), ([], ["no-exposed-files"]))


if __name__ == "__main__":
    unittest.main()
