"""security-scan.py and security-report.py against a local server (127.0.0.1 only, no real site)."""
import contextlib
import io
import json
import os
import pathlib
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO, load_script  # noqa: E402

FILES_ROW = "No sensitive files/paths exposed"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _handle(self):
        self.server.log.append((self.command, self.path, self.headers.get("Host")))
        head = self.command == "HEAD"
        body, ctype, code, extra = b"nope", "text/html", 404, []
        routed = None
        if self.server.route is not None:   # a test's own answer for this host and path, or None
            routed = self.server.route(self.command, (self.headers.get("Host") or "").rsplit(":", 1)[0], self.path)
        if routed is not None:
            code, ctype, body, extra = routed
        elif self.path == "/":
            body, code = b"<html><head><title>Home</title></head><body>Hello</body></html>", 200
            if self.server.home_body is not None:
                body = self.server.home_body
            extra = [("Set-Cookie", self.server.cookie)] + list(self.server.home_headers)
            if self.server.redirect:
                body, code, extra = b"", 302, extra + [("Location", self.server.redirect)]
        elif self.path == "/robots.txt":
            body, ctype, code = b"User-agent: *\nDisallow: /private/\n", "text/plain", 200
        elif self.path == "/.env":
            body, ctype, code = b"S" * 20, "text/plain", 200
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        if not head:
            self.wfile.write(body)

    do_GET = do_HEAD = _handle


def run_main(module, args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = module.main(args)
    return code, out.getvalue(), err.getvalue()


@contextlib.contextmanager
def names_to_localhost():
    """Every connection goes to 127.0.0.1 on the same port, whatever the host name; nothing is looked up."""
    real = socket.create_connection

    def connect(address, *args, **kwargs):
        return real(("127.0.0.1", address[1]), *args, **kwargs)
    with mock.patch.object(socket, "create_connection", connect):
        yield


class ServerCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.srv.daemon_threads = True
        cls.srv.log = []
        cls.srv.cookie = "sid=SECRET123; Path=/"
        cls.srv.redirect = cls.srv.route = None
        cls.srv.home_headers, cls.srv.home_body = [], None
        cls.thread = threading.Thread(target=cls.srv.serve_forever, kwargs={"poll_interval": 0.05})
        cls.thread.start()
        cls.url = "http://127.0.0.1:%d" % cls.srv.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()
        cls.thread.join()

    def setUp(self):
        self.srv.log.clear()
        self.srv.cookie = "sid=SECRET123; Path=/"
        self.srv.redirect = self.srv.route = None
        self.srv.home_headers, self.srv.home_body = [], None
        self._tmp = tempfile.TemporaryDirectory(prefix="sec cli ")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name)
        self.port = self.srv.server_address[1]
        self.netloc = "127.0.0.1:%d" % self.port

    def scan(self, *extra, url=None):
        module = load_script("scripts/security-scan.py")
        module.PROBE_DELAY = 0
        with mock.patch.object(module.fetch, "dns_txt", return_value=None), names_to_localhost():
            return run_main(module, [url or self.url, "--out", str(self.tmp), *extra])

    def facts(self):
        return json.loads((self.tmp / "security-scan.json").read_text(encoding="utf-8"))

    def page(self):
        return json.loads((self.tmp / "audit-data" / "security.json").read_text(encoding="utf-8"))


class TestScan(ServerCase):
    def test_scan_without_probe_marks_files_not_checked(self):
        code, out, err = self.scan()
        self.assertEqual(code, 0, err)
        for name in ("security-scan.json", "audit-data/security.json", "security.md"):
            self.assertTrue((self.tmp / name).is_file(), name)
            self.assertIn(name.split("/")[-1], out)
        page = self.page()
        row = next(r for r in page["rubric"] if r["criterion"] == FILES_ROW)
        self.assertEqual(row["result"], "Partial")
        self.assertIn("Exposed files: not checked, because ownership wasn't confirmed.", page["notes"])
        self.assertNotIn("HEAD", [m for m, _, _ in self.srv.log])
        self.assertEqual({h for _, _, h in self.srv.log}, {self.url.split("//")[1]})
        facts = json.loads((self.tmp / "security-scan.json").read_text(encoding="utf-8"))
        self.assertIs(facts["probed_files"], False)
        self.assertEqual(facts["url"], self.url)

    def test_scan_with_probe_finds_env(self):
        code, _, err = self.scan("--probe-files")
        self.assertEqual(code, 0, err)
        keys = [f["key"] for f in self.page()["findings"]]
        self.assertIn("exposed-secrets", keys)
        self.assertIn("HEAD", [m for m, _, _ in self.srv.log])
        self.assertTrue((self.tmp / "security-scan.json").is_file())
        self.assertIs(json.loads((self.tmp / "security-scan.json").read_text("utf-8"))["probed_files"], True)

    def test_probe_delay_is_two_seconds(self):
        self.assertEqual(load_script("scripts/security-scan.py").PROBE_DELAY, 2.0)

    def test_probe_stops_after_three_unanswered(self):
        module = load_script("scripts/security-scan.py")
        module.PROBE_DELAY = 0
        calls = []

        def fake(url):
            calls.append(url)
            return module.fetch.ProbeResult(404, "text/html", 4) if len(calls) < 5 else None

        with mock.patch.object(module.fetch, "dns_txt", return_value=None),                 mock.patch.object(module.fetch, "probe", side_effect=fake):
            code, _, err = run_main(module, [self.url, "--out", str(self.tmp), "--probe-files"])
        self.assertEqual(code, 0, err)
        self.assertEqual(len(calls), 7)
        facts = json.loads((self.tmp / "security-scan.json").read_text("utf-8"))
        self.assertIs(facts["probe_stopped_early"], True)
        self.assertEqual(facts["unanswered"], 149)
        self.assertEqual(sum(v is None for v in facts["files"].values()), 149)
        self.assertIn("149 of 149 addresses got no answer", self.page()["notes"])
        self.assertIn("The platform wasn't recognised. The file check asked about 1 of 149 well-known addresses "
                      "before the server stopped answering.", (self.tmp / "security.md").read_text("utf-8"))

    def test_early_stop_scope_keeps_the_platform(self):
        self.srv.home_body = b'<html><head><link rel="stylesheet" href="/wp-content/themes/a/s.css"></head></html>'
        module = load_script("scripts/security-scan.py")
        module.PROBE_DELAY = 0
        calls = []

        def fake(url):
            calls.append(url)
            return module.fetch.ProbeResult(404, "text/html", 4) if len(calls) <= 2 else None
        with mock.patch.object(module.fetch, "dns_txt", return_value=None), \
                mock.patch.object(module.fetch, "probe", side_effect=fake):
            code, _, err = run_main(module, [self.url, "--out", str(self.tmp), "--probe-files"])
        self.assertEqual(code, 0, err)
        scope = [e["body"] for e in self.page()["extra"] if e["title"] == "What the file check covered"]
        self.assertEqual(scope, ["Recognised platform: WordPress, PHP. The file check asked about 3 of 85 "
                                 "well-known addresses before the server stopped answering."])

    def test_normal_probe_is_not_stopped_early(self):
        self.scan("--probe-files")
        facts = json.loads((self.tmp / "security-scan.json").read_text("utf-8"))
        self.assertIs(facts["probe_stopped_early"], False)
        self.assertEqual(facts["unanswered"], 0)

    def test_progress_every_ten_addresses(self):
        code, _, err = self.scan("--probe-files")
        self.assertEqual(code, 0, err)
        progress = [line for line in err.splitlines() if line.startswith("Checked ")]
        self.assertEqual(progress, ["Checked %d of 154 addresses..." % i for i in range(10, 151, 10)])
        _, _, quiet = self.scan()
        self.assertNotIn("Checked ", quiet)

    def probed_paths(self):
        return [p for m, p, _ in self.srv.log if m == "HEAD"]

    def test_wordpress_site_gets_wordpress_and_php_paths(self):
        self.srv.home_headers = [("X-Powered-By", "PHP/8.3.36")]
        self.srv.home_body = (b'<html><head><link rel="stylesheet" href="/wp-content/themes/a/style.css">'
                              b'</head><body>Hi</body></html>')
        code, _, err = self.scan("--probe-files")
        self.assertEqual(code, 0, err)
        probed = self.probed_paths()
        self.assertIn("/wp-config.php.bak", probed)
        self.assertIn("/phpinfo.php", probed)
        self.assertNotIn("/config/database.yml", probed)
        real = [p for p in probed if "-not-here" not in p]
        self.assertEqual(len(real), 85)
        baselines = [p for p in probed if "-not-here" in p]
        self.assertEqual(sorted(p.rsplit("-not-here", 1)[1] for p in baselines), ["", ".php"])
        facts = json.loads((self.tmp / "security-scan.json").read_text("utf-8"))
        self.assertEqual((facts["platforms"], facts["paths_checked"]), (["php", "wordpress"], 85))
        md = (self.tmp / "security.md").read_text("utf-8")
        self.assertIn("## What the file check covered", md)
        self.assertIn("Recognised platform: WordPress, PHP. The file check looked at 85 well-known addresses.", md)
        extra = self.page()["extra"]
        self.assertEqual([e["title"] for e in extra][1:], ["What the file check covered"])

    def test_unrecognised_site_gets_every_path(self):
        code, _, err = self.scan("--probe-files")
        self.assertEqual(code, 0, err)
        probed = self.probed_paths()
        self.assertEqual(len([p for p in probed if "-not-here" not in p]), 149)
        self.assertEqual(len([p for p in probed if "-not-here" in p]), 5)
        self.assertIn("/config/database.yml", probed)
        facts = json.loads((self.tmp / "security-scan.json").read_text("utf-8"))
        self.assertEqual((facts["platforms"], facts["paths_checked"]), ([], 149))
        md = (self.tmp / "security.md").read_text("utf-8")
        self.assertIn("The platform wasn't recognised, so the file check looked at all 149 addresses on its list.", md)

    def test_no_scope_without_probe(self):
        self.scan()
        self.assertNotIn("What the file check covered", (self.tmp / "security.md").read_text("utf-8"))
        facts = json.loads((self.tmp / "security-scan.json").read_text("utf-8"))
        self.assertNotIn("platforms", facts)

    def test_outputs_hold_no_cookie_value(self):
        self.scan("--probe-files")
        for name in ("security-scan.json", "audit-data/security.json", "security.md"):
            self.assertNotIn("SECRET123", (self.tmp / name).read_text(encoding="utf-8"), name)

    def test_cookie_without_equals_is_not_stored(self):
        self.srv.cookie = "SECRETTOKEN; Secure"
        self.scan()
        for name in ("security-scan.json", "audit-data/security.json", "security.md"):
            self.assertNotIn("SECRETTOKEN", (self.tmp / name).read_text(encoding="utf-8"), name)

    def test_redirect_to_other_host_is_not_followed(self):
        other = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        other.daemon_threads = True
        other.log, other.cookie, other.redirect = [], "a=b", None
        t = threading.Thread(target=other.serve_forever, kwargs={"poll_interval": 0.05})
        t.start()
        self.addCleanup(t.join)
        self.addCleanup(other.server_close)
        self.addCleanup(other.shutdown)
        self.srv.redirect = "http://127.0.0.1:%d/" % other.server_address[1]
        code, _, err = self.scan("--probe-files")
        self.assertEqual(code, 3, err)
        self.assertIn("%s redirects to %s, which is another site, so no security check ran. Run it on that "
                      "address if that site is yours." % (self.url, self.srv.redirect), err)
        self.assertEqual(list(self.tmp.iterdir()), [])
        self.assertEqual(other.log, [])
        self.assertEqual({h for _, _, h in self.srv.log}, {self.url.split("//")[1]})

    def test_bad_urls_exit_2(self):
        module = load_script("scripts/security-scan.py")
        for bad in ("http://host:abc/", "http://[::1/"):
            with self.subTest(url=bad):
                code, out, err = run_main(module, [bad, "--out", str(self.tmp)])
                self.assertEqual(code, 2)
                self.assertIn("not a valid URL", out + err)
        self.assertEqual(list(self.tmp.iterdir()), [])

    def test_unreachable_writes_nothing(self):
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        url = "http://127.0.0.1:%d" % port
        r = subprocess.run([sys.executable, str(REPO / "scripts" / "security-scan.py"), url, "--out", str(self.tmp)],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("Could not reach %s over HTTPS or HTTP, so no security check ran." % url, r.stderr)
        self.assertEqual(list(self.tmp.iterdir()), [])


HOME = b"<html><head><title>Home</title></head><body>Hello</body></html>"
GUARDED = [("Content-Security-Policy", "default-src 'self'; frame-ancestors 'self'")]   # only on the real page


class TestHomepageRedirects(ServerCase):
    """The homepage's redirects are followed on the site itself; everything later goes to where they end."""

    def keys(self):
        return [f["key"] for f in self.page()["findings"]]

    def test_apex_to_www_scans_the_www_site(self):
        www = "www.example.test:%d" % self.port

        def route(method, host, path):
            if host == "example.test":   # the apex sends every address to its www twin
                return 301, "text/html", b"", [("Location", "http://%s%s" % (www, path))]
            if path == "/":
                return 200, "text/html", HOME, GUARDED
            return None
        self.srv.route = route
        code, _, err = self.scan("--probe-files", url="http://example.test:%d" % self.port)
        self.assertEqual(code, 0, err)
        self.assertNotIn("no-csp", self.keys())          # read from the www homepage, not the redirect
        self.assertIn("exposed-secrets", self.keys())    # /.env on the www host
        self.assertNotIn("None of the well-known private file addresses the check tried were open.",
                         self.page()["strengths"])
        heads = [h for m, _, h in self.srv.log if m == "HEAD"]
        self.assertTrue(heads)
        self.assertEqual(set(heads), {www})
        self.assertEqual({h for m, p, h in self.srv.log if p != "/"}, {www})
        self.assertIn(("GET", "/robots.txt", www), self.srv.log)
        self.assertEqual(self.facts()["page"]["homepage"]["url"], "http://%s/" % www)

    def test_redirect_to_a_path_on_the_same_host(self):
        def route(method, host, path):
            if path == "/":
                return 302, "text/html", b"", [("Location", "/en/")]
            if path == "/en/":
                return 200, "text/html", HOME, GUARDED
            return None
        self.srv.route = route
        code, _, err = self.scan("--probe-files")
        self.assertEqual(code, 0, err)
        self.assertNotIn("no-csp", self.keys())
        self.assertIn("exposed-secrets", self.keys())
        self.assertIn(("GET", "/robots.txt", self.netloc), self.srv.log)
        self.assertEqual(self.facts()["page"]["homepage"]["url"], self.url + "/en/")

    def test_redirect_to_another_site_writes_nothing(self):
        other = "http://other.test:%d/" % self.port

        def route(method, host, path):
            return (301, "text/html", b"", [("Location", other)]) if host == "example.test" else None
        self.srv.route = route
        url = "http://example.test:%d" % self.port
        code, out, err = self.scan("--probe-files", url=url)
        self.assertEqual(code, 3, err)
        self.assertEqual(err.strip(), "%s redirects to %s, which is another site, so no security check ran. "
                                      "Run it on that address if that site is yours." % (url, other))
        self.assertEqual(list(self.tmp.iterdir()), [])
        self.assertEqual({h for _, _, h in self.srv.log}, {"example.test:%d" % self.port})

    def test_homepage_that_is_not_2xx_writes_nothing(self):
        for status, everywhere in ((403, False), (401, True)):
            with self.subTest(status=status):
                self.srv.log.clear()

                def route(method, host, path, status=status, everywhere=everywhere):
                    if path == "/" or everywhere:
                        return status, "text/html", b"no", [("WWW-Authenticate", 'Basic realm="x"')]
                    return None
                self.srv.route = route
                code, _, err = self.scan("--probe-files")
                self.assertEqual(code, 3, err)
                self.assertEqual(err.strip(), "%s answered %d, so the check couldn't read the site (it may be "
                                              "blocked, password-protected or down). No security check ran."
                                 % (self.url, status))
                self.assertEqual(list(self.tmp.iterdir()), [])
                self.assertNotIn("HEAD", [m for m, _, _ in self.srv.log])

    def test_redirects_are_followed_at_most_five_times(self):
        self.srv.route = lambda method, host, path: (302, "text/html", b"", [("Location", "/")])
        code, _, err = self.scan()
        self.assertEqual(code, 3, err)
        self.assertIn("answered 302", err)
        self.assertEqual(len([p for m, p, _ in self.srv.log if m == "GET"]), 6)   # the first answer + 5

    def test_scheme_less_url_with_a_port(self):
        code, _, err = self.scan(url=self.netloc)
        self.assertEqual(code, 0, err)
        facts = self.facts()
        self.assertEqual(facts["url"], "https://" + self.netloc)
        self.assertEqual(facts["page"]["homepage"]["url"], "http://%s/" % self.netloc)
        self.assertIn(("GET", "/robots.txt", self.netloc), self.srv.log)
        self.assertEqual({h for _, _, h in self.srv.log}, {self.netloc})


NOTHING_OPEN = "None of the well-known private file addresses the check tried were open."


class TestProbeAnswers(ServerCase):
    """Rate limits, block pages and a dropped baseline never read as "nothing open"."""

    def test_rate_limit_after_a_real_hit_stops_the_probe(self):
        state = {"limited": False}

        def route(method, host, path):
            if method != "HEAD":
                return None
            if state["limited"]:
                return 429, "text/html", b"slow down", []
            state["limited"] = path == "/.env"   # everything after /.env is rate-limited
            return None
        self.srv.route = route
        code, _, err = self.scan("--probe-files")
        self.assertEqual(code, 0, err)
        page = self.page()
        secrets = next(f for f in page["findings"] if f["key"] == "exposed-secrets")
        self.assertIn("/.env 200", secrets["evidence"])
        self.assertNotIn(NOTHING_OPEN, page["strengths"])
        self.assertIn("addresses got no answer", page["notes"])
        heads = [p for m, p, _ in self.srv.log if m == "HEAD"]
        self.assertEqual(len(heads), 5 + 6 + 3)   # baselines, the paths up to /.env, three 429s
        self.assertIs(self.facts()["probe_stopped_early"], True)
        self.assertIn("The file check asked about 9 of 149 well-known addresses before the server stopped "
                      "answering.", (self.tmp / "security.md").read_text("utf-8"))

    def test_block_page_everywhere_is_cant_tell(self):
        self.srv.route = lambda method, host, path: None if path == "/" else (403, "text/html", b"denied", [])
        code, _, err = self.scan("--probe-files")
        self.assertEqual(code, 0, err)
        page = self.page()
        self.assertIn("Exposed files: 149 of 149 addresses gave the same answer as an address that doesn't exist "
                      "(403), so the check couldn't tell whether they're there.", page["notes"])
        self.assertNotIn(NOTHING_OPEN, page["strengths"])
        self.assertEqual(next(r["result"] for r in page["rubric"] if r["criterion"] == FILES_ROW), "Partial")

    def test_dropped_baseline_is_asked_again(self):
        body = b"<html><body>" + b"x" * 800 + b"</body></html>"
        self.srv.route = lambda method, host, path: (200, "text/html", body, [])   # a catch-all site
        module = load_script("scripts/security-scan.py")
        module.PROBE_DELAY = 0
        real, calls = module.fetch.probe, []

        def flaky(url):
            calls.append(url)
            return None if len(calls) == 1 else real(url)
        with mock.patch.object(module.fetch, "dns_txt", return_value=None), \
                mock.patch.object(module.fetch, "probe", side_effect=flaky):
            code, _, err = run_main(module, [self.url, "--out", str(self.tmp), "--probe-files"])
        self.assertEqual(code, 0, err)
        self.assertEqual(calls[0], calls[1])          # the "" baseline, asked once more
        keys = [f["key"] for f in self.page()["findings"] if f["key"].startswith(("exposed", "possible"))]
        self.assertEqual(keys, ["exposed-unclear"])


EMAIL_ROW = "Email/domain spoofing protection (SPF/DMARC)"
IP_NOTE = "Email: not checked, because the site was given as an IP address."


class TestEmailDomain(unittest.TestCase):
    """Which domain the SPF and DMARC lookups ask about (DNS answers are canned)."""

    def lookup(self, host, records):
        module = load_script("scripts/security-scan.py")
        asked = []

        def dns(name):
            asked.append(name)
            return records.get(name, [])
        with mock.patch.object(module.fetch, "dns_txt", side_effect=dns):
            outcome, facts = module._email(host)
        return outcome, facts, asked

    def test_subdomain_uses_the_parent_dmarc(self):
        o, facts, asked = self.lookup("shop.example.com", {"_dmarc.example.com": ["v=DMARC1; p=none"],
                                                           "example.com": ["v=spf1 ?all"]})
        self.assertEqual([h.check for h in o.hits], ["weak-spf", "dmarc-monitor-only"])
        for h in o.hits:
            self.assertTrue(h.evidence.startswith("Taken from example.com: "), h.evidence)
        self.assertEqual(asked, ["shop.example.com", "_dmarc.shop.example.com", "_dmarc.example.com", "example.com"])
        self.assertEqual(facts["domain"], "example.com")

    def test_subdomain_without_a_parent_record_keeps_its_own(self):
        o, facts, asked = self.lookup("www.shop.example.com", {})
        self.assertEqual(asked, ["shop.example.com", "_dmarc.shop.example.com", "_dmarc.example.com"])
        evidence = {h.check: h.evidence for h in o.hits}
        self.assertEqual(evidence["no-dmarc"], "No `v=DMARC1` record at `_dmarc.shop.example.com`")
        self.assertEqual(evidence["no-spf"], "No `v=spf1` record at `shop.example.com`")
        self.assertEqual(facts["domain"], "shop.example.com")

    def test_public_suffix_parent_is_never_asked(self):
        for host in ("example.com.ua", "www.example.com.ua", "shop.co.uk"):
            with self.subTest(host=host):
                o, _, asked = self.lookup(host, {})
                domain = host[4:] if host.startswith("www.") else host
                self.assertEqual(asked, [domain, "_dmarc." + domain])
                self.assertIn("No `v=DMARC1` record at `_dmarc.%s`" % domain, [h.evidence for h in o.hits])

    def test_two_label_domain_is_not_walked_up(self):
        o, _, asked = self.lookup("www.example.com", {"example.com": ["v=spf1 -all"],
                                                      "_dmarc.example.com": ["v=DMARC1; p=reject"]})
        self.assertEqual(asked, ["example.com", "_dmarc.example.com"])
        self.assertEqual((o.hits, o.strengths), ([], ["email-protected"]))

    def test_ip_host_is_not_checked(self):
        for host in ("127.0.0.1", "::1"):
            with self.subTest(host=host):
                o, facts, asked = self.lookup(host, {})
                self.assertEqual(asked, [])
                self.assertEqual((o.hits, o.strengths), ([], []))
                self.assertEqual(o.not_checked, [(EMAIL_ROW, IP_NOTE)])
                self.assertIsNone(facts["domain"])


class TestEmailInScan(ServerCase):
    def test_subdomain_scan_reads_the_parent_dmarc(self):
        module = load_script("scripts/security-scan.py")
        records = {"_dmarc.example.test": ["v=DMARC1; p=reject"], "example.test": ["v=spf1 -all"]}
        with mock.patch.object(module.fetch, "dns_txt", side_effect=lambda name: records.get(name, [])), \
                names_to_localhost():
            code, _, err = run_main(module, ["http://shop.example.test:%d" % self.port, "--out", str(self.tmp)])
        self.assertEqual(code, 0, err)
        keys = [f["key"] for f in self.page()["findings"]]
        self.assertNotIn("no-dmarc", keys)
        self.assertNotIn("no-spf", keys)
        self.assertEqual(self.facts()["email"]["domain"], "example.test")

    def test_ip_host_scan_has_the_note_and_no_lookup(self):
        module = load_script("scripts/security-scan.py")
        with mock.patch.object(module.fetch, "dns_txt", return_value=None) as dns:
            code, _, err = run_main(module, [self.url, "--out", str(self.tmp)])
        self.assertEqual(code, 0, err)
        dns.assert_not_called()
        page = self.page()
        self.assertIn(IP_NOTE, page["notes"])
        self.assertNotIn("couldn't be looked up", page["notes"])
        self.assertEqual(next(r["result"] for r in page["rubric"] if r["criterion"] == EMAIL_ROW), "Partial")


class TestNonAsciiFolder(ServerCase):
    def test_cyrillic_folder_on_a_cp1252_console(self):
        # The site is an IP address on 127.0.0.1, so the subprocess makes no DNS lookups.
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        env.pop("PYTHONUTF8", None)
        out = self.tmp / "аудит-сайту"
        for script, args in (("security-scan.py", [self.url, "--out", str(out)]),
                             ("security-report.py", [str(out)])):
            with self.subTest(script=script):
                r = subprocess.run([sys.executable, str(REPO / "scripts" / script), *args], env=env,
                                   capture_output=True, timeout=120)
                self.assertEqual(r.returncode, 0, (r.stdout + r.stderr).decode("cp1252", "replace"))
                self.assertNotIn(b"Traceback", r.stderr)
                self.assertTrue((out / "security.md").is_file())
        self.assertTrue((out / "security-scan.json").is_file())
        self.assertTrue((out / "audit-data" / "security.json").is_file())


class TestTransportChain(unittest.TestCase):
    """http -> http-www -> https-www counts as a redirect to HTTPS (canned answers, no network)."""

    def test_http_chain_through_www_counts_as_https_redirect(self):
        module = load_script("scripts/security-scan.py")
        R = module.checks.Response
        page = R("https://www.example.com/", 200, [], "<html><body>Hi</body></html>")
        answers = {
            "https://example.com/": R("https://example.com/", 301, [("Location", "https://www.example.com/")]),
            "http://example.com/": R("http://example.com/", 301, [("Location", "http://www.example.com/")]),
            "http://www.example.com/": R("http://www.example.com/", 301, [("Location", "https://www.example.com/")]),
            "https://www.example.com/": page,
        }
        asked = []

        def get(url, timeout=None):
            asked.append(url)
            return answers.get(url)
        now = module.dt.datetime.now(module.dt.timezone.utc)
        tls = module.fetch.TlsInfo("TLSv1.3", now + module.dt.timedelta(days=60), "Test CA", None, [],
                                   now - module.dt.timedelta(days=30))
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(module.fetch, "get", side_effect=get), \
                mock.patch.object(module.fetch, "tls_info", return_value=tls) as tls_info, \
                mock.patch.object(module.fetch, "dns_txt", return_value=None):
            code, _, err = run_main(module, ["example.com", "--out", tmp])
            self.assertEqual(code, 0, err)
            page = json.loads((pathlib.Path(tmp) / "audit-data" / "security.json").read_text("utf-8"))
        keys = [f["key"] for f in page["findings"]]
        self.assertNotIn("no-https-redirect", keys)
        self.assertNotIn("no-https", keys)
        self.assertIn("Your site loads over a secure connection with a valid certificate.", page["strengths"])
        tls_info.assert_called_once_with("www.example.com", 443)
        self.assertIn("https://www.example.com/robots.txt", asked)
        self.assertEqual({u.split("/")[2] for u in asked}, {"example.com", "www.example.com"})
        self.assertEqual(asked.count("https://www.example.com/"), 1)   # the http chain stops at the https hop


class TestReport(ServerCase):
    def report(self):
        module = load_script("scripts/security-report.py")
        return run_main(module, [str(self.tmp)])

    def test_report_rerenders_after_edit(self):
        self.scan()
        page = self.page()
        low = min(page["findings"], key=lambda f: f["impact"])
        low["impact"] = 5
        low["title"] = "Moved to the top"
        (self.tmp / "audit-data" / "security.json").write_text(json.dumps(page), encoding="utf-8")
        code, out, err = self.report()
        self.assertEqual(code, 0, err)
        self.assertIn("security.md", out)
        md = (self.tmp / "security.md").read_text(encoding="utf-8")
        self.assertIn("SEC-01", md)
        self.assertRegex(md, r"### SEC-01 [^\n]*Moved to the top")

    def test_report_rejects_bad_json(self):
        self.scan()
        page = self.page()
        page["findings"][0]["impact"] = 9
        (self.tmp / "audit-data" / "security.json").write_text(json.dumps(page), encoding="utf-8")
        code, out, err = self.report()
        self.assertEqual(code, 2)
        self.assertIn("impact", err)

    def test_report_input_errors_are_one_clear_line(self):
        self.scan()
        scan, sec = self.tmp / "security-scan.json", self.tmp / "audit-data" / "security.json"
        good_scan, good_sec = scan.read_text("utf-8"), sec.read_text("utf-8")

        def fail(expect):
            code, _, err = self.report()
            self.assertEqual(code, 2)
            self.assertIn(expect, err)
            self.assertEqual(len(err.strip().splitlines()), 1, err)

        sec.write_text("[1, 2]", encoding="utf-8")
        fail("audit-data/security.json must be a JSON object")
        sec.write_text(good_sec, encoding="utf-8")
        scan.write_text("{}", encoding="utf-8")
        fail("security-scan.json has no 'url'")
        scan.write_text("[]", encoding="utf-8")
        fail("security-scan.json must be a JSON object")
        scan.unlink()
        fail("security-scan.json is missing; run security-scan.py first")
        scan.write_text(good_scan, encoding="utf-8")
        sec.unlink()
        fail("audit-data/security.json is missing")

    def test_report_incomplete_page_is_one_clean_line(self):
        self.scan()
        sec = self.tmp / "audit-data" / "security.json"
        good = json.loads(sec.read_text("utf-8"))
        broken = [{}, dict(good, findings=[{"title": "x"}]), dict(good, findings=["x"]),
                  dict(good, rubric=[{}]), dict(good, rubric=5)]
        for page in broken:
            with self.subTest(page=str(page)[:60]):
                sec.write_text(json.dumps(page), encoding="utf-8")
                code, _, err = self.report()
                self.assertEqual(code, 2)
                self.assertTrue(err.strip())
                self.assertNotIn("Traceback", err)


if __name__ == "__main__":
    unittest.main()
