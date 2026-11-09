"""The security step's constants, disclaimer and copy table (scripts/security/)."""
import dataclasses
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
import security as sec  # noqa: E402
from security import wording  # noqa: E402
from security.paths import CORE_PATHS  # noqa: E402

SPEC = REPO / "docs" / "superpowers" / "specs" / "2026-11-07-security-step-design.md"


def _spec_lines() -> list:
    return SPEC.read_text(encoding="utf-8").splitlines()


def _quote_after(marker: str) -> list:
    """The first blockquote after the line starting with `marker`: its raw lines ('> …' or a bare '>')."""
    lines = _spec_lines()
    start = next(i for i, line in enumerate(lines) if line.startswith(marker))
    quote = []
    for line in lines[start + 1:]:
        if line == ">" or line.startswith("> "):
            quote.append(line)
        elif quote:
            break
    return quote


def spec_disclaimer() -> tuple:
    """(heading, body) from the blockquote in spec §3.1.

    The first line's bold text is the heading. The rest splits into paragraphs at bare '>' lines; a
    paragraph's wrapped lines are joined with one space, and the paragraphs with a blank line.
    """
    first, *rest = _quote_after("### 3.1")
    heading = first[2:]
    assert heading.startswith("**") and heading.endswith("**"), heading
    paragraphs, current = [], []
    for line in rest + [">"]:
        if line == ">":
            if current:
                paragraphs.append(" ".join(current))
            current = []
        else:
            current.append(line[2:])
    return heading[2:-2], "\n\n".join(paragraphs)


def spec_voice_sample() -> dict:
    """The four parts of the confirmed voice sample in spec §6.3, wrapped lines joined with spaces."""
    text = " ".join(line[2:] for line in _quote_after("Confirmed voice sample"))
    m = re.fullmatch(r"\*\*🔴 HIGH — (?P<title>.+?)\*\* \*In plain words:\* (?P<issue>.+?) "
                     r"\*Why you should care:\* (?P<impact_text>.+?) \*For your developer:\* (?P<dev>.+)", text)
    assert m, text
    return m.groupdict()


def spec_rubric() -> tuple:
    """((criterion, weight), ...) from the weights table in spec §6.6, bold markers removed."""
    lines = _spec_lines()
    start = next(i for i, line in enumerate(lines) if line.startswith("### 6.6"))
    rows = []
    for line in lines[start + 1:]:
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells[1].isdigit():
                rows.append((cells[0].replace("**", ""), int(cells[1])))
        elif rows:
            break
    return tuple(rows)


ROWS = {
    "Files": "No sensitive files/paths exposed",
    "HTTPS": "HTTPS & TLS (version, cert validity, HSTS)",
    "Headers": "Security headers present and strong",
    "Info": "No information disclosure (version/listing/mixed content)",
    "Cookies": "Cookie flags (Secure/HttpOnly/SameSite)",
    "Email": "Email/domain spoofing protection (SPF/DMARC)",
    "Forms": "Forms sent over HTTPS",
    "—": None,
}

# The agreed default ratings for every check: check id -> (row, impact, effort), in order.
PLAN_TABLE = {
    "exposed-secrets": ("Files", 5, 1),
    "exposed-info-files": ("Files", 3, 1),
    "exposed-admin-tools": ("Files", 4, 1),
    "possible-backdoor": ("Files", 5, 2),
    "exposed-unclear": ("Files", 2, 1),
    "no-https": ("HTTPS", 5, 3),
    "no-https-redirect": ("HTTPS", 4, 1),
    "old-tls": ("HTTPS", 3, 2),
    "cert-expired": ("HTTPS", 5, 1),
    "cert-expiring": ("HTTPS", 4, 1),
    "cert-name-mismatch": ("HTTPS", 5, 2),
    "cert-untrusted": ("HTTPS", 5, 2),
    "no-hsts": ("HTTPS", 3, 1),
    "hsts-weak": ("HTTPS", 2, 1),
    "no-csp": ("Headers", 3, 3),
    "weak-csp": ("Headers", 2, 3),
    "no-frame-protection": ("Headers", 3, 1),
    "no-nosniff": ("Headers", 2, 1),
    "no-referrer-policy": ("Headers", 1, 1),
    "unsafe-referrer-policy": ("Headers", 2, 1),
    "no-permissions-policy": ("Headers", 1, 1),
    "no-cross-origin-policies": ("Headers", 1, 2),
    "outdated-xss-header": ("Headers", 1, 1),
    "server-version": ("Info", 2, 1),
    "generator-version": ("Info", 2, 1),
    "directory-listing": ("Info", 4, 1),
    "mixed-content": ("Info", 3, 2),
    "robots-names-sensitive-areas": ("Info", 2, 1),
    "sitemap-lists-sensitive-urls": ("Info", 2, 1),
    "cookie-no-secure": ("Cookies", 3, 1),
    "cookie-no-httponly": ("Cookies", 3, 1),
    "cookie-no-samesite": ("Cookies", 2, 1),
    "cookie-broad-domain": ("Cookies", 2, 1),
    "no-spf": ("Email", 4, 1),
    "weak-spf": ("Email", 3, 1),
    "no-dmarc": ("Email", 5, 1),
    "dmarc-monitor-only": ("Email", 3, 2),
    "form-over-http": ("Forms", 5, 2),
    "password-over-http": ("Forms", 5, 2),
    "no-security-txt": ("—", 1, 1),
}

STRENGTH_IDS = ("https-valid", "hsts-set", "csp-set", "no-exposed-files", "email-protected",
                "security-txt", "cookies-flagged", "no-version-leaks")

EXPOSED = {
    "secret": ("/.git/HEAD", "/.git/config", "/.git-credentials", "/.svn/entries", "/.hg/hgrc",
               "/.env", "/.env.local", "/.env.production", "/.env.development", "/.env.backup", "/.env.save",
               "/.htpasswd", "/.htaccess", "/web.config",
               "/.aws/credentials", "/.ssh/id_rsa", "/id_rsa", "/.bash_history",
               "/sftp-config.json", "/.vscode/sftp.json", "/.ftpconfig",
               "/docker-compose.yml", "/docker-compose.override.yml",
               "/backup.zip", "/backup.tar.gz", "/backup.sql", "/backup.sql.gz", "/database.sql",
               "/database.sql.gz", "/db.sql", "/db.sql.gz", "/dump.sql", "/site.zip", "/site.tar.gz", "/www.zip",
               "/error_log", "/error.log", "/debug.log", "/logs/error.log",
               "/server-status", "/server-info"),
    "info": ("/.DS_Store", "/Thumbs.db", "/.idea/workspace.xml", "/swagger-ui.html", "/swagger.json",
             "/openapi.json", "/api-docs"),
}

# Words a non-technical owner shouldn't meet in "In plain words" / "Why you should care".
# Header and attribute names match case-insensitively; acronyms match as whole words.
JARGON_NAMES = ("Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options",
                "Referrer-Policy", "Permissions-Policy", "Cross-Origin", "X-XSS-Protection", "X-Powered-By",
                "X-AspNet", "Set-Cookie", "frame-ancestors", "nosniff", "SameSite", "HttpOnly", "max-age",
                "includeSubDomains", "unsafe-inline", "unsafe-eval", "p=none", "header", ".txt", ".xml", "`")
JARGON_ACRONYMS = ("CSP", "HSTS", "TLS", "SSL", "SPF", "DMARC", "DKIM", "DNS", "COOP", "COEP", "CORP", "XSS",
                   "CSRF", "MIME", "PCI", "CDN", "API", "URL", "HTTP", "TXT", "RFC", "CMS")
# report-format.md, "Write like a human": banned vocabulary and stock phrases.
BANNED = ("leverage", "delve", "robust", "seamless", "elevate", "unlock", "empower", "transformative",
          "cutting-edge", "myriad", "paradigm", "boasts", "foster", "streamline", "harness", "holistic",
          "at its core", "when it comes to", "in the realm of", "navigate the", "worth noting",
          "important to note", "here's the thing", "in conclusion", "at the end of the day", "the bottom line")


def _copy(check) -> tuple:
    return (check.title, check.issue, check.impact_text, check.fix)


# The design document is kept locally by the maintainers and isn't published, so the checks that compare
# the code with it only run where it exists. Every other check below always runs.
needs_spec = unittest.skipUnless(SPEC.exists(), "the design document is kept locally, not published")


class WordingTest(unittest.TestCase):
    @needs_spec
    def test_disclaimer_matches_spec(self):
        self.assertEqual((sec.DISCLAIMER_HEADING, sec.DISCLAIMER_BODY), spec_disclaimer())

    def test_disclaimer_shape(self):
        paragraphs = sec.DISCLAIMER_BODY.split("\n\n")
        self.assertEqual(len(paragraphs), 3)
        for p in paragraphs:
            self.assertNotIn("\n", p, "line break inside a paragraph")
        # Owner decision 2026-11-09: the list's size depends on the platform, so the disclaimer names no number.
        self.assertIn("It also looks up a list of well-known addresses where sensitive files sometimes get left "
                      "by mistake.", sec.DISCLAIMER_BODY)
        self.assertIsNone(re.search(r"\d", sec.DISCLAIMER_BODY), "a number in the disclaimer")

    def test_fixed_strings(self):
        self.assertEqual(sec.DISCLAIMER_HEADING, "Before we start: what this security check does and doesn't do")
        self.assertEqual(sec.DISCLAIMER_EXTRA_TITLE, "What this check does and doesn't do")
        self.assertEqual(sec.OWNERSHIP_QUESTION, "Is this your site, or are you authorised to audit it?")
        self.assertEqual(sec.USER_AGENT, "WebsiteAuditSuite-SecurityCheck/1.0 (+https://ananas-agency.com)")
        self.assertEqual(sec.DIRECTORY_PATHS, ("/wp-content/uploads/", "/uploads/", "/images/"))

    @needs_spec
    def test_rubric_matches_spec(self):
        self.assertEqual(sec.RUBRIC, spec_rubric())

    def test_rubric_rows_and_sum(self):
        self.assertEqual(tuple(name for name, _ in sec.RUBRIC), tuple(v for v in ROWS.values() if v))
        self.assertEqual(sum(w for _, w in sec.RUBRIC), 100)

    def test_every_check_complete(self):
        names = {name for name, _ in sec.RUBRIC}
        self.assertEqual(len(wording.CHECKS), 40)
        for cid, check in wording.CHECKS.items():
            with self.subTest(cid):
                self.assertIsInstance(check, wording.Check)
                self.assertTrue(check.criterion is None or check.criterion in names, check.criterion)
                self.assertIn(check.impact, range(1, 6))
                self.assertIn(check.effort, range(1, 6))
                for text in _copy(check):
                    self.assertIsInstance(text, str)
                    self.assertTrue(text.strip(), "empty text")
                    self.assertEqual(text, text.strip(), "stray whitespace")
        with self.assertRaises(dataclasses.FrozenInstanceError):
            wording.CHECKS["no-dmarc"].impact = 1

    def test_ratings_match_plan_table(self):
        self.assertEqual(list(wording.CHECKS), list(PLAN_TABLE))
        got = {cid: (c.criterion, c.impact, c.effort) for cid, c in wording.CHECKS.items()}
        want = {cid: (ROWS[row], i, e) for cid, (row, i, e) in PLAN_TABLE.items()}
        self.assertEqual(got, want)

    @needs_spec
    def test_no_dmarc_uses_spec_voice_sample(self):
        sample = spec_voice_sample()
        c = wording.CHECKS["no-dmarc"]
        self.assertEqual(c.title, sample["title"])
        self.assertEqual(c.issue, sample["issue"])
        self.assertEqual(c.impact_text, sample["impact_text"])
        # The sample's developer line is evidence + fix; the scanner supplies the evidence part.
        self.assertTrue(sample["dev"].endswith(" " + c.fix), sample["dev"])

    def test_no_dmarc_title_and_fix(self):
        c = wording.CHECKS["no-dmarc"]
        self.assertEqual(c.title, "Anyone can send email pretending to be your domain (no DMARC)")
        self.assertEqual(c.fix, "Publish DMARC (start `p=none`).")

    def test_backdoor_copy_never_claims_a_hack(self):
        # A harmless file can share a backdoor's name: the owner hears "check it", never "hacked".
        # The bare word catches every phrasing: was, has been, is, may have been, got hacked.
        c = wording.CHECKS["possible-backdoor"]
        for field in ("title", "issue", "impact_text"):
            self.assertNotRegex(getattr(c, field), r"(?i)\bhacked\b", field)

    def test_paths_fixed(self):
        # The core list is fixed word for word here; the platform lists are checked in test_security_paths.py.
        self.assertEqual(len(CORE_PATHS), 48)
        for kind, paths in EXPOSED.items():
            self.assertEqual(tuple(p for p, k in CORE_PATHS if k == kind), paths, kind)

    def test_strengths(self):
        self.assertEqual(set(wording.STRENGTHS), set(STRENGTH_IDS))
        for sid, text in wording.STRENGTHS.items():
            with self.subTest(sid):
                self.assertTrue(text.strip())
                self.assertTrue(text.endswith("."), text)

    def test_copy_is_plain(self):
        words = 0
        dashes = 0
        acronyms = re.compile(r"\b(%s)\b" % "|".join(JARGON_ACRONYMS))
        for cid, check in wording.CHECKS.items():
            texts = _copy(check)
            words += sum(len(t.split()) for t in texts)
            dashes += sum(t.count("—") for t in texts)
            with self.subTest(cid):
                self.assertLessEqual(sum(t.count("—") for t in texts), 1, "more than one em-dash")
                for field in ("issue", "impact_text"):
                    text = getattr(check, field)
                    for name in JARGON_NAMES:
                        self.assertNotIn(name.lower(), text.lower(), f"{field}: {name}")
                    self.assertIsNone(acronyms.search(text), f"{field}: {text}")
                for text in texts:
                    for phrase in BANNED:
                        self.assertNotIn(phrase, text.lower())
        for sid, text in wording.STRENGTHS.items():
            with self.subTest(sid):
                self.assertNotIn("—", text)
                self.assertIsNone(acronyms.search(text), text)
                for phrase in BANNED:
                    self.assertNotIn(phrase, text.lower())
        self.assertLessEqual(dashes, max(1, words // 150), f"{dashes} em-dashes in {words} words")


if __name__ == "__main__":
    unittest.main()
