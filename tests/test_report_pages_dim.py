import hashlib
import json
import pathlib
import re
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from report import DIMENSIONS  # noqa: E402
from report.chrome import dochead, page, pagenav, sections, walk, write_page  # noqa: E402
from report.data import load_run  # noqa: E402
from report.pages_action import render_report  # noqa: E402
from report.pages_dim import render_dimension  # noqa: E402
from report.rules import apply_rules  # noqa: E402

FIXTURE = REPO / "tests" / "fixtures" / "sample-run"
HEAD = re.compile(r'<h2 class="section">(?:<span class="no">\d+</span> )?(.*?)(?:<a|</h2>)')


def fresh():
    run = load_run(FIXTURE)
    return run, apply_rules(run)


class DimensionPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit, cls.keymap = fresh()

    def render(self, page_name, final=False):
        return render_dimension(self.audit, page_name, self.keymap, final)

    def test_dimension_sections_in_order(self):
        html, _ = self.render("seo")
        heads = HEAD.findall(html)
        self.assertEqual(heads[:2], ["Grade &amp; scorecard", "Findings"])
        self.assertEqual(heads[-2:], ["What&rsquo;s working", "Summary"])

    def test_sections_are_numbered_in_sequence(self):
        html, _ = self.render("messaging")
        nums = re.findall(r'<span class="no">(\d+)</span>', html)
        self.assertEqual(nums, [str(i) for i in range(1, len(nums) + 1)])

    def test_card_title_keeps_hint_inside_one_flex_item(self):
        run, _ = fresh()
        run.dims["messaging"].findings[0].title = "Hero CTA is vague"
        html, _ = render_dimension(run, "messaging", apply_rules(run), False)
        h3 = re.search(r'<h3><span class="id">MSG-\d+</span> (.*?)<span class="scorewrap">', html).group(1)
        self.assertRegex(h3, r'^<span class="ttl">Hero <abbr title="[^"]*">CTA</abbr> is vague</span>$')

    def test_card_markup(self):
        html, _ = self.render("messaging")
        self.assertIn('<span class="id">MSG-01</span>', html)
        self.assertIn("width:100%", html)  # MSG-01 is impact 5
        self.assertIn("width:60%", html)   # impact 3
        self.assertIn("Impact 5/5", html)
        self.assertIn("Effort 2/5", html)
        seo, _ = self.render("seo")
        self.assertIn("width:80%", seo)    # SEO-01 is impact 4

    def test_card_has_tag_label_and_evidence(self):
        html, _ = self.render("messaging")
        self.assertIn('<span class="tag quickwin" title=', html)
        self.assertIn("<blockquote>", html)
        self.assertIn("<code>h1</code>", html)

    def test_scorecard_table(self):
        html, _ = self.render("messaging")
        self.assertIn("<th>#</th><th>Criterion</th><th>Result</th><th>Weight</th><th>Points</th>", html)
        dim = self.audit.dims["messaging"]
        total = sum(r.weight for r in dim.rubric)
        self.assertIn("<td><b>Total</b></td><td></td><td><b>%d</b></td>" % total, html)
        self.assertIn('class="grade %s"' % dim.grade.lower(), html)
        self.assertIn("<b>%d/100</b>" % dim.score, html)

    def test_verdict_markdown_converted(self):
        html, _ = self.render("messaging")
        self.assertIn("<b>hero</b>", html)

    def test_key_reference_is_link_in_prose(self):
        html, _ = self.render("seo")
        self.assertIn('<a href="messaging.html" title="MSG-01', html)

    def test_summary_top_priority_is_link(self):
        html, _ = self.render("seo")
        summary = html.split("Summary")[-1]
        top = self.audit.dims["seo"].findings[0]
        self.assertIn(">%s</a>" % top.id, summary)
        self.assertRegex(re.sub(r"<[^>]+>", "", summary), r"\d+ \(\d+ quick wins?, \d+ big bets?\)")

    def test_measured_chip_only_when_measured(self):
        for page_name, dim in self.audit.dims.items():
            html = self.render(page_name)[0]
            self.assertEqual(html.count('class="chip-measured"'),
                             sum(f.measured for f in dim.findings), page_name)

    def test_measured_chip_present_on_a_measured_finding(self):
        measured = [f for f in self.audit.dims["conversion"].findings if f.measured]
        self.assertTrue(measured)
        html = self.render("conversion")[0]
        card = html[html.index(f'<span class="id">{measured[0].id}</span>'):]
        self.assertIn('class="chip-measured"', card[:card.index("</h3>")])

    def test_working_copy_has_no_nav_final_has_walk(self):
        self.assertNotIn('class="pagenav"', self.render("seo")[0])
        final = self.render("seo", True)[0]
        self.assertIn('href="conversion.html"', final)
        self.assertIn('href="ux-technical.html"', final)

    def test_header_meta_has_date_model_grade(self):
        html, _ = self.render("seo")
        dim = self.audit.dims["seo"]
        self.assertIn("<b>Date:</b> %s" % self.audit.date, html)
        self.assertIn("<b>Model:</b> Ananas-Agency Website Audit", html)
        self.assertIn("<b>Grade:</b> %s (%d/100)" % (dim.grade, dim.score), html)
        self.assertIn("<h1>SEO &amp; Content — %s</h1>" % self.audit.site, html)

    def test_footer_date_comes_from_run(self):
        html, _ = self.render("seo")
        self.assertIn("generated %s." % self.audit.date, html)

    def test_hints_applied_but_not_inside_tags(self):
        html, _ = self.render("messaging")
        self.assertIn("<abbr", html)
        self.assertNotRegex(html, r'<span class="tag[^>]*>[^<]*<abbr')

    def test_markdown_page(self):
        _, md = self.render("messaging")
        self.assertIn("## Findings", md)
        self.assertRegex(md, r"### MSG-01\. .+ — Impact \d · Effort \d · (quick win|big bet|fill-in|skip)")
        self.assertIn("## Grade:", md)
        self.assertIn("### Scorecard", md)
        self.assertIn("## What's working", md)
        self.assertIn("## Summary", md)
        self.assertNotIn("[[", md)

    def test_markdown_scorecard_escapes_pipe_in_criterion(self):
        run, keymap = fresh()
        run.dims["messaging"].rubric[0].criterion = "Clear | concise"
        _, md = render_dimension(run, "messaging", keymap, False)
        row = next(l for l in md.splitlines() if l.startswith("| 1 |"))
        self.assertIn("Clear \\| concise", row)
        self.assertEqual(len(re.findall(r"(?<!\\)\|", row)), 6)

    def test_markdown_resolves_key_references(self):
        _, md = self.render("seo")
        self.assertIn("MSG-01", md)

    def test_print_hint_exact(self):
        html, _ = self.render("seo")
        self.assertIn('<p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> '
                      '(<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>', html)

    def test_frame_basics(self):
        html, _ = self.render("seo")
        self.assertTrue(html.startswith("<!DOCTYPE html>\n<html lang=\"en\">"))
        self.assertIn('<meta charset="utf-8">', html)
        self.assertIn('class="brandband"', html)
        self.assertIn('<footer class="doc">', html)
        self.assertIn("utm_content=seo-content", html)

    def test_non_ascii_round_trip(self):
        run, keymap = fresh()
        run.site = "Ананас — “Grow”"
        html, md = render_dimension(run, "messaging", keymap, False)
        with tempfile.TemporaryDirectory() as tmp:
            write_page(pathlib.Path(tmp), "messaging", html, md)
            raw = (pathlib.Path(tmp) / "messaging.html").read_bytes()
            self.assertNotIn(b"\r", raw)
            self.assertNotIn(b"\r", (pathlib.Path(tmp) / "messaging.md").read_bytes())
            self.assertIn("Ананас — “Grow”", raw.decode("utf-8"))
            self.assertIn("Ананас — “Grow”", (pathlib.Path(tmp) / "messaging.md").read_text(encoding="utf-8"))

    def test_extra_section_rendered_after_findings(self):
        run, keymap = fresh()
        run.dims["messaging"].extra = [("Extra topic", "Some **bold** text")]
        html, md = render_dimension(run, "messaging", keymap, False)
        heads = HEAD.findall(html)
        self.assertEqual(heads.index("Extra topic"), heads.index("Findings") + 1)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("## Extra topic", md)


class ChromeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit, cls.keymap = fresh()

    def test_sections_numbers_only_with_two_or_more(self):
        one = sections([("Only", "x", "")])
        self.assertNotIn('class="no"', one)
        two = sections([("A", "x", ""), ("B", "y", "")])
        self.assertIn('<span class="no">1</span> A', two)
        self.assertIn('<span class="no">2</span> B', two)

    def test_sections_open_button(self):
        html = sections([("A", "x", "goals.html"), ("B", "y", "")])
        self.assertEqual(html.count("Open full document →"), 1)
        self.assertIn('<a class="openbtn" href="goals.html">Open full document →</a>', html)

    def test_walk_order_and_goals_conditional(self):
        names = walk(self.audit)
        self.assertEqual(names[0], "report")
        self.assertEqual(names[1], "site-snapshot")
        self.assertEqual(names[-1], "action-report")
        self.assertEqual("goals" in names, self.audit.goals is not None)
        self.assertEqual([n for n in names if n in {d[0] for d in DIMENSIONS}],
                         [d[0] for d in DIMENSIONS if d[0] in self.audit.dims])
        run, _ = fresh()
        run.goals = None
        self.assertNotIn("goals", walk(run))
        run.snapshot = None
        run.action = None
        self.assertEqual(walk(run)[0], "report")
        self.assertNotIn("site-snapshot", walk(run))
        self.assertNotIn("action-report", walk(run))

    def test_pagenav_labels_and_hrefs(self):
        run, _ = fresh()
        self.assertIsNotNone(run.goals)
        nav = pagenav(run, "report")
        self.assertIn('href="site-snapshot.html">Site Snapshot →', nav)
        self.assertNotIn("prevbtn", nav)
        nav = pagenav(run, "messaging")
        self.assertIn("← Goals &amp; Discovery", nav)
        self.assertIn("Conversion (CRO) →", nav)
        nav = pagenav(run, "site-snapshot")
        self.assertIn('href="_%s-website-audit-report.html">← Audit Report' % run.slug, nav)
        self.assertIn('href="goals.html">Goals &amp; Discovery →', nav)
        nav = pagenav(run, "action-report")
        self.assertIn("← Design &amp; Visual", nav)
        self.assertNotIn("nextbtn", nav)

    def test_pagenav_skips_goals_when_absent(self):
        run, _ = fresh()
        run.goals = None
        self.assertIn('href="site-snapshot.html">← Site Snapshot', pagenav(run, "messaging"))
        self.assertIn('href="messaging.html">Messaging &amp; Clarity →', pagenav(run, "site-snapshot"))

    def test_dochead_and_page(self):
        self.assertEqual(dochead("T", "m"), '<header class="doc"><h1>T</h1><div class="meta">m</div></header>')
        html = page("A & B", "seo-content", dochead("T", "m"), "<p>x</p>", "<nav></nav>", date="2026-01-02")
        self.assertIn("generated 2026-01-02.", html)
        self.assertIn("<title>A &amp; B</title>", html)
        self.assertIn("<style>\n", html)
        self.assertLess(html.index("<p>x</p>"), html.index("<nav></nav>"))
        self.assertLess(html.index("<nav></nav>"), html.index('class="printhint"'))

    def test_style_css_unchanged(self):
        # style.css is now the source of truth for the report look; this hash pins today's content so a
        # change is deliberate (update the constant together with the CSS). read_text normalises line
        # endings, as the builder does (chrome._read_css); git may check the file out with CRLF on
        # Windows (* text=auto), so hashing raw bytes would fail on a fresh clone.
        css = (REPO / "scripts" / "report" / "style.css").read_text(encoding="utf-8")
        digest = hashlib.sha256(css.encode("utf-8")).hexdigest()
        self.assertEqual(digest, "6da1ff5049de215f8a508c5abde9ccbc8d0dd87eb36c28f9c49e4ae5590eb9b1")


class LineEndingTests(unittest.TestCase):
    def test_crlf_fix_text_keeps_the_markdown_row_on_one_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = pathlib.Path(tmp) / "run"
            shutil.copytree(FIXTURE, run_dir)
            path = run_dir / "audit-data" / "seo.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["findings"][0]["fix"] = "Fix the title.\r\n\r\nThen the meta."
            path.write_text(json.dumps(data), encoding="utf-8")
            run = load_run(run_dir)
            keymap = apply_rules(run)
            html, _ = render_dimension(run, "seo", keymap, False)
            _, md = render_report(run, keymap)
        self.assertNotIn("\r", md)
        self.assertNotIn("\r", html)
        rows = [line for line in md.split("\n") if line.startswith("| SEO-01")]
        self.assertEqual(len(rows), 1)
        self.assertIn("Then the meta.", rows[0])
        self.assertIn("Fix the title.<br><br>Then the meta.", html)


if __name__ == "__main__":
    unittest.main()
