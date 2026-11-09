"""Platform-aware file lists (scripts/security/paths.py, platform.py, checks.classify_probes): offline."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from security import checks as c  # noqa: E402
from security import fetch  # noqa: E402
from security.paths import (CORE_PATHS, KINDS, PHP_PLATFORMS, PLATFORM_NAMES, PLATFORM_PATHS,  # noqa: E402
                            SCRIPT_EXTENSIONS)
from security.platform import detect_platforms, select_paths  # noqa: E402

P = fetch.ProbeResult


def resp(headers=(), body="<html><body>Hi</body></html>"):
    return c.Response("https://example.com/", 200, list(headers), body)


class TestLists(unittest.TestCase):
    def test_lists_exact(self):
        self.assertEqual(len(CORE_PATHS), 48)
        self.assertEqual(sum(1 for _, k in CORE_PATHS if k == "secret"), 41)
        self.assertEqual(sum(1 for _, k in CORE_PATHS if k == "info"), 7)
        self.assertEqual(len(PLATFORM_PATHS["php"]), 29)
        everything = list(CORE_PATHS) + [e for v in PLATFORM_PATHS.values() for e in v]
        unique = {p for p, _ in everything}
        self.assertEqual(len(everything), 149)
        self.assertEqual(len(unique), 149)
        self.assertEqual(len(unique), len({e for e in everything}))   # a path never has two kinds
        for p, k in everything:
            self.assertIn(k, KINDS)
            self.assertTrue(p.startswith("/"), p)
        self.assertEqual(set(PLATFORM_NAMES), set(PLATFORM_PATHS))
        self.assertTrue(set(PHP_PLATFORMS) <= set(PLATFORM_PATHS))
        self.assertEqual(SCRIPT_EXTENSIONS, (".php", ".aspx", ".axd", ".jsp"))

    def test_select_paths(self):
        wp = select_paths(["php", "wordpress"])
        self.assertEqual(len(wp), 85)
        self.assertEqual(len({p for p, _ in wp}), 85)
        self.assertNotIn("/config/database.yml", [p for p, _ in wp])
        allp = select_paths([])
        self.assertEqual(len(allp), 149)
        self.assertEqual(len({p for p, _ in allp}), 149)
        self.assertEqual(select_paths(["php", "wordpress"])[:48], list(CORE_PATHS))


class TestDetect(unittest.TestCase):
    def test_detect_each_platform(self):
        def html(head="", body=""):
            return "<html><head>%s</head><body>%s</body></html>" % (head, body)
        cases = {
            "wordpress": [resp(body=html('<meta name="generator" content="WordPress 6.5">')),
                          resp(body=html('<script src="/wp-includes/js/x.js"></script>')),
                          resp([("Link", '<https://e.com/wp-json/>; rel="https://api.w.org/"')])],
            "drupal": [resp(body=html('<meta name="generator" content="Drupal 10">')),
                       resp([("X-Generator", "Drupal 10 (https://www.drupal.org)")]),
                       resp([("X-Drupal-Cache", "HIT")]),
                       resp(body=html(body='<img src="/sites/default/files/a.png">'))],
            "joomla": [resp(body=html('<meta name="generator" content="Joomla! - Open Source">')),
                       resp(body=html('<script src="/media/jui/js/jquery.min.js"></script>'))],
            "magento": [resp([("X-Magento-Cache-Debug", "HIT")]),
                        resp([("Set-Cookie", "mage-cache-sessid=true; path=/")]),
                        resp(body=html('<script src="/static/version1/x.js"></script>'))],
            "laravel": [resp([("Set-Cookie", "laravel_session=abc; path=/")])],
            "symfony": [resp([("X-Debug-Token", "abc")]), resp([("X-Debug-Token-Link", "/_profiler/abc")])],
            "craft": [resp([("X-Powered-By", "Craft CMS")]), resp([("Set-Cookie", "CraftSessionId=a")])],
            "php": [resp([("X-Powered-By", "PHP/8.3.36")]), resp([("Set-Cookie", "PHPSESSID=a")])],
            "node": [resp([("X-Powered-By", "Express")]), resp([("Set-Cookie", "connect.sid=a")]),
                     resp(body=html('<script src="/_next/static/a.js"></script>')),
                     resp(body=html('<meta name="generator" content="Ghost 5.0">'))],
            "python": [resp([("Set-Cookie", "csrftoken=a")]),
                       resp(body=html(body='<form><input type="hidden" name="csrfmiddlewaretoken" value="x"></form>')),
                       resp([("Server", "gunicorn/21.2")])],
            "rails": [resp(body=html('<meta name="csrf-param" content="authenticity_token">')),
                      resp([("X-Runtime", "0.012")]), resp([("Server", "nginx + Phusion Passenger 6")])],
            "java": [resp([("Set-Cookie", "JSESSIONID=a; Path=/")]), resp([("Server", "Apache-Coyote/1.1")]),
                     resp([("X-Powered-By", "Servlet/3.1")])],
            "dotnet": [resp([("X-Powered-By", "ASP.NET")]), resp([("X-AspNet-Version", "4.0")]),
                       resp([("Set-Cookie", ".AspNetCore.Session=a")]),
                       resp([("Set-Cookie", "ASP.NET_SessionId=a")]), resp([("Server", "Microsoft-IIS/10.0")]),
                       resp(body=html(body='<input type="hidden" name="__VIEWSTATE" value="x">'))],
            "static": [resp(body=html('<meta name="generator" content="Hugo 0.120">'))],
        }
        for key, responses in cases.items():
            for i, r in enumerate(responses):
                with self.subTest(key, i=i):
                    self.assertIn(key, detect_platforms(r))
        for key in PHP_PLATFORMS:
            self.assertIn("php", detect_platforms(cases[key][0]))
        self.assertEqual(detect_platforms(resp([("X-Powered-By", "PHP/8.3.36")],
                                               '<link href="/wp-content/themes/a.css" rel="stylesheet">')),
                         ["php", "wordpress"])

    def test_text_mentions_are_not_signals(self):
        page = resp(body="<html><body><p>We build WordPress and Django sites, with PHP, Laravel and "
                         "ASP.NET.</p></body></html>")
        self.assertEqual(detect_platforms(page), [])
        self.assertEqual(detect_platforms(resp()), [])

    def test_links_are_not_asset_signals(self):
        for href in ("/sites/default/files/report.pdf", "/wp-content/uploads/x.pdf", "/_next/x", "/media/jui/x"):
            with self.subTest(href):
                self.assertEqual(detect_platforms(resp(body='<a href="%s">x</a>' % href)), [])
        self.assertEqual(detect_platforms(resp(body='<link href="/wp-content/themes/x/style.css">')),
                         ["php", "wordpress"])
        self.assertEqual(detect_platforms(resp(body='<img src="/sites/default/files/a.png">')), ["drupal", "php"])

    def test_redirect_response_is_not_read(self):
        redirect = c.Response("https://example.com/", 301, [("X-Powered-By", "PHP/8.3")], "")
        self.assertEqual(detect_platforms(redirect), [])
        wp = c.Response("https://example.com/", 301, [("X-Powered-By", "PHP/8.3"),
                                                      ("X-Redirect-By", "WordPress")], "")
        self.assertEqual(detect_platforms(wp), ["php", "wordpress"])

    def test_express_is_a_word(self):
        self.assertEqual(detect_platforms(resp([("X-Powered-By", "ExpressionEngine")])), [])
        self.assertEqual(detect_platforms(resp([("X-Powered-By", "Express")])), ["node"])

    def test_cookie_value_is_not_read(self):
        self.assertEqual(detect_platforms(resp([("Set-Cookie", "sid=PHPSESSID; Path=/")])), [])


class TestClassify(unittest.TestCase):
    def test_admin_401_counts(self):
        out = c.classify_probes({"/phpmyadmin/": P(401, "text/html", 10), "/.env": P(401, "text/html", 10),
                                 "/adminer/": P(200, "text/html", 500)}, {"": P(404, "text/html", 5)})
        self.assertEqual([h.check for h in out.hits], ["exposed-admin-tools"])
        self.assertIn("/phpmyadmin/ 401", out.hits[0].evidence)
        self.assertIn("/adminer/ 200", out.hits[0].evidence)
        self.assertNotIn("/.env", out.hits[0].evidence)

    def test_admin_401_is_not_swallowed_by_a_200_baseline(self):
        out = c.classify_probes({"/phpmyadmin/": P(401, "text/html", 1000)}, {"": P(200, "text/html", 1000)})
        self.assertEqual([h.check for h in out.hits], ["exposed-admin-tools"])

    def test_backdoor_hit(self):
        out = c.classify_probes({"/shell.php": P(200, "text/html", 40), "/cmd.jsp": P(401, "text/html", 40)},
                                {"": P(404, "text/html", 5), ".php": P(404, "text/html", 5)})
        self.assertEqual([h.check for h in out.hits], ["possible-backdoor"])
        self.assertIn("/shell.php 200", out.hits[0].evidence)
        self.assertNotIn("/cmd.jsp", out.hits[0].evidence)

    def test_php_catch_all_is_unclear(self):
        baselines = {"": P(404, "text/html", 5), ".php": P(200, "text/html", 1000)}
        out = c.classify_probes({"/phpinfo.php": P(200, "text/html", 1010), "/shell.php": P(200, "text/html", 1000),
                                 "/.env": P(200, "text/html", 1000)}, baselines)
        checks = {h.check: h.evidence for h in out.hits}
        self.assertEqual(set(checks), {"exposed-unclear", "exposed-secrets"})
        self.assertIn("/phpinfo.php", checks["exposed-unclear"])
        self.assertIn("/shell.php", checks["exposed-unclear"])
        self.assertIn("/.env", checks["exposed-secrets"])
        self.assertNotIn("/.env", checks["exposed-unclear"])

    def test_missing_extension_baseline_falls_back_to_empty_key(self):
        out = c.classify_probes({"/x.php": P(200, "text/html", 1000)}, {"": P(200, "text/html", 1000)})
        self.assertEqual([h.check for h in out.hits], ["exposed-unclear"])


if __name__ == "__main__":
    unittest.main()
