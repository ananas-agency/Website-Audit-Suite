"""The skills hand their results to the report builder through audit-data-format.md."""
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from report.data import load_run  # noqa: E402

FORMAT_DOC = REPO / "audit-data-format.md"

# Section heading -> the file its json example is written to.
SECTION_FILES = {
    "audit.json": "audit.json",
    "site-snapshot.json": "site-snapshot.json",
    "goals.json": "goals.json",
    "Dimension files": "messaging.json",
    "action-report.json": "action-report.json",
}


def json_blocks_by_section(text: str) -> dict:
    blocks = {}
    for part in re.split(r"(?m)^## ", text)[1:]:
        heading, _, body = part.partition("\n")
        found = re.findall(r"```json\n(.*?)```", body, flags=re.S)
        if found:
            blocks[heading.strip()] = found
    return blocks


class FormatDocTest(unittest.TestCase):
    def test_format_doc_examples_validate(self):
        blocks = json_blocks_by_section(FORMAT_DOC.read_text(encoding="utf-8"))
        self.assertEqual(sorted(blocks), sorted(SECTION_FILES))
        with tempfile.TemporaryDirectory() as tmp:
            run = pathlib.Path(tmp) / "audit-demo"
            data = run / "audit-data"
            data.mkdir(parents=True)
            for heading, fname in SECTION_FILES.items():
                self.assertEqual(len(blocks[heading]), 1, heading)
                json.loads(blocks[heading][0])
                (data / fname).write_text(blocks[heading][0], encoding="utf-8")
            load_run(run)
            done = subprocess.run([sys.executable, str(REPO / "scripts" / "build-report.py"), str(run), "--final"],
                                  capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("TBD left: Site & business / Platform / CMS", done.stdout)  # the example's TBD value

    def test_format_doc_states_text_rules(self):
        text = FORMAT_DOC.read_text(encoding="utf-8").lower()
        for phrase in ("no html", "[[key]]", "never type an id"):
            self.assertIn(phrase, text)

    def test_format_doc_has_expected_headings(self):
        text = FORMAT_DOC.read_text(encoding="utf-8")
        for h in ("The run folder", "Writing text", "audit.json", "site-snapshot.json", "goals.json",
                  "Dimension files", "action-report.json", "Building"):
            self.assertIn(f"\n## {h}\n", text)

    def test_building_says_final_writes_every_page_with_data(self):
        text = FORMAT_DOC.read_text(encoding="utf-8")
        self.assertIn("writes every page that has data", text)

    def test_format_doc_size(self):
        self.assertLess(len(FORMAT_DOC.read_bytes()), 9000)


class ReportFormatTest(unittest.TestCase):
    def test_priority_rule_text(self):
        fmt = (REPO / "report-format.md").read_text(encoding="utf-8")
        rules = (REPO / "7 Action Report" / "action-report" / "references"
                 / "rules-action-report.md").read_text(encoding="utf-8")
        self.assertIn("High = 3–5", fmt)
        self.assertIn("(3–5)", fmt)
        for text in (fmt, rules):
            self.assertNotIn("High = 4–5", text)
            self.assertNotIn("(4–5)", text)

    def test_report_format_size(self):
        self.assertLess(len((REPO / "report-format.md").read_bytes()), 18000)


STYLE_CSS = (REPO / "scripts" / "report" / "style.css").read_text(encoding="utf-8")
STYLE_CLASSES = set(re.findall(r"\.([A-Za-z_][\w-]*)", STYLE_CSS))
RULES_FILES = sorted(REPO.glob("[0-8] */*/references/rules-*.md"))


class RulesFilesTest(unittest.TestCase):
    def test_rules_files_have_no_output_templates(self):
        self.assertEqual(len(RULES_FILES), 9)
        for path in RULES_FILES:
            text = path.read_text(encoding="utf-8")
            for banned in ("```html", "<style>", "## Output file format"):
                self.assertNotIn(banned, text, f"{path.name} still contains {banned!r}")
            # A worked example may quote an element as evidence (CRO-03's <a class="btn">);
            # page markup uses the stylesheet's classes.
            for attr in re.findall(r'class="([^"]*)"', text):
                used = STYLE_CLASSES & set(attr.split())
                self.assertFalse(used, f"{path.name} still contains page markup: class={attr!r}")

    def test_rules_files_total_size(self):
        total = sum(len(p.read_bytes()) for p in RULES_FILES)
        self.assertLess(total, 110000)

    def test_no_old_pip_line(self):
        old = "pip install playwright && playwright install chromium"
        # test-runs/, misc/ and website/ are git-ignored local data (test-runs holds old-version run copies).
        skip = {"claude-app", "docs", "tests", ".superpowers", ".git", "test-runs", "misc", "website"}
        hits = []
        for pattern in ("*.md", "*.py"):
            for path in REPO.rglob(pattern):
                rel = path.relative_to(REPO)
                if skip & set(rel.parts):
                    continue
                # The setup check is the one place that legitimately shows the install commands.
                if rel.as_posix() == "scripts/setup-check.py":
                    continue
                if old in path.read_text(encoding="utf-8"):
                    hits.append(str(rel))
        self.assertEqual(hits, [])

    def test_scan_scripts_point_at_the_setup_check(self):
        for path in sorted((REPO / "scripts").glob("*.py")):
            if path.name == "setup-check.py":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"pip\s+install\s+playwright", text), path.name)
            if "Playwright not installed" in text:
                self.assertIn("python scripts/setup-check.py", text, path.name)


PAGE_SKILLS = {
    "site-snapshot": "0 Site Snapshot/site-snapshot",
    "goals": "1 Goals Discovery/goals-discovery",
    "messaging": "2 Messaging Clarity/messaging-clarity",
    "conversion": "3 Conversion CRO/conversion-cro",
    "seo": "4 SEO Content/seo-content",
    "ux-technical": "5 UX Technical/ux-technical",
    "design": "6 Design Visual/design-visual",
}


def skill_text(folder: str) -> str:
    return (REPO / folder / "SKILL.md").read_text(encoding="utf-8")


class PageSkillsBuilderTest(unittest.TestCase):
    def test_every_page_skill_runs_the_builder(self):
        for page, folder in PAGE_SKILLS.items():
            text = skill_text(folder)
            self.assertIn('scripts/build-report.py"', text, page)
            self.assertIn(f"--page {page}", text, page)

    def test_every_page_skill_creates_audit_json_if_missing(self):
        for page, folder in PAGE_SKILLS.items():
            self.assertIn("audit.json", skill_text(folder), page)

    def test_builder_commands_quote_paths_and_use_run_folder(self):
        pattern = re.compile(r'python3? "\$\{CLAUDE_PLUGIN_ROOT\}/scripts/build-report\.py" "audit-<slug>" '
                             r'--(page [a-z-]+|final)')
        for page, folder in PAGE_SKILLS.items():
            lines = [ln for ln in skill_text(folder).splitlines() if "build-report.py" in ln]
            self.assertTrue(lines, page)
            for ln in lines:
                self.assertRegex(ln, pattern, page)

    def test_page_skills_link_format_doc(self):
        for page, folder in PAGE_SKILLS.items():
            self.assertIn("../../audit-data-format.md", skill_text(folder), page)

    def test_skills_no_longer_assemble_report(self):
        for page, folder in PAGE_SKILLS.items():
            self.assertNotIn("Add to the Website Audit Report", skill_text(folder), page)

    def test_scans_write_into_the_run_folder(self):
        for page, folder in PAGE_SKILLS.items():
            self.assertNotIn("--out <folder>", skill_text(folder), page)
        for path in RULES_FILES:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("--out <folder>", text, path.name)
            self.assertNotIn("--out out", text, path.name)
            for line in text.splitlines():
                if re.search(r"python3? \S*scripts/\S+-(scan|audit|sweep)\.py", line):
                    self.assertIn('--out "audit-<slug>"', line, f"{path.name}: {line}")

    def test_goals_launches_all_six_scans_into_the_run_folder(self):
        text = skill_text(PAGE_SKILLS["goals"])
        for scan in ("perf-a11y-scan.py", "mobile-audit.py", "design-scan.py", "seo-sweep.py",
                     "tracking-scan.py", "interaction-scan.py"):
            self.assertIn(scan, text)
        self.assertIn('--out "audit-<slug>"', text)
        rules = (REPO / PAGE_SKILLS["goals"] / "references" / "rules-goals-discovery.md").read_text(encoding="utf-8")
        for scan in ("tracking-scan.py", "interaction-scan.py"):
            self.assertIn(scan, rules)

    def test_build_steps_run_the_setup_check_first(self):
        for page, folder in PAGE_SKILLS.items():
            text = skill_text(folder)
            self.assertIn("setup-check.py", text, page)
            start = text.index("Build the report page")
            if page == "site-snapshot":
                self.assertLess(text.index("setup-check.py"), text.index("## Build the report page"), page)
            else:
                self.assertIn("setup-check.py", text[start:], page)
            self.assertIn("mode", text[start:], page)

    def test_no_deliver_the_files_before_the_build(self):
        for page in ("site-snapshot", "goals"):
            self.assertNotIn("deliver the files", skill_text(PAGE_SKILLS[page]), page)

    def test_finding_key_examples_are_distinct(self):
        examples = {"messaging": "vague-headline", "conversion": "long-form", "seo": "missing-meta",
                    "ux-technical": "slow-lcp", "design": "weak-contrast"}
        for page, key in examples.items():
            text = skill_text(PAGE_SKILLS[page])
            self.assertIn(f"`{key}`", text, page)
            self.assertNotIn("(for example `hero`)", text, page)
        doc = FORMAT_DOC.read_text(encoding="utf-8")
        self.assertIn("unique across all", doc)
        goals = re.search(r"```json\n(.*?)```", doc.split("## goals.json")[1], flags=re.S).group(1)
        self.assertIsNone(re.search(r"\[\[[a-z]", goals))

    def test_format_doc_covers_lists_logo_and_notes(self):
        doc = FORMAT_DOC.read_text(encoding="utf-8")
        for phrase in ("blank line", "no lists, tables or headings", "No real tension",
                       "saved in the run folder", "go in `notes`", "never drop a criterion"):
            self.assertIn(phrase, doc)

    def test_seo_does_not_copy_the_sweep_table(self):
        for path in (REPO / PAGE_SKILLS["seo"] / "SKILL.md",
                     REPO / PAGE_SKILLS["seo"] / "references" / "rules-seo.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("full table in the deliverable", text, path.name)
            self.assertNotIn("Put the full table", text, path.name)
            self.assertIn("seo-sweep.json", text, path.name)

    def test_snapshot_logo_is_a_file_in_the_run_folder(self):
        text = (REPO / PAGE_SKILLS["site-snapshot"] / "references" / "rules-snapshot.md").read_text(encoding="utf-8")
        self.assertNotIn("data URI", text)

    def test_stale_wording_is_gone(self):
        rules = (REPO / "7 Action Report/action-report/references/rules-action-report.md").read_text(encoding="utf-8")
        self.assertNotIn("consistency pass", rules)
        self.assertNotIn("the bundle all live", rules)
        self.assertNotIn("note the change in the Action Report", rules)
        self.assertIn("rating_notes", rules)
        self.assertNotIn("dossier, bundle", (REPO / "README.md").read_text(encoding="utf-8"))

    def test_goals_and_action_report_update_audit_json(self):
        self.assertIn("primary_goal", skill_text(PAGE_SKILLS["goals"]).split("## Build the report page")[1])
        action = skill_text("7 Action Report/action-report")
        self.assertIn("audit.json", action.split("### Step 4")[1].split("### Step 5")[0])

    def test_python_required_wording(self):
        text = skill_text(PAGE_SKILLS["site-snapshot"])
        self.assertNotIn("continue in Basic", text)
        self.assertIn("Python 3.9+ is required", text)

    def test_no_claude_app_examples_in_goals(self):
        text = skill_text(PAGE_SKILLS["goals"])
        self.assertNotIn("e.g. the Claude app", text)
        self.assertNotIn("e.g. Claude Code", text)

    def test_root_sentence_comes_before_the_tool_lead_in(self):
        for page in ("conversion", "seo", "ux-technical", "design"):
            text = skill_text(PAGE_SKILLS[page])
            flat = text.replace("\r\n", "\n")
            self.assertNotRegex(flat, r":\n\nThe suite's scripts", page)


ACTION_SKILL = "7 Action Report/action-report"


class ActionReportBuilderTest(unittest.TestCase):
    def test_action_report_runs_final(self):
        self.assertIn('python "${CLAUDE_PLUGIN_ROOT}/scripts/build-report.py" "audit-<slug>" --final',
                      skill_text(ACTION_SKILL))

    def test_action_report_no_manual_assembly(self):
        text = skill_text(ACTION_SKILL)
        for phrase in ("Regenerate **every**", "Bundle the ZIP", "Assemble & deliver the consolidated"):
            self.assertNotIn(phrase, text)

    def test_action_report_writes_action_json(self):
        text = skill_text(ACTION_SKILL)
        self.assertIn("action-report.json", text)
        self.assertIn("../../audit-data-format.md", text)
        self.assertIn("rating_notes", text)

    def test_action_report_names_the_benchmark_table(self):
        text = " ".join(skill_text(ACTION_SKILL).split())
        self.assertIn("The 2026 baseline in one line per dimension", text)

    def test_action_report_ungrounded_goes_in_rating_notes(self):
        text = " ".join(skill_text(ACTION_SKILL).split())
        self.assertRegex(text, r"first entry in `rating_notes`.*ungrounded")


class ReadmeBuilderTest(unittest.TestCase):
    def test_readme_mentions_builder(self):
        r = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn("build-report.py", r)
        self.assertIn("audit-data-format.md", r)
        self.assertNotIn("plus one compiled handbook", r)

class ActionReportSkillTest(unittest.TestCase):
    def setUp(self):
        self.text = skill_text("7 Action Report/action-report")

    def test_setup_check_runs_before_final(self):
        self.assertIn("setup-check.py", self.text)
        self.assertLess(self.text.index("setup-check.py"), self.text.index("--final"))

    def test_rules_that_repeat_steps_are_gone(self):
        rules = self.text[self.text.index("## Critical rules"):]
        self.assertNotIn("Consistency across dimensions", rules)
        self.assertNotIn("No report without an owner brief", rules)

    def test_benchmark_note_may_cite_findings_and_names_the_standard_cell(self):
        step = self.text[self.text.index("### Step 3"):self.text.index("### Step 4")]
        self.assertIn("[[key]]", step)
        self.assertIn("The 2026 bar", step)


class SharedMethodWordingTest(unittest.TestCase):
    def test_report_format_is_called_the_shared_method(self):
        fmt = (REPO / "report-format.md").read_text(encoding="utf-8")
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn("shared method", fmt)
        self.assertIn("shared method", readme)
        for text in (fmt, readme):
            self.assertNotIn("shared spec", text)



if __name__ == "__main__":
    unittest.main()
