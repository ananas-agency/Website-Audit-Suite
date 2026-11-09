"""Pure checks on one fetched page (a Response): headers, cookies, versions, mixed content, forms, files.

No I/O happens here. Each check turns what was fetched into hits (a check id from wording.CHECKS plus
evidence) and strengths (an id from wording.STRENGTHS). Evidence is an exact header line or element
snippet of at most 200 characters; cookie values never appear in it, only cookie names.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlsplit

from . import RUBRIC
from .paths import CORE_PATHS, PLATFORM_PATHS, SCRIPT_EXTENSIONS

MAX_EVIDENCE = 200
HSTS_MIN_AGE = 15552000
SENSITIVE_WORDS = ("admin", "administrator", "login", "staging", "stage", "backup", "backups", "config",
                   "configuration")   # matched as whole path segments


@dataclass
class Response:
    url: str
    status: int
    headers: List[Tuple[str, str]] = field(default_factory=list)
    body: str = ""


@dataclass
class Hit:
    check: str
    evidence: str


@dataclass
class Outcome:
    hits: List[Hit] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    not_checked: List[Tuple[str, str]] = field(default_factory=list)


def merge(*outcomes: Outcome) -> Outcome:
    out = Outcome()
    for o in outcomes:
        out.hits.extend(o.hits)
        for s in o.strengths:
            if s not in out.strengths:
                out.strengths.append(s)
        out.not_checked.extend(o.not_checked)
    return out


def values(resp: Response, name: str) -> List[str]:
    name = name.lower()
    return [v for k, v in resp.headers if k.lower() == name]


def _clip(text: str) -> str:
    text = " ".join(text.split())
    return text if len(text) <= MAX_EVIDENCE else text[:MAX_EVIDENCE - 3] + "..."


def _line(name: str, value: str) -> str:
    return _clip("%s: %s" % (name, value))


# ---------------------------------------------------------------- HTML

class _Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.generators: List[str] = []
        self.assets: List[str] = []                            # snippets of http:// assets
        self.forms: List[dict] = []
        self.passwords: List[Tuple[str, Optional[int]]] = []   # (snippet, index of its form or None)
        self._open_form: Optional[int] = None

    @staticmethod
    def _snippet(tag: str, attrs: list) -> str:
        parts = [tag] + ['%s="%s"' % (k, v if v is not None else "") for k, v in attrs]
        return _clip("<" + " ".join(parts) + ">")

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta" and a.get("name", "").lower() == "generator":
            self.generators.append(a.get("content", ""))
        elif tag in ("script", "img", "iframe", "source", "audio", "video"):
            if a.get("src", "").strip().lower().startswith("http://"):
                self.assets.append(self._snippet(tag, attrs))
        elif tag == "link" and "stylesheet" in a.get("rel", "").lower().split():
            if a.get("href", "").strip().lower().startswith("http://"):
                self.assets.append(self._snippet(tag, attrs))
        elif tag == "form":
            self.forms.append({"action": a.get("action", "").strip(), "snippet": self._snippet(tag, attrs)})
            self._open_form = len(self.forms) - 1
        elif tag == "input" and a.get("type", "").strip().lower() == "password":
            self.passwords.append((self._snippet(tag, attrs), self._open_form))

    def handle_endtag(self, tag):
        if tag == "form":
            self._open_form = None


def _parse(body: str) -> _Page:
    p = _Page()
    try:
        p.feed(body)
        p.close()
    except Exception:  # malformed HTML must never break a check
        pass
    return p


# ---------------------------------------------------------------- headers

def _csp_directives(policy: str) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for part in policy.split(";"):
        toks = part.split()
        if toks:
            out.setdefault(toks[0].lower(), toks[1:])
    return out


def _weak_csp(policies: List[str]) -> Optional[str]:
    """The first enforcing policy whose script rules allow inline/eval code or any source, as evidence."""
    for pol in policies:
        d = _csp_directives(pol)
        # default-src only applies when the policy has no script-src / script-src-elem of its own
        names = ("script-src", "script-src-elem")
        if not any(n in d for n in names):
            names = ("default-src",)
        for name in names:
            srcs = [s.lower() for s in d.get(name, [])]
            strict = any(s.startswith(("'nonce-", "'sha")) or s == "'strict-dynamic'" for s in srcs)
            if any(s in ("'unsafe-eval'", "*") or (s == "'unsafe-inline'" and not strict) for s in srcs):
                return _line("Content-Security-Policy", pol)
    return None


def _hsts(resp: Response, out: Outcome) -> bool:
    """Record HSTS hits for an https page. Returns True when HSTS is present and not weak."""
    vals = values(resp, "Strict-Transport-Security")
    if not vals:
        out.hits.append(Hit("no-hsts", "No Strict-Transport-Security header"))
        return False
    v = vals[0]
    m = re.search(r"max-age\s*=\s*\"?(\d+)", v, re.I)
    age = int(m.group(1)) if m else 0
    if age < HSTS_MIN_AGE or not re.search(r"includesubdomains", v, re.I):
        out.hits.append(Hit("hsts-weak", _line("Strict-Transport-Security", v)))
        return False
    return True


def _headers(resp: Response, out: Outcome, https: bool) -> None:
    enforcing = values(resp, "Content-Security-Policy")
    if not enforcing:
        note = " (only Report-Only)" if values(resp, "Content-Security-Policy-Report-Only") else ""
        out.hits.append(Hit("no-csp", "No Content-Security-Policy header" + note))
    else:
        weak = _weak_csp(enforcing)
        if weak:
            out.hits.append(Hit("weak-csp", weak))
        else:
            out.strengths.append("csp-set")

    frame_ok = bool(values(resp, "X-Frame-Options")) or any(
        "frame-ancestors" in _csp_directives(p) for p in enforcing)
    if not frame_ok:
        out.hits.append(Hit("no-frame-protection", "No X-Frame-Options header or CSP frame-ancestors"))

    if not any(v.strip().lower() == "nosniff" for v in values(resp, "X-Content-Type-Options")):
        out.hits.append(Hit("no-nosniff", "No X-Content-Type-Options: nosniff header"))

    ref = values(resp, "Referrer-Policy")
    if not ref:
        out.hits.append(Hit("no-referrer-policy", "No Referrer-Policy header"))
    else:
        toks = [t.strip().lower() for v in ref for t in v.split(",")]
        if toks and toks[-1] == "unsafe-url":  # the last token is the one browsers honour
            out.hits.append(Hit("unsafe-referrer-policy", _line("Referrer-Policy", ref[-1])))

    if not (values(resp, "Permissions-Policy") or values(resp, "Feature-Policy")):
        out.hits.append(Hit("no-permissions-policy", "No Permissions-Policy header"))

    if not any(values(resp, n) for n in
               ("Cross-Origin-Opener-Policy", "Cross-Origin-Embedder-Policy", "Cross-Origin-Resource-Policy")):
        out.hits.append(Hit("no-cross-origin-policies", "No Cross-Origin-Opener-Policy, "
                            "Cross-Origin-Embedder-Policy or Cross-Origin-Resource-Policy header"))

    xss = values(resp, "X-XSS-Protection")
    if xss and not xss[0].strip().startswith("0"):
        out.hits.append(Hit("outdated-xss-header", _line("X-XSS-Protection", xss[0])))

    if https and _hsts(resp, out):
        out.strengths.append("hsts-set")


# ---------------------------------------------------------------- cookies

def _cookies(resp: Response, out: Outcome) -> None:
    host = (urlsplit(resp.url).hostname or "").lower()
    found: Dict[str, List[str]] = {"cookie-no-secure": [], "cookie-no-httponly": [],
                                   "cookie-no-samesite": [], "cookie-broad-domain": []}
    cookies = values(resp, "Set-Cookie")
    for raw in cookies:
        parts = [p.strip() for p in raw.split(";")]
        # a first token without "=" is not a name=value pair; never echo it (it may be a bare value)
        name = parts[0].split("=", 1)[0].strip() if "=" in parts[0] else ""
        name = name or "(unnamed)"
        attrs = {}
        for p in parts[1:]:
            k, _, v = p.partition("=")
            attrs[k.strip().lower()] = v.strip()
        if "secure" not in attrs:
            found["cookie-no-secure"].append(name)
        if "httponly" not in attrs:
            found["cookie-no-httponly"].append(name)
        if "samesite" not in attrs:
            found["cookie-no-samesite"].append(name)
        dom = attrs.get("domain", "").lstrip(".").lower()
        if dom and host and host != dom and host.endswith("." + dom):
            found["cookie-broad-domain"].append(name)
    labels = {"cookie-no-secure": "no Secure", "cookie-no-httponly": "no HttpOnly",
              "cookie-no-samesite": "no SameSite", "cookie-broad-domain": "Domain is a parent domain"}
    for check, names in found.items():
        if names:
            uniq = list(dict.fromkeys(names))
            out.hits.append(Hit(check, _clip("Set-Cookie: %s (%s)" % (", ".join(uniq), labels[check]))))
    if cookies and not any(found.values()):
        out.strengths.append("cookies-flagged")


# ---------------------------------------------------------------- versions

_VERSION = re.compile(r"\d+\.\d+|/\s*\d+")


def _versions(resp: Response, page: _Page, out: Outcome) -> None:
    lines = ["%s: %s" % (k, v) for k, v in resp.headers
             if (k.lower() in ("server", "x-powered-by") or k.lower().startswith("x-aspnet"))
             and _VERSION.search(v)]
    if lines:
        out.hits.append(Hit("server-version", _clip(" | ".join(lines))))
    gens = [g for g in page.generators if re.search(r"\d+\.\d+", g)]
    if gens:
        out.hits.append(Hit("generator-version", _clip('<meta name="generator" content="%s">' % gens[0])))
    if not lines and not gens:
        out.strengths.append("no-version-leaks")


# ---------------------------------------------------------------- page

def _more(first: str, count: int) -> str:
    return first if count <= 1 else _clip("%s (+%d more)" % (first[:MAX_EVIDENCE - 20], count - 1))


def check_page(resp: Response) -> Outcome:
    out = Outcome()
    https = urlsplit(resp.url).scheme.lower() == "https"
    page = _parse(resp.body or "")
    _headers(resp, out, https)
    _cookies(resp, out)
    _versions(resp, page, out)

    if https and page.assets:
        out.hits.append(Hit("mixed-content", _more(page.assets[0], len(page.assets))))

    # A form is sent over http when it posts to http://, or when the page itself is http and the form
    # does not name an https:// target.
    bad_forms = []
    for i, f in enumerate(page.forms):
        action = f["action"].lower()
        if action.startswith("http://") or (
                not https and not action.startswith(("https://", "mailto:", "javascript:"))):
            bad_forms.append(i)
    if bad_forms:
        out.hits.append(Hit("form-over-http", _more(page.forms[bad_forms[0]]["snippet"], len(bad_forms))))

    pw = [snip for snip, idx in page.passwords if (not https) or (idx is not None and idx in bad_forms)]
    if pw:
        out.hits.append(Hit("password-over-http", _more(pw[0], len(pw))))
    return out


# ---------------------------------------------------------------- other files

def _sensitive(path: str) -> bool:
    """True when a whole path segment is a sensitive word, compared without case, its extension or robots.txt
    wildcards (`/login.php`, `/Admin*`): `/badminton-club/` or `/blog/backup-your-site` don't count."""
    for segment in path.split("?", 1)[0].split("/"):
        if segment.strip("*$").split(".", 1)[0].lower() in SENSITIVE_WORDS:
            return True
    return False


def check_robots(text: Optional[str]) -> Outcome:
    out = Outcome()
    if not text:
        return out
    lines = []
    for raw in text.splitlines():
        m = re.match(r"disallow\s*:\s*(\S+)", raw.split("#", 1)[0].strip(), re.I)
        if not m:
            continue
        path = m.group(1)
        if re.match(r"/wp-admin(?![\w-])", path, re.I):  # WordPress's default; not a finding
            continue
        if _sensitive(path):
            lines.append("Disallow: " + path)
    if lines:
        out.hits.append(Hit("robots-names-sensitive-areas", _clip("; ".join(lines))))
    return out


def check_sitemap(text: Optional[str]) -> Outcome:
    out = Outcome()
    if not text:
        return out
    urls = []
    for m in re.finditer(r"<loc>\s*(.*?)\s*</loc>", text, re.I | re.S):
        if _sensitive(urlsplit(m.group(1)).path):
            urls.append(m.group(1))
    if urls:
        out.hits.append(Hit("sitemap-lists-sensitive-urls", _clip("; ".join(urls))))
    return out


def check_security_txt(resp: Optional[Response]) -> Outcome:
    """The strength needs a real file: a 200, plain text, and a `Contact:` line (RFC 9116). A site that shows
    a normal page for every address answers 200 with HTML, which isn't one."""
    out = Outcome()
    ctype = (values(resp, "Content-Type") or [""])[0] if resp is not None else ""
    if resp is None:
        why = "could not be fetched"
    elif resp.status != 200:
        why = "returned %d" % resp.status
    elif ctype.split(";")[0].strip().lower() != "text/plain":
        why = "is not plain text (Content-Type: %s)" % (ctype.strip() or "none")
    elif not re.search(r"^[ \t]*contact:", resp.body or "", re.I | re.M):
        why = "has no Contact line"
    else:
        out.strengths.append("security-txt")
        return out
    out.hits.append(Hit("no-security-txt", _clip("/.well-known/security.txt " + why)))
    return out


def check_directories(pages: Dict[str, Optional[Response]]) -> Outcome:
    out = Outcome()
    found = [path for path, r in pages.items()
             if r is not None and re.search(r"<title>\s*Index of /", r.body or "", re.I)]
    if found:
        out.hits.append(Hit("directory-listing", _clip("<title>Index of /... at " + ", ".join(found))))
    return out


# ---------------------------------------------------------------- transport

HTTPS_ROW = next(n for n, _ in RUBRIC if n.startswith("HTTPS"))
EMAIL_ROW = next(n for n, _ in RUBRIC if n.startswith("Email"))
EXPIRY_WARN_DAYS = 15
_REDIRECTS = (301, 302, 307, 308)


def _host_of(target: str) -> str:
    host = urlsplit(target if "://" in target else "//" + target).hostname or target
    return host.lower()


def _redirects_to_https(http_resp: Response, hosts: set) -> bool:
    if http_resp.status not in _REDIRECTS:
        return False
    locs = values(http_resp, "Location")
    if not locs:
        return False
    dest = urlsplit(urljoin(http_resp.url, locs[0].strip()))
    return dest.scheme.lower() == "https" and (dest.hostname or "").lower() in hosts


def check_transport(target, http_resp, https_resp, tls, now=None) -> Outcome:
    """The HTTPS row: https reachable, http redirects to it, certificate state, old TLS versions."""
    out = Outcome()
    host = _host_of(target)
    apex = host[4:] if host.startswith("www.") else host
    hosts = {apex, "www." + apex}
    now = now or dt.datetime.now(dt.timezone.utc)

    if https_resp is None:
        if http_resp is not None and _redirects_to_https(http_resp, hosts):
            # The site sends visitors to https, which didn't answer this time: that says nothing either way.
            out.not_checked.append((HTTPS_ROW, "HTTPS: not checked, because the secure version of the site "
                                               "didn't answer in time."))
        elif http_resp is not None:
            out.hits.append(Hit("no-https", _clip("https://%s/ could not be reached; http:// answered %d"
                                                  % (host, http_resp.status))))
        return out

    if http_resp is not None and not _redirects_to_https(http_resp, hosts):
        locs = values(http_resp, "Location")
        if http_resp.status in _REDIRECTS and locs:
            what = "redirects to " + locs[0].strip()
        else:
            what = "answered %d with no redirect to https" % http_resp.status
        out.hits.append(Hit("no-https-redirect", _clip("%s %s" % (http_resp.url, what))))

    if tls is None or tls.error == "unreachable":
        out.not_checked.append((HTTPS_ROW, "Certificate: not checked, because the secure connection "
                                           "couldn't be inspected."))
        return out

    if tls.error == "expired":
        when = " on %s" % tls.not_after.date().isoformat() if tls.not_after else ""
        out.hits.append(Hit("cert-expired", "The certificate for %s expired%s" % (host, when)))
    elif tls.error == "name-mismatch":
        out.hits.append(Hit("cert-name-mismatch", "The certificate does not cover %s" % host))
    elif tls.error == "untrusted":
        who = " (issuer: %s)" % tls.issuer if tls.issuer else ""
        out.hits.append(Hit("cert-untrusted", _clip("The certificate for %s is not trusted%s" % (host, who))))
    elif tls.not_after is not None:
        warn = dt.timedelta(days=EXPIRY_WARN_DAYS)
        if tls.not_before is not None and tls.not_after > tls.not_before:
            warn = min(warn, (tls.not_after - tls.not_before) / 3)
        if tls.not_after - now < warn:
            out.hits.append(Hit("cert-expiring", "The certificate for %s expires on %s"
                                % (host, tls.not_after.date().isoformat())))

    if tls.old_protocols:
        out.hits.append(Hit("old-tls", "The server still accepts " + ", ".join(tls.old_protocols)))

    if not out.hits:
        out.strengths.append("https-valid")
    return out


# ---------------------------------------------------------------- email

def _all_qualifier(spf: str) -> Optional[str]:
    """The qualifier of the record's final `all` term ('+', '-', '~' or '?'), None when it has none."""
    for tok in reversed(spf.lower().split()):
        m = re.fullmatch(r"([+\-~?]?)all", tok)
        if m:
            return m.group(1) or "+"
    return None


def _record(records: List[str], prefix: str) -> Optional[str]:
    for r in records:
        if r.strip().lower().startswith(prefix):
            return r.strip()
    return None


EMAIL_IP_NOTE = "Email: not checked, because the site was given as an IP address."
# Two-label public suffixes: a subdomain's parent here is a registry, never the owner's domain.
TWO_LABEL_SUFFIXES = frozenset((
    "co.uk", "org.uk", "ac.uk", "gov.uk", "com.au", "net.au", "org.au", "com.ua", "org.ua", "net.ua", "in.ua",
    "kiev.ua", "co.nz", "co.za", "com.br", "com.tr", "co.jp", "com.mx", "com.cn", "com.sg", "co.in"))


def parent_domain(domain: str) -> Optional[str]:
    """The domain one label up, for a domain of more than two labels whose parent isn't a public suffix."""
    labels = domain.split(".")
    parent = ".".join(labels[1:])
    return parent if len(labels) > 2 and parent not in TWO_LABEL_SUFFIXES else None


def has_dmarc(records: Optional[List[str]]) -> bool:
    return records is not None and _record(records, "v=dmarc1") is not None


def check_email(spf: Optional[List[str]], dmarc: Optional[List[str]], domain: Optional[str] = None,
                inherited: bool = False) -> Outcome:
    """SPF and DMARC of `domain` (the name looked up). `inherited`: the records are a parent domain's, taken
    because the site's own domain has no DMARC record; the evidence says so."""
    out = Outcome()
    if spf is None or dmarc is None:
        out.not_checked.append((EMAIL_ROW, "Email protection: not checked, because the domain's DNS records "
                                           "couldn't be looked up."))
    taken = "Taken from %s: " % domain if inherited and domain else ""
    qual = policy = None
    if spf is not None:
        spf_rec = _record(spf, "v=spf1")
        if spf_rec is None:
            out.hits.append(Hit("no-spf", "No `v=spf1` record at `%s`" % domain if domain
                                else "No SPF record (v=spf1) in the domain's TXT records"))
        else:
            qual = _all_qualifier(spf_rec)
            if qual in ("+", "?"):
                out.hits.append(Hit("weak-spf", _clip(taken + spf_rec)))
    if dmarc is not None:
        dmarc_rec = _record(dmarc, "v=dmarc1")
        if dmarc_rec is None:
            out.hits.append(Hit("no-dmarc", "No `v=DMARC1` record at `_dmarc.%s`" % domain if domain
                                else "No DMARC record (v=DMARC1) at _dmarc in the domain's TXT records"))
        else:
            m = re.search(r"(?:^|;)\s*p\s*=\s*(\w+)", dmarc_rec, re.I)
            policy = m.group(1).lower() if m else None
            if policy == "none":
                out.hits.append(Hit("dmarc-monitor-only", _clip(taken + dmarc_rec)))
    if qual in ("-", "~") and policy in ("quarantine", "reject"):
        out.strengths.append("email-protected")
    return out


# ---------------------------------------------------------------- exposed files

_KIND = dict(CORE_PATHS)
for _entries in PLATFORM_PATHS.values():
    _KIND.update(_entries)
_CHECK_FOR_KIND = {"secret": "exposed-secrets", "info": "exposed-info-files",
                   "admin": "exposed-admin-tools", "backdoor": "possible-backdoor"}
_ORDER = ("exposed-unclear", "exposed-secrets", "exposed-info-files", "exposed-admin-tools", "possible-backdoor")


NO_ANSWER = (429, 503)        # "slow down" / "unavailable": the server didn't really answer
MISSING = (404, 410)          # how a server says an address doesn't exist


def answered(r) -> bool:
    """True when a probe got a real answer: not None, and not a rate-limit or unavailable status."""
    return r is not None and r.status not in NO_ANSWER


def script_extension(path: str) -> str:
    """The script extension a path ends with, or "" (the key of its soft-404 baseline)."""
    low = path.lower()
    return next((e for e in SCRIPT_EXTENSIONS if low.endswith(e)), "")


def _baseline_for(path: str, baselines):
    """The answered baseline for the path's extension, else the answered "" one, else None."""
    for key in (script_extension(path), ""):
        if answered(baselines.get(key)):
            return baselines[key]
    return None


def _same_type(a: Optional[str], b: Optional[str]) -> bool:
    def norm(t):
        return (t or "").split(";")[0].strip().lower()
    return norm(a) == norm(b)


def _resembles(r, baseline) -> bool:
    if baseline is None or baseline.status != 200 or r.status != baseline.status or not _same_type(r.content_type, baseline.content_type):
        return False
    if r.length is None or baseline.length is None:
        return True
    return abs(r.length - baseline.length) <= max(64, 0.05 * baseline.length)


def _lines_evidence(lines: List[str]) -> str:
    """One line per file, cut to MAX_EVIDENCE characters with a '(+N more)' tail when lines are dropped."""
    shown = len(lines)
    while shown > 1 and len("\n".join(lines[:shown])) + (len("\n(+%d more)" % (len(lines) - shown))
                                                          if shown < len(lines) else 0) > MAX_EVIDENCE:
        shown -= 1
    text = "\n".join(lines[:shown])
    if shown < len(lines):
        text += "\n(+%d more)" % (len(lines) - shown)
    return text[:MAX_EVIDENCE]


def classify_probes(results, baselines) -> Outcome:
    """Sort probe results into hits. `baselines` maps "" or a script extension to the probe of a made-up
    address with that extension; each path is compared with the answered baseline for its own extension,
    else the "" one. A hit is a 200 (for admin tools a 401 too); one that resembles its baseline, or has no
    baseline to compare with, is "unclear". A 429 or 503 counts as no answer. A path that gets the same
    status as its baseline, other than 200 or a missing-page status, can't be told apart from a made-up
    address. "Nothing open" needs a "" baseline that answered as missing, and every path answered and told."""
    out = Outcome()
    groups: Dict[str, List[str]] = {check: [] for check in _ORDER}
    cant_tell: List[int] = []
    for path, r in results.items():
        if not answered(r):
            continue
        baseline = _baseline_for(path, baselines)
        if baseline is not None and r.status == baseline.status and r.status != 200 and r.status not in MISSING:
            cant_tell.append(r.status)
            continue
        kind = _KIND.get(path, "info")
        if r.status != 200 and not (kind == "admin" and r.status == 401):
            continue
        line = "%s %d %s %s" % (path, r.status, r.content_type or "unknown",
                                r.length if r.length is not None else "unknown")
        if (baseline is None and r.status == 200) or _resembles(r, baseline):
            groups["exposed-unclear"].append(line)
        else:
            groups[_CHECK_FOR_KIND[kind]].append(line)
    for check in _ORDER:
        if groups[check]:
            out.hits.append(Hit(check, _lines_evidence(groups[check])))
    unanswered = sum(1 for r in results.values() if not answered(r))
    if unanswered:
        out.not_checked.append((RUBRIC[0][0], (
            "Exposed files: %d of %d addresses got no answer, possibly because the server started blocking "
            "the check, so they weren't checked." % (unanswered, len(results)))))
    if cant_tell:
        out.not_checked.append((RUBRIC[0][0], (
            "Exposed files: %d of %d addresses gave the same answer as an address that doesn't exist (%s), so the "
            "check couldn't tell whether they're there." % (
                len(cant_tell), len(results), ", ".join(str(s) for s in sorted(set(cant_tell)))))))
    plain = baselines.get("")
    if (results and not out.hits and not unanswered and not cant_tell
            and answered(plain) and plain.status in MISSING):
        out.strengths.append("no-exposed-files")
    return out
