"""The Security skill's files: the disclaimer and question order, the commands and the rubric table."""
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
from helpers import REPO  # noqa: E402
from security import DISCLAIMER_BODY, DISCLAIMER_HEADING, OWNERSHIP_QUESTION, RUBRIC  # noqa: E402

SKILL = REPO / "8 Security" / "security"
SKILL_MD = (SKILL / "SKILL.md").read_text(encoding="utf-8") if (SKILL / "SKILL.md").is_file() else ""
RULES = SKILL / "references" / "rules-security.md"
COMMAND = 'python "${CLAUDE_PLUGIN_ROOT}'


class SecuritySkillTest(unittest.TestCase):
    def test_skill_shows_disclaimer_verbatim(self):
        first_command = SKILL_MD.find(COMMAND)
        self.assertGreater(first_command, 0)
        self.assertIn(DISCLAIMER_HEADING, SKILL_MD[:first_command])
        for paragraph in DISCLAIMER_BODY.split("\n\n"):
            flat = re.sub(r"\n> ?", " ", SKILL_MD[:first_command])
            self.assertIn(paragraph, flat)

    def test_skill_asks_ownership_before_probe(self):
        self.assertIn(OWNERSHIP_QUESTION, SKILL_MD)
        self.assertLess(SKILL_MD.index(OWNERSHIP_QUESTION), SKILL_MD.index("--probe-files"))

    def test_skill_warns_before_ownership_question(self):
        warning = ("Some hosting firewalls block a computer that asks for many missing pages, so this computer "
                   "may be blocked from the site for a while after the file check. If that would be a problem, "
                   "ask your host to allow your IP address first.")
        flat = re.sub(r"\n> ?", " ", SKILL_MD)
        self.assertIn(warning, flat)
        self.assertLess(flat.index(warning), flat.index(OWNERSHIP_QUESTION))

    def test_skill_review_step_matches_draft_rule(self):
        rule = ("`Fail` if any finding in the row has impact 4 or more, even when the row wasn't fully checked; "
                "otherwise `Partial` if the row wasn't fully checked or has any finding; otherwise `Pass`.")
        for name, text in (("SKILL.md", SKILL_MD), ("rules-security.md", RULES.read_text(encoding="utf-8"))):
            with self.subTest(name):
                flat = re.sub(r"\s+", " ", text)
                self.assertIn(rule, flat)
                self.assertNotIn("Rows for checks that didn't run stay", flat)
                self.assertNotIn("couldn't run stays `Partial`", flat)

    def test_skill_prepares_for_a_long_file_check(self):
        flat = re.sub(r"\s+", " ", SKILL_MD)
        probe_run = flat.index('--probe-files --out "audit-<slug>"')
        for text in ("about 3 to 12 minutes for a WordPress site and up to about 20 for a site whose platform "
                     "isn't recognised, because it waits 2 seconds between addresses plus however long the "
                     "server takes to answer",
                     "Run it in the background, or with the longest timeout the shell tool allows."):
            self.assertIn(text, flat)
            self.assertLess(flat.index(text), probe_run)
        self.assertIn("If it times out, never run it again without asking the user: a second run doubles the "
                      "load that trips hosting firewalls.", flat)
        self.assertIn("On **exit 2** the address isn't a valid URL: fix it and run the command once more.", flat)

    def test_review_step_guards(self):
        flat = re.sub(r"\s+", " ", SKILL_MD)
        review = flat[flat.index("### Step 5"):flat.index("### Step 6")]
        for guard in ("Never add a strength.",
                      "Never remove or soften a not-checked note in `notes`.",
                      "Never say in the `verdict` that the site is secure.",
                      "Never delete a finding. When a finding is demonstrably wrong for this site, lower its "
                      "`impact` to 1 and say why in the plain-words line (`issue`)."):
            self.assertIn(guard, review)

    def test_rules_warn_about_windows_certificates(self):
        flat = re.sub(r"\s+", " ", RULES.read_text(encoding="utf-8"))
        self.assertIn("On Windows, Python can lack root certificates that a browser has, so confirm a "
                      "`cert-untrusted` warning in a browser before keeping it HIGH.", flat)

    def test_slug_follows_the_data_format(self):
        flat = re.sub(r"\s+", " ", SKILL_MD)
        fmt = re.sub(r"\s+", " ", (REPO / "audit-data-format.md").read_text(encoding="utf-8"))
        self.assertIn("`<slug>` is the first label of the site's domain", fmt)
        self.assertIn("the slug is the first label of the site's domain", flat)
        self.assertIn("(`https://www.ananas-agency.com` becomes `audit-ananas-agency`)", flat)
        self.assertNotIn("ananas-agency-com", flat)
        self.assertNotIn("dots replaced by hyphens", flat)

    def test_skill_commands(self):
        for name in ("security-scan.py", "security-report.py"):
            self.assertIn(f'python "${{CLAUDE_PLUGIN_ROOT}}/scripts/{name}"', SKILL_MD)
        self.assertIsNone(re.search(r"python3? \$\{CLAUDE_PLUGIN_ROOT\}", SKILL_MD))

    def test_rules_file_rubric_matches_constants(self):
        text = RULES.read_text(encoding="utf-8")
        for criterion, weight in RUBRIC:
            self.assertRegex(text, r"\|\s*%s\s*\|\s*%d\s*\|" % (re.escape(criterion), weight))


if __name__ == "__main__":
    unittest.main()
