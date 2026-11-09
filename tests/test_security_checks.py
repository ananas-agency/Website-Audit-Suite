"""Checks on one fetched page (scripts/security/checks.py): offline, hand-built responses."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from security import checks as c  # noqa: E402
from security import fetch  # noqa: E402
from security import RUBRIC  # noqa: E402
from security import wording  # noqa: E402

GOOD = [
    ("Content-Security-Policy", "default-src 'self'; frame-ancestors 'self'"),
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ("Permissions-Policy", "camera=()"),
    ("Cross-Origin-Opener-Policy", "same-origin"),
    ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
]


def R(headers=(), body="", url="https://www.example.com/", status=200):
    return c.Response(url, status, list(headers), body)


def ids(o):
    return [h.check for h in o.hits]


class ChecksTests(unittest.TestCase):
    def test_missing_headers_on_https(self):
        self.assertEqual(set(ids(c.check_page(R()))), {
            "no-csp", "no-frame-protection", "no-nosniff", "no-referrer-policy",
            "no-permissions-policy", "no-cross-origin-policies", "no-hsts"})

    def test_header_quirks(self):
        o = c.check_page(R([("content-SECURITY-policy", "default-src 'self'"),
                            ("Content-Security-Policy", "script-src 'unsafe-inline'")] + GOOD[1:]))
        self.assertIn("weak-csp", ids(o))
        self.assertNotIn("no-csp", ids(o))
        self.assertNotIn("csp-set", o.strengths)
        o = c.check_page(R([("Content-Security-Policy-Report-Only", "default-src 'self'")]))
        self.assertIn("no-csp", ids(o))
        self.assertNotIn("csp-set", o.strengths)

    def test_frame_ancestors_counts_as_frame_protection(self):
        o = c.check_page(R([("Content-Security-Policy", "frame-ancestors 'none'")]))
        self.assertNotIn("no-frame-protection", ids(o))
        self.assertIn("no-frame-protection", ids(c.check_page(R())))

    def test_hsts_and_other_header_rules(self):
        o = c.check_page(R([("Strict-Transport-Security", "max-age=300")]))
        self.assertIn("hsts-weak", ids(o))
        self.assertNotIn("no-hsts", ids(o))
        self.assertNotIn("hsts-set", o.strengths)
        self.assertNotIn("no-hsts", ids(c.check_page(R(url="http://www.example.com/"))))
        o = c.check_page(R([("Referrer-Policy", "unsafe-url"), ("X-XSS-Protection", "1; mode=block")]))
        self.assertIn("unsafe-referrer-policy", ids(o))
        self.assertIn("outdated-xss-header", ids(o))

    def test_cookie_values_never_in_evidence(self):
        o = c.check_page(R([("Set-Cookie", "sid=SECRET123; Path=/")]))
        self.assertEqual({"cookie-no-secure", "cookie-no-httponly", "cookie-no-samesite"},
                         {i for i in ids(o) if i.startswith("cookie")})
        for h in o.hits:
            self.assertNotIn("SECRET123", h.evidence)
        self.assertEqual(next(h for h in o.hits if h.check == "cookie-no-secure").evidence,
                         "Set-Cookie: sid (no Secure)")

    def test_cookie_rules(self):
        o = c.check_page(R([("Set-Cookie", "a=1; Secure; HttpOnly; SameSite=Lax; Domain=example.com"),
                            ("Set-Cookie", "b=2; Path=/"), ("Set-Cookie", "d=3")]))
        self.assertEqual(ids(o).count("cookie-no-secure"), 1)
        self.assertEqual(next(h.evidence for h in o.hits if h.check == "cookie-no-secure"),
                         "Set-Cookie: b, d (no Secure)")
        broad = [h.evidence for h in o.hits if h.check == "cookie-broad-domain"]
        self.assertEqual(broad, ["Set-Cookie: a (Domain is a parent domain)"])
        ok = c.check_page(R([("Set-Cookie", "a=1; Secure; HttpOnly; SameSite=Lax; Path=/")]))
        self.assertIn("cookies-flagged", ok.strengths)
        self.assertEqual([i for i in ids(ok) if i.startswith("cookie")], [])
        dot = c.check_page(R([("Set-Cookie", "a=1; Secure; HttpOnly; SameSite=Lax; Domain=.example.com")]))
        self.assertIn("cookie-broad-domain", ids(dot))
        self.assertNotIn("cookies-flagged", dot.strengths)

    def test_versions_leak(self):
        self.assertIn("server-version", ids(c.check_page(R([("Server", "nginx/1.18.0")]))))
        o = c.check_page(R([("Server", "nginx")]))
        self.assertNotIn("server-version", ids(o))
        self.assertIn("no-version-leaks", o.strengths)
        self.assertIn("server-version", ids(c.check_page(R([("X-AspNet-Version", "4.0.30319")]))))
        o = c.check_page(R(body='<meta name="generator" content="WordPress 6.4.2">'))
        self.assertIn("generator-version", ids(o))
        self.assertNotIn("no-version-leaks", o.strengths)
        o = c.check_page(R(body='<meta name="generator" content="Wix">'))
        self.assertNotIn("generator-version", ids(o))

    def test_mixed_content_only_on_https(self):
        body = '<img src="http://cdn.example.com/a.png"><link rel="stylesheet" href="http://x/s.css">'
        self.assertIn("mixed-content", ids(c.check_page(R(body=body))))
        self.assertNotIn("mixed-content", ids(c.check_page(R(body=body, url="http://www.example.com/"))))
        self.assertNotIn("mixed-content", ids(c.check_page(R(body='<a href="http://x/">x</a>'))))

    def test_forms_over_http(self):
        o = c.check_page(R(body='<form action="http://x.example/login"><input name=q></form>'))
        self.assertIn("form-over-http", ids(o))
        o = c.check_page(R(body='<form action="/go"><input type="password" name="p"></form>',
                           url="http://www.example.com/"))
        self.assertIn("password-over-http", ids(o))
        o = c.check_page(R(body='<form action="/go"><input type="password" name="p"></form>'))
        self.assertNotIn("password-over-http", ids(o))
        self.assertNotIn("form-over-http", ids(o))

    def test_robots_and_sitemap_sensitive(self):
        o = c.check_robots("User-agent: *\nDisallow: /admin/\nDisallow: /blog/\n")
        self.assertEqual(ids(o), ["robots-names-sensitive-areas"])
        self.assertIn("/admin/", o.hits[0].evidence)
        self.assertNotIn("/blog/", o.hits[0].evidence)
        wp = "User-agent: *\nDisallow: /wp-admin/\nAllow: /wp-admin/admin-ajax.php"
        self.assertEqual(ids(c.check_robots(wp)), [])
        self.assertEqual(ids(c.check_robots("Disallow: /wp-admin/\nDisallow: /staging/")),
                         ["robots-names-sensitive-areas"])
        self.assertEqual(ids(c.check_robots(None)), [])
        o = c.check_sitemap("<urlset><url><loc>https://e.com/backup/x</loc></url>"
                            "<url><loc>https://e.com/a</loc></url></urlset>")
        self.assertEqual(ids(o), ["sitemap-lists-sensitive-urls"])
        self.assertEqual(ids(c.check_sitemap(None)), [])

    def test_cookie_without_equals_is_unnamed(self):
        o = c.check_page(R([("Set-Cookie", "SECRETTOKEN; Secure"),
                            ("Set-Cookie", 'q="v; Secure"; Path=/')]))
        self.assertTrue(o.hits)
        for h in o.hits:
            self.assertNotIn("SECRETTOKEN", h.evidence)
        self.assertIn("(unnamed)", next(h.evidence for h in o.hits if h.check == "cookie-no-httponly"))

    def test_csp_default_src_only_when_no_script_src(self):
        ok = c.check_page(R([("Content-Security-Policy", "default-src 'self' 'unsafe-inline'; script-src 'self'")]))
        self.assertNotIn("weak-csp", ids(ok))
        ok = c.check_page(R([("Content-Security-Policy",
                              "default-src 'unsafe-inline'; script-src-elem 'self'")]))
        self.assertNotIn("weak-csp", ids(ok))
        bad = c.check_page(R([("Content-Security-Policy", "default-src 'self' 'unsafe-inline'")]))
        self.assertIn("weak-csp", ids(bad))

    def test_wp_admin_paths_are_exempt(self):
        for p in ("/wp-admin", "/wp-admin/", "/wp-admin/*", "/wp-admin/admin-ajax.php", "/wp-admin/admin/"):
            self.assertEqual(ids(c.check_robots("Disallow: " + p)), [], p)
        self.assertEqual(ids(c.check_robots("Disallow: /wp-admin-old/admin/")), ["robots-names-sensitive-areas"])

    def test_sensitive_words_match_whole_segments(self):
        quiet = ("/configurator/", "/badminton-club/", "/blog/backup-your-site", "/wp-admin-old/", "/admin-panel/",
                 "/wp-login.php", "/stages/", "/?page=login")
        loud = ("/admin/", "/staging/", "/config/", "/Admin/", "/login.php", "/backup.tar.gz", "/backups/",
                "/administrator/", "/stage/", "/configuration.php", "/shop/admin", "/admin*", "/login$")
        for path in quiet:
            with self.subTest(path=path):
                self.assertEqual(ids(c.check_robots("Disallow: " + path)), [])
                self.assertEqual(ids(c.check_sitemap("<loc>https://e.com%s</loc>" % path)), [])
        for path in loud:
            with self.subTest(path=path):
                self.assertEqual(ids(c.check_robots("Disallow: " + path)), ["robots-names-sensitive-areas"])
                self.assertEqual(ids(c.check_sitemap("<loc>https://e.com%s</loc>" % path)),
                                 ["sitemap-lists-sensitive-urls"])

    def test_security_txt(self):
        def txt(body, ctype="text/plain", status=200):
            return R([("Content-Type", ctype)], body, url="https://www.example.com/.well-known/security.txt",
                     status=status)
        good = "Contact: mailto:security@example.com\nExpires: 2027-01-01T00:00:00.000Z\n"
        self.assertEqual(c.check_security_txt(txt(good)).strengths, ["security-txt"])
        ok = c.check_security_txt(txt("# hi\ncontact: https://example.com/report", "text/plain; charset=utf-8"))
        self.assertEqual((ids(ok), ok.strengths), ([], ["security-txt"]))
        for resp, why in ((None, "could not be fetched"), (txt(good, status=404), "returned 404"),
                          (txt("<html><body>Shop</body></html>", "text/html"), "not plain text"),
                          (txt("Expires: 2027-01-01T00:00:00.000Z\n# Contact: none"), "no Contact line")):
            with self.subTest(why=why):
                o = c.check_security_txt(resp)
                self.assertEqual((ids(o), o.strengths), (["no-security-txt"], []))
                self.assertIn(why, o.hits[0].evidence)

    def test_catch_all_page_is_not_security_txt(self):
        page = R([("Content-Type", "text/html")], "<html><body>Contact: us</body></html>")
        self.assertEqual(ids(c.check_security_txt(page)), ["no-security-txt"])

    def test_directory_listing(self):
        o = c.check_directories({"/uploads/": R(body="<html><title>Index of /uploads</title>"),
                                 "/backup/": R(body="<title>Home</title>"), "/files/": None})
        self.assertEqual(ids(o), ["directory-listing"])
        self.assertIn("/uploads/", o.hits[0].evidence)
        self.assertEqual(ids(c.check_directories({"/a/": None})), [])

    def test_clean_page_strengths(self):
        o = c.check_page(R(GOOD + [("Set-Cookie", "a=1; Secure; HttpOnly; SameSite=Strict")], "<p>hi</p>"))
        self.assertEqual(ids(o), [])
        self.assertEqual(set(o.strengths), {"hsts-set", "csp-set", "cookies-flagged", "no-version-leaks"})

    def test_merge(self):
        good = R([("Content-Type", "text/plain")], "Contact: mailto:a@example.com")
        m = c.merge(c.check_security_txt(good), c.check_security_txt(good), c.check_security_txt(R(status=404)))
        self.assertEqual(m.strengths, ["security-txt"])
        self.assertEqual(ids(m), ["no-security-txt"])

    def test_ids_exist_and_evidence_short(self):
        long = "x" * 500
        outs = [
            c.check_page(R([("Server", "nginx/1.1 " + long), ("Set-Cookie", long + "=1"),
                            ("Referrer-Policy", "unsafe-url")],
                           '<meta name="generator" content="W 1.2 %s">' % long)),
            c.check_page(R(GOOD)),
            c.check_robots("Disallow: /admin/" + long),
            c.check_sitemap("<loc>https://e.com/admin/%s</loc>" % long),
            c.check_security_txt(R(status=404)),
            c.check_security_txt(R([("Content-Type", long)], "Contact: x")),
        ]
        for o in outs:
            for h in o.hits:
                self.assertIn(h.check, wording.CHECKS)
                self.assertLessEqual(len(h.evidence), 200)
            for s in o.strengths:
                self.assertIn(s, wording.STRENGTHS)


class UnansweredProbeTests(unittest.TestCase):
    P = fetch.ProbeResult
    BASE = {"": fetch.ProbeResult(404, "text/html", 10)}

    def results(self, n, none_count, first=None):
        res = {"/p%d" % i: self.P(404, "text/html", 10) for i in range(n)}
        for i in range(n - none_count, n):
            res["/p%d" % i] = None
        if first:
            res["/p0"] = first
        return res

    def note(self, u, n):
        return ("Exposed files: %d of %d addresses got no answer, possibly because the server started "
                "blocking the check, so they weren't checked." % (u, n))

    def test_unanswered_probes_are_not_checked(self):
        out = c.classify_probes(self.results(10, 2), self.BASE)
        self.assertEqual(out.not_checked, [(RUBRIC[0][0], self.note(2, 10))])
        self.assertIn("2 of 10", out.not_checked[0][1])
        self.assertNotIn("no-exposed-files", out.strengths)

    def test_all_unanswered(self):
        out = c.classify_probes(self.results(10, 10), self.BASE)
        self.assertIn("10 of 10", out.not_checked[0][1])
        self.assertEqual(out.hits, [])
        self.assertEqual(out.strengths, [])

    def test_all_answered_has_no_note(self):
        out = c.classify_probes(self.results(10, 0), self.BASE)
        self.assertEqual(out.not_checked, [])
        self.assertIn("no-exposed-files", out.strengths)

    def test_hits_among_answered_still_reported(self):
        out = c.classify_probes(self.results(10, 2, first=self.P(200, "text/plain", 20)), self.BASE)
        self.assertEqual(len(out.not_checked), 1)
        self.assertTrue(out.hits)

    def test_rate_limit_answers_count_as_no_answer(self):
        for status in (429, 503):
            with self.subTest(status=status):
                res = self.results(10, 0, first=self.P(200, "text/plain", 20))
                res["/p8"] = res["/p9"] = self.P(status, "text/html", 10)
                out = c.classify_probes(res, self.BASE)
                self.assertEqual(out.not_checked, [(RUBRIC[0][0], self.note(2, 10))])
                self.assertEqual(ids(out), ["exposed-info-files"])   # /p0 isn't on a list, so it counts as "info"
                self.assertNotIn("no-exposed-files", out.strengths)

    def cant_tell(self, k, n, statuses):
        return ("Exposed files: %d of %d addresses gave the same answer as an address that doesn't exist (%s), so "
                "the check couldn't tell whether they're there." % (k, n, statuses))

    def test_same_answer_as_a_missing_address_is_cant_tell(self):
        res = {"/.env": self.P(403, "text/html", 9), "/.git/HEAD": self.P(403, "text/html", 9),
               "/phpmyadmin/": self.P(401, "text/html", 9), "/x.php": self.P(301, "text/html", 0),
               "/.svn/entries": self.P(404, "text/html", 4)}
        base = {"": self.P(403, "text/html", 9), ".php": self.P(301, "text/html", 0)}
        out = c.classify_probes(res, base)
        self.assertEqual(out.not_checked, [(RUBRIC[0][0], self.cant_tell(3, 5, "301, 403"))])
        self.assertEqual(ids(out), ["exposed-admin-tools"])   # the admin 401 differs from its 403 baseline...
        self.assertEqual(out.strengths, [])
        out = c.classify_probes({"/phpmyadmin/": self.P(401, "text/html", 9)}, {"": self.P(401, "text/html", 9)})
        self.assertEqual(out.hits, [])                        # ...but a 401 everywhere tells nothing
        self.assertEqual(out.not_checked, [(RUBRIC[0][0], self.cant_tell(1, 1, "401"))])

    def test_nothing_open_needs_a_missing_page_answer(self):
        four = self.P(404, "text/html", 4)
        for status, strong in ((404, True), (410, True), (403, False), (301, False), (200, False)):
            with self.subTest(status=status):
                out = c.classify_probes({"/.env": four}, {"": self.P(status, "text/html", 4)})
                self.assertEqual("no-exposed-files" in out.strengths, strong)
                self.assertEqual(out.hits, [])

    def test_unanswered_baseline_falls_back_to_the_plain_one(self):
        page = self.P(200, "text/html", 1000)
        out = c.classify_probes({"/shell.php": page, "/.env": page}, {"": page, ".php": None})
        self.assertEqual(ids(out), ["exposed-unclear"])
        out = c.classify_probes({"/shell.php": page}, {"": page, ".php": self.P(429, "text/html", 5)})
        self.assertEqual(ids(out), ["exposed-unclear"])

    def test_no_usable_baseline_makes_every_200_unclear(self):
        page = self.P(200, "text/html", 1000)
        for base in ({"": None}, {"": None, ".php": None}, {"": self.P(503, "text/html", 5)}):
            with self.subTest(base=base):
                out = c.classify_probes({"/shell.php": page, "/.env": self.P(200, "text/plain", 20),
                                         "/adminer.php": page, "/.git/HEAD": self.P(404, "text/html", 4)}, base)
                self.assertEqual(ids(out), ["exposed-unclear"])
                self.assertEqual(out.strengths, [])
        out = c.classify_probes({"/.env": self.P(404, "text/html", 4)}, {"": None})
        self.assertEqual((out.hits, out.strengths), ([], []))


if __name__ == "__main__":
    unittest.main()
