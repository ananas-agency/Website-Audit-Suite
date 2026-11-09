"""Drafting the security page and rendering its text list (scripts/security/draft.py, text.py): offline."""
import copy
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from report import rules  # noqa: E402
from report.data import validate_dimension  # noqa: E402
from security import (DISCLAIMER_BODY, DISCLAIMER_EXTRA_TITLE, DISCLAIMER_HEADING, RUBRIC)  # noqa: E402
from security.checks import Hit, Outcome  # noqa: E402
from security.draft import draft_page  # noqa: E402
from security.text import render_text  # noqa: E402
from security.wording import CHECKS, STRENGTHS  # noqa: E402

SKIPPED = "Exposed files: not checked, because ownership wasn't confirmed."
FILES = RUBRIC[0][0]
EMAIL = RUBRIC[5][0]
HEADERS = RUBRIC[2][0]


def sample_outcome():
    return Outcome(
        hits=[Hit("no-referrer-policy", "Referrer-Policy: (missing)"),
              Hit("no-dmarc", "No `v=DMARC1` record at `_dmarc.example.com`."),
              Hit("exposed-info-files", "/package.json\n/composer.lock")],
        strengths=["https-valid"],
        not_checked=[(FILES, SKIPPED)],
    )


def rows(page):
    return {r["criterion"]: r["result"] for r in page["rubric"]}


class DraftTests(unittest.TestCase):
    def test_draft_is_valid_page(self):
        errors, _, findings = validate_dimension(draft_page(sample_outcome()), "security.json")
        self.assertEqual(errors, [])
        self.assertEqual(len(findings), 3)

    def test_page_shape(self):
        page = draft_page(sample_outcome())
        self.assertEqual(page["extra"], [{"title": DISCLAIMER_EXTRA_TITLE, "body": DISCLAIMER_BODY}])
        self.assertEqual(page["strengths"], [STRENGTHS["https-valid"]])
        self.assertEqual([f["key"] for f in page["findings"]],
                         [k for k in CHECKS if k in ("exposed-info-files", "no-referrer-policy", "no-dmarc")])
        self.assertTrue(all(f["measured"] for f in page["findings"]))
        self.assertEqual([r["criterion"] for r in page["rubric"]], [c for c, _ in RUBRIC])
        self.assertEqual(page["verdict"],
                         "3 security issues found, 1 of them high priority; 1 protection already in place.")

    def test_scope_adds_second_extra_block(self):
        self.assertEqual(len(draft_page(sample_outcome())["extra"]), 1)
        page = draft_page(sample_outcome(), "Recognised platform: WordPress, PHP. The file check looked at 85 "
                                            "well-known addresses.")
        self.assertEqual(page["extra"][1], {"title": "What the file check covered",
                                            "body": "Recognised platform: WordPress, PHP. The file check looked "
                                                    "at 85 well-known addresses."})
        self.assertEqual(validate_dimension(page, "security.json")[0], [])
        text = render_text(page, "https://example.com", "2026-11-09")
        self.assertLess(text.index("## What's working"), text.index("## What the file check covered"))
        self.assertLess(text.index("## What the file check covered"), text.index("## Not checked"))
        self.assertIn("The file check looked at 85 well-known addresses.", text)
        self.assertNotIn("## What the file check covered", render_text(draft_page(sample_outcome()), "u", "d"))

    def test_verdict_singular(self):
        page = draft_page(Outcome(hits=[Hit("no-dmarc", "x")]))
        self.assertEqual(page["verdict"],
                         "1 security issue found, 1 of them high priority; 0 protections already in place.")

    def test_rubric_rules(self):
        page = draft_page(Outcome(hits=[Hit("no-dmarc", "x"), Hit("no-referrer-policy", "y")]))
        r = rows(page)
        self.assertEqual(r[EMAIL], "Fail")          # impact 5
        self.assertEqual(r[HEADERS], "Partial")     # only low-impact hit
        self.assertEqual(r[FILES], "Pass")          # none

    def test_not_checked_files_is_partial_with_note(self):
        page = draft_page(Outcome(not_checked=[(FILES, SKIPPED)]))
        self.assertEqual(rows(page)[FILES], "Partial")
        self.assertEqual(page["notes"], SKIPPED)
        self.assertEqual(len(page["rubric"]), len(RUBRIC))

    def test_not_checked_with_low_impact_finding_is_partial(self):
        page = draft_page(Outcome(hits=[Hit("exposed-info-files", "/package.json")], not_checked=[(FILES, "n")]))
        self.assertEqual(rows(page)[FILES], "Partial")

    def test_hit_seen_before_block_still_fails(self):
        note = "Exposed files: 2 of 10 addresses got no answer, possibly because the server started blocking the check, so they weren't checked."
        page = draft_page(Outcome(hits=[Hit("exposed-secrets", "/.env")], not_checked=[(FILES, note)]))
        self.assertEqual(rows(page)[FILES], "Fail")
        self.assertIn(note, page["notes"])

    def test_no_strengths_gets_honest_line(self):
        page = draft_page(Outcome(hits=[Hit("no-dmarc", "x")]))
        self.assertEqual(page["strengths"],
                         ["Nothing on this list was already in place, so the findings below are the place to start."])
        self.assertEqual(validate_dimension(page, "security.json")[0], [])
        self.assertIn(page["strengths"][0], render_text(page, "u", "d"))

    def test_no_notes_key_when_empty(self):
        self.assertNotIn("notes", draft_page(Outcome()))

    def test_duplicate_hit_keeps_first_and_strengths_dedupe(self):
        page = draft_page(Outcome(hits=[Hit("no-dmarc", "first"), Hit("no-dmarc", "second")],
                                  strengths=["hsts-set", "https-valid", "hsts-set"]))
        self.assertEqual([f["evidence"] for f in page["findings"]], ["first"])
        self.assertEqual(page["strengths"], [STRENGTHS["https-valid"], STRENGTHS["hsts-set"]])


class TextTests(unittest.TestCase):
    def setUp(self):
        self.page = draft_page(sample_outcome())
        self.text = render_text(self.page, "https://example.com", "2026-11-08")

    def test_text_starts_with_disclaimer(self):
        lines = self.text.split("\n")
        self.assertEqual(lines[0], "# Security check: https://example.com (2026-11-08)")
        paras = DISCLAIMER_BODY.split("\n\n")
        expect = [f"> **{DISCLAIMER_HEADING}**", ">"]
        for i, p in enumerate(paras):
            expect += ["> " + p] + ([">"] if i < len(paras) - 1 else [])
        pos = [i for i, l in enumerate(lines) if l.startswith(">")]
        self.assertEqual([lines[i] for i in pos], expect)
        self.assertEqual(pos[0], 2)

    def test_text_order_and_ids(self):
        t = self.text
        i1 = t.index("### SEC-01 ")
        i2 = t.index("### SEC-02 ")
        i3 = t.index("### SEC-03 ")
        self.assertLess(t.index(CHECKS["no-dmarc"].title), t.index(CHECKS["exposed-info-files"].title))
        self.assertLess(t.index(CHECKS["exposed-info-files"].title), t.index(CHECKS["no-referrer-policy"].title))
        self.assertTrue(i1 < i2 < i3)
        c = CHECKS["no-dmarc"]
        self.assertIn(f"### SEC-01 🔴 HIGH · Quick win: {c.title}\n"
                      f"*In plain words:* {c.issue}\n\n"
                      f"*Why you should care:* {c.impact_text}\n\n"
                      f"*For your developer:* Seen: No `v=DMARC1` record at `_dmarc.example.com`. {c.fix}", t)
        self.assertIn("🟠 MEDIUM · Quick win", t)
        self.assertIn("🟢 LOW · Fill-in", t)

    def test_multiline_evidence_in_code_block(self):
        c = CHECKS["exposed-info-files"]
        self.assertIn("*For your developer:* Seen:\n```\n/package.json\n/composer.lock\n```\n\n" + c.fix, self.text)

    def test_labelled_parts_are_separate_paragraphs(self):
        lines = self.text.splitlines()
        labels = ("*In plain words:*", "*Why you should care:*", "*For your developer:*")
        labelled = [i for i, line in enumerate(lines) if line.startswith(labels)]
        self.assertEqual(len(labelled), 9)
        for i in labelled:
            if not lines[i].startswith(labels[0]):
                self.assertEqual(lines[i - 1], "", lines[i])  # never glued to the line above

    def test_inline_evidence_in_backticks(self):
        self.assertIn("*For your developer:* Seen: `Referrer-Policy: (missing)`. " + CHECKS["no-referrer-policy"].fix,
                      self.text)

    def test_sections(self):
        t = self.text
        self.assertIn("## What's working\n", t)
        self.assertIn("- " + STRENGTHS["https-valid"], t)
        self.assertIn("## Not checked\n", t)
        self.assertIn("- " + SKIPPED, t)
        self.assertLess(t.index("## What's working"), t.index("## Not checked"))
        self.assertLess(t.index("## Not checked"), t.index("## Findings"))
        clean = render_text(draft_page(Outcome(strengths=["https-valid"])), "u", "d")
        self.assertNotIn("## Not checked", clean)

    def test_grade_from_builder_rules(self):
        _, rubric, _ = validate_dimension(self.page, "security.json")
        score = rules.score_rubric(rubric)[1]
        letter = rules.grade(score)[0]
        self.assertIn(f"**Grade: {letter} ({score}/100)**", self.text)
        self.assertIn(self.page["verdict"], self.text)

    def test_edited_page_rerenders(self):
        page = copy.deepcopy(self.page)
        for f in page["findings"]:
            if f["key"] == "no-referrer-policy":
                f["impact"] = 5
                f["effort"] = 1
        t = render_text(page, "u", "d")
        self.assertLess(t.index(CHECKS["no-referrer-policy"].title), t.index(CHECKS["exposed-info-files"].title))
        self.assertIn("### SEC-01 🔴 HIGH", t)

    def test_invalid_page_raises(self):
        page = copy.deepcopy(self.page)
        page["verdict"] = ""
        with self.assertRaises(ValueError):
            render_text(page, "u", "d")


if __name__ == "__main__":
    unittest.main()
