#!/usr/bin/env python3
"""Website Audit Suite security scan (passive).

    python scripts/security-scan.py URL [--probe-files] [--out DIR]

Writes DIR/security-scan.json (facts), DIR/audit-data/security.json and DIR/security.md.
The homepage's redirects are followed while they stay on the entered host or its www/apex twin; every later
request goes to where they end.
Exit codes: 0 success, 2 usage error, 3 the site could not be reached or read (nothing is written).
"""
import datetime as dt
import ipaddress
import json
import sys
import time
import uuid
from pathlib import Path
from urllib.parse import urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))

from security import DIRECTORY_PATHS, RUBRIC, fetch  # noqa: E402
from security import checks  # noqa: E402
from security.draft import draft_page  # noqa: E402
from security.text import render_text  # noqa: E402
from security.paths import PLATFORM_NAMES  # noqa: E402
from security.platform import detect_platforms, select_paths  # noqa: E402

USAGE = "usage: security-scan.py <URL> [--probe-files] [--out DIR]"
PROBE_DELAY = 2.0   # seconds between exposed-file requests
STOP_AFTER = 3      # consecutive unanswered probes after which probing stops
FILES_NOT_CHECKED = "Exposed files: not checked, because ownership wasn't confirmed."
REDIRECTS = (301, 302, 303, 307, 308)
MAX_REDIRECTS = 5   # homepage redirects followed on the site itself
DEFAULT_PORTS = {"http": 80, "https": 443}


def _is_ip(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _site_hosts(host):
    """The entered host and its www/apex twin; an IP address has no twin."""
    if _is_ip(host):
        return {host}
    apex = host[4:] if host.startswith("www.") else host
    return {apex, "www." + apex}


def _email(host):
    """(Outcome, facts) for SPF and DMARC. The email domain is the host without www.; when it has no DMARC
    record, a subdomain's parent (never a public suffix) is asked once, and if the parent has one, both
    records come from the parent. An IP address has no domain to ask about."""
    if _is_ip(host):
        return (checks.Outcome(not_checked=[(checks.EMAIL_ROW, checks.EMAIL_IP_NOTE)]),
                {"domain": None, "spf": None, "dmarc": None})
    domain = host[4:] if host.startswith("www.") else host
    spf = fetch.dns_txt(domain)
    dmarc = fetch.dns_txt("_dmarc." + domain)
    parent, inherited = checks.parent_domain(domain), False
    if parent and dmarc is not None and not checks.has_dmarc(dmarc):
        up = fetch.dns_txt("_dmarc." + parent)
        if checks.has_dmarc(up):
            domain, dmarc, spf, inherited = parent, up, fetch.dns_txt(parent), True
    return checks.check_email(spf, dmarc, domain, inherited), {"domain": domain, "spf": spf, "dmarc": dmarc}


def _location(resp):
    """Where a redirect points, as an absolute URL; None when `resp` isn't a redirect with a Location."""
    locs = checks.values(resp, "Location") if resp.status in REDIRECTS else []
    return urljoin(resp.url, locs[0].strip()) if locs else None


def _on_site(url, hosts, port):
    """http or https, on the entered host or its twin, on the entered port or the scheme's default one."""
    try:
        parts = urlsplit(url)
        scheme = parts.scheme.lower()
        used = parts.port or DEFAULT_PORTS.get(scheme)
    except ValueError:
        return False
    return (scheme in DEFAULT_PORTS and (parts.hostname or "").lower() in hosts
            and used in {DEFAULT_PORTS[scheme], port})


def _follow(resp, hosts, port, stop_at_https=False):
    """Follow `resp`'s redirects while they stay on the site, at most MAX_REDIRECTS of them.

    Returns (chain, off_site): the responses in order (the last is None when a hop didn't answer), and the
    address of a redirect that leaves the site, which is never requested. With `stop_at_https` the chain
    stops before requesting an https address."""
    chain = [resp]
    for _ in range(MAX_REDIRECTS):
        nxt = _location(resp)
        if nxt is None:
            break
        if not _on_site(nxt, hosts, port):
            return chain, nxt
        if stop_at_https and urlsplit(nxt).scheme.lower() == "https":
            break
        resp = fetch.get(nxt)
        chain.append(resp)
        if resp is None:
            break
    return chain, None


def _scheme(resp):
    return urlsplit(resp.url).scheme.lower()


def _headers(resp):
    """Header list for the facts file; Set-Cookie keeps the cookie name only."""
    out = []
    for k, v in resp.headers:
        if k.lower() == "set-cookie":
            v = v.split(";", 1)[0].split("=", 1)[0].strip() if "=" in v.split(";", 1)[0] else ""
            v = v or "(unnamed)"
        out.append([k, v])
    return out


def _resp_facts(resp):
    return None if resp is None else {"url": resp.url, "status": resp.status, "headers": _headers(resp)}


def _outcome_facts(o):
    return {"hits": [{"check": h.check, "evidence": h.evidence} for h in o.hits],
            "strengths": list(o.strengths), "not_checked": [list(n) for n in o.not_checked]}


def _text(resp):
    return resp.body if resp is not None and resp.status == 200 else None


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(USAGE)
        return 2
    url, probe_files, out_dir, rest = argv[0], False, ".", list(argv[1:])
    while rest:
        arg = rest.pop(0)
        if arg == "--probe-files":
            probe_files = True
        elif arg == "--out" and rest:
            out_dir = rest.pop(0)
        else:
            print(USAGE)
            return 2
    if "://" not in url:
        url = "https://" + url
    try:
        parts = urlsplit(url)
        host, port = parts.hostname or "", parts.port
    except ValueError:
        host = port = None
    if not host:
        print("%s is not a valid URL." % argv[0], file=sys.stderr)
        return 2
    netloc = host if ":" not in host else "[%s]" % host
    netloc += ":%d" % port if port else ""

    https_resp = fetch.get("https://%s/" % netloc)
    http_resp = fetch.get("http://%s/" % netloc)
    if https_resp is None and http_resp is None:
        print("Could not reach %s over HTTPS or HTTP, so no security check ran." % url, file=sys.stderr)
        return 3
    # The homepage is where the site's own redirects end. Every later request goes there.
    hosts = _site_hosts(host)
    chain, off_site = _follow(https_resp or http_resp, hosts, port)
    home = chain[-1]
    if off_site is not None:
        print("%s redirects to %s, which is another site, so no security check ran. Run it on that address if "
              "that site is yours." % (url, off_site), file=sys.stderr)
        return 3
    if home is None:
        print("%s redirects to %s, which didn't answer, so no security check ran." % (url, _location(chain[-2])),
              file=sys.stderr)
        return 3
    if not 200 <= home.status < 300:
        print("%s answered %d, so the check couldn't read the site (it may be blocked, password-protected or "
              "down). No security check ran." % (url, home.status), file=sys.stderr)
        return 3
    home_parts = urlsplit(home.url)
    base = "%s://%s" % (home_parts.scheme, home_parts.netloc)

    # The transport check judges where http:// leads (through the twin too) and the https answer it saw.
    if https_resp is None:
        http_chain = chain
    else:
        http_chain = _follow(http_resp, hosts, port, stop_at_https=True)[0] if http_resp is not None else []
    http_last = next((r for r in reversed(http_chain) if r is not None and _scheme(r) == "http"), None)
    secure = https_resp or next((r for r in chain if r is not None and _scheme(r) == "https"), None)
    # The certificate is read where the secure homepage is, else where https answered, else on the entered host.
    tls_at = home if _scheme(home) == "https" else secure
    if tls_at is not None:
        tls_host, tls_port = urlsplit(tls_at.url).hostname, urlsplit(tls_at.url).port or 443
    else:
        tls_host, tls_port = host, port or 443
    tls = fetch.tls_info(tls_host, tls_port)

    robots = fetch.get(base + "/robots.txt")
    sitemap = fetch.get(base + "/sitemap.xml")
    sec_txt = fetch.get(base + "/.well-known/security.txt")
    dirs = {p: fetch.get(base + p) for p in DIRECTORY_PATHS}

    email, email_facts = _email(host)

    parts_out = {
        "page": checks.check_page(home),
        "robots": checks.check_robots(_text(robots)),
        "sitemap": checks.check_sitemap(_text(sitemap)),
        "security_txt": checks.check_security_txt(sec_txt),
        "directories": checks.check_directories(dirs),
        "transport": checks.check_transport(tls_host, http_last, secure, tls),
        "email": email,
    }
    probes = None
    scope = platforms = paths_checked = unanswered = None
    stopped_early = False
    if probe_files:
        platforms = detect_platforms(home)
        picked = select_paths(platforms)
        paths_checked = len(picked)
        baselines, probes = {}, {}
        queue = [("", ext) for ext in sorted({""} | {checks.script_extension(p) for p, _ in picked})]
        queue += [("path", path) for path, _ in picked]
        misses = asked = asked_paths = 0
        for kind, key in queue:
            address = "/%s-not-here%s" % (uuid.uuid4().hex, key) if kind == "" else key
            result, tried = None, False   # not probed: recorded as unanswered
            for _ in range(2 if kind == "" else 1):   # a baseline that got no answer is asked once more
                if misses >= STOP_AFTER:
                    stopped_early = True
                    break
                time.sleep(PROBE_DELAY)
                result, tried = fetch.probe(base + address), True
                if checks.answered(result):   # a 429 or 503 counts as no answer
                    misses = 0
                    break
                misses += 1
            (baselines if kind == "" else probes)[key] = result
            if tried:
                asked += 1
                asked_paths += kind != ""
                if asked % 10 == 0:
                    print("Checked %d of %d addresses..." % (asked, len(queue)), file=sys.stderr, flush=True)
        unanswered = sum(1 for r in probes.values() if not checks.answered(r))
        parts_out["files"] = checks.classify_probes(probes, baselines)
        names = ", ".join(PLATFORM_NAMES[k] for k in sorted(platforms, key=lambda k: (k == "php", k)))
        if stopped_early:
            scope = (("Recognised platform: %s. " % names if platforms else "The platform wasn't recognised. ")
                     + "The file check asked about %d of %d well-known addresses before the server stopped "
                       "answering." % (asked_paths, paths_checked))
        elif platforms:
            scope = "Recognised platform: %s. The file check looked at %d well-known addresses." % (
                names, paths_checked)
        else:
            scope = ("The platform wasn't recognised, so the file check looked at all %d addresses on its "
                     "list." % paths_checked)
    else:
        parts_out["files"] = checks.Outcome(not_checked=[(RUBRIC[0][0], FILES_NOT_CHECKED)])

    outcome = checks.merge(*parts_out.values())
    date = dt.date.today().isoformat()
    page = draft_page(outcome, scope)
    markdown = render_text(page, url, date)

    facts = {"url": url, "date": date, "probed_files": probe_files}
    if probe_files:
        facts["platforms"] = platforms
        facts["paths_checked"] = paths_checked
        facts["unanswered"] = unanswered
        facts["probe_stopped_early"] = stopped_early
    facts["page"] = {"homepage": _resp_facts(home),
                     "redirects": [{"url": r.url, "status": r.status} for r in chain[:-1]],
                     "https": _resp_facts(https_resp), "http": _resp_facts(http_resp)}
    facts["transport"] = None if tls is None else {
        "version": tls.version, "error": tls.error, "issuer": tls.issuer, "old_protocols": tls.old_protocols,
        "not_before": tls.not_before.isoformat() if tls.not_before else None,
        "not_after": tls.not_after.isoformat() if tls.not_after else None}
    facts["robots"] = {"status": robots.status if robots else None}
    facts["sitemap"] = {"status": sitemap.status if sitemap else None}
    facts["security_txt"] = {"status": sec_txt.status if sec_txt else None}
    facts["directories"] = {p: (r.status if r else None) for p, r in dirs.items()}
    facts["email"] = email_facts
    facts["files"] = None if probes is None else {
        p: (None if r is None else {"status": r.status, "content_type": r.content_type, "length": r.length})
        for p, r in probes.items()}
    facts["results"] = {name: _outcome_facts(o) for name, o in parts_out.items()}

    out = Path(out_dir)
    paths = [out / "security-scan.json", out / "audit-data" / "security.json", out / "security.md"]
    _write(paths[0], json.dumps(facts, indent=2, ensure_ascii=False) + "\n")
    _write(paths[1], json.dumps(page, indent=2, ensure_ascii=False) + "\n")
    _write(paths[2], markdown)
    for p in paths:
        print(p)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):   # a path a cp1252 console can't show is escaped, not a crash
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    sys.exit(main(sys.argv[1:]))
