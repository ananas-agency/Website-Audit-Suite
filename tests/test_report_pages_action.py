import base64
import copy
import pathlib
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from report.data import load_run  # noqa: E402
from report.pages_action import brief_fix, render_action, render_report  # noqa: E402
from report.pages_dim import render_dimension  # noqa: E402
from report.pages_intake import render_goals, render_snapshot  # noqa: E402
from report.rules import apply_rules, roadmap  # noqa: E402

FIXTURE = REPO / "tests" / "fixtures" / "sample-run"
HEAD = re.compile(r'<h2 class="section">(?:<span class="no">\d+</span> )?(.*?)(?:<a|</h2>)')
ID = re.compile(r"\b(?:MSG|CRO|SEO|UX|DSN)-\d\d\b")


# Literal copy of the call-to-action block the Action Report must contain exactly once.
CTA_BLOCK = (
    '<div class="ctablock">\n'
    '  <div class="ctahead">Fresh eyes turned your site into a to-do list?</div>\n'
    '  <div class="ctasub">We turn audits like this one into websites that actually convert.</div>\n'
    '  <a class="ctabtn" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;'
    'utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=action-report-cta" '
    'target="_blank" rel="noopener">Let\'s Grow Together</a>\n'
    '</div>'
)


def between(html, start, end):
    i = html.index(start)
    return html[i:html.index(end, i)]


class ActionPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = load_run(FIXTURE)
        cls.keymap = apply_rules(cls.audit)
        cls.html, cls.md = render_action(cls.audit, cls.keymap, False)

    def test_section_order(self):
        self.assertEqual(HEAD.findall(self.html), [
            "Overall scorecard", "2026 standard vs your site", "Executive summary",
            "Priority matrix", "Roadmap", "Plan"])

    def test_overall_row(self):
        # Dimension scores 43, 67, 42, 50, 57 -> mean 51.8 -> 52, grade F.
        self.assertIn('<tr><td><b>Overall</b></td><td><b><span class="grade f">F</span></b></td>'
                      '<td><b>52</b></td></tr>', self.html)
        self.assertIn("<b>Overall:</b> F (52/100)", self.html)
        self.assertIn("## Overall grade: F (52/100)", self.md)
        self.assertIn("| **Overall** | **F** | **52** |", self.md)

    def test_missing_dimension_named_under_table(self):
        run = load_run(FIXTURE)
        del run.dims["seo"]
        keymap = apply_rules(run)
        html, md = render_action(run, keymap, False)
        plain = re.sub(r"<[^>]+>", "", html)
        self.assertIn("SEO &amp; Content not run", plain)
        self.assertIn("SEO & Content not run", md)
        self.assertNotIn("<td>SEO &amp; Content</td>", html)

    def test_matrix_has_every_finding_once(self):
        matrix = between(self.html, '<div class="matrix">', "</section>")
        for f in roadmap(self.audit):
            self.assertEqual(matrix.count(f">{f.id}</a>"), 1, f.id)
        self.assertEqual(len(ID.findall(re.sub(r"title=\"[^\"]*\"", "", matrix))), len(roadmap(self.audit)))
        self.assertEqual(matrix.count('class="quad '), 4)

    def test_matrix_empty_cell_dash(self):
        run = load_run(FIXTURE)
        for d in run.dims.values():
            d.findings = [f for f in d.findings if f.impact >= 3 and f.effort <= 2]
        html, _ = render_action(run, apply_rules(run), False)
        self.assertIn('<div class="quad sk"><h4><span class="dot"></span>Skip — backlog</h4>'
                      '<ul><li>—</li></ul></div>', html)

    def test_roadmap_order_matches_rules(self):
        table = between(self.html, "<th>Fix (brief)</th>", "</section>")
        ids = re.findall(r'<td>\d+</td><td style="white-space:nowrap"><a href="[^"]+" title="[^"]*">([A-Z]+-\d\d)</a>', table)
        self.assertEqual(ids, [f.id for f in roadmap(self.audit)])
        self.assertIn("<th>#</th><th>ID</th><th>Issue</th><th>Fix (brief)</th><th>Impact</th>"
                      "<th>Effort</th><th>From</th>", self.html)

    def test_fix_brief_fallback(self):
        f = copy.copy(roadmap(self.audit)[0])
        f.fix_brief = ""
        f.fix = " ".join(["alpha"] * 60)  # 299 chars
        out = brief_fix(f, self.keymap)
        self.assertLessEqual(len(out), 121)
        self.assertTrue(out.endswith("alpha…"))
        f.fix = "Short first sentence. And a second one that is dropped."
        self.assertEqual(brief_fix(f, self.keymap), "Short first sentence.")
        f.fix_brief = "Author brief"
        self.assertEqual(brief_fix(f, self.keymap), "Author brief")

    def test_fix_brief_not_split_after_abbreviation(self):
        f = copy.copy(roadmap(self.audit)[0])
        f.fix_brief = ""
        f.fix = "Add a meta description that names the service (e.g. 'Bookkeeping for trades'). Then reuse it."
        out = brief_fix(f, self.keymap)
        self.assertNotIn(out, ("Add a meta description that names the service (e.g.",))
        self.assertIn("'Bookkeeping for trades')", out)
        self.assertNotIn("Then reuse", out)

    def test_roadmap_id_cell_does_not_wrap(self):
        table = between(self.html, "<th>Fix (brief)</th>", "</section>")
        self.assertRegex(table, r'<td style="white-space:nowrap"><a href="[^"]+" title="[^"]*">[A-Z]+-\d\d</a></td>')

    def test_fix_brief_strips_links_before_cutting(self):
        f = copy.copy(roadmap(self.audit)[0])
        f.fix_brief = ""
        f.fix = "Move one strong result next to the hero claim and link to the full story at [the case study page](https://example.com/x)."
        out = brief_fix(f, self.keymap)
        self.assertIn("full story at the case study page", out)
        self.assertNotIn("[", out)
        self.assertNotIn("(", out)

    def test_fix_brief_keeps_key_reference_as_id_link(self):
        run = load_run(FIXTURE)
        keymap = apply_rules(run)
        f = next(x for x in roadmap(run) if x.id == "MSG-01")
        f.fix_brief = ""
        f.fix = "Apply the schema from [[schema]] first. Then do more."
        long_fix = "Fix " + " ".join(["alpha"] * 22) + " see [[schema]] and [[heading-order]] later."
        out = brief_fix(f, keymap)
        self.assertEqual(out, "Apply the schema from [[schema]] first.")
        html, md = render_action(run, keymap, False)
        row = html[html.index(">MSG-01</a></td><td>Hero"):]
        row = row[:row.index("</tr>")]
        self.assertRegex(row, r'<a href="seo\.html" title="SEO-02[^"]*">SEO-02</a>')
        self.assertNotIn("[[", md)
        f.fix = long_fix
        out = brief_fix(f, keymap)
        self.assertLessEqual(len(out.replace("[[schema]]", "SEO-02")), 121)
        self.assertEqual(out.count("[["), out.count("]]"))
        f.fix = "alpha " * 20 + "[[schema]] tail words here"
        out = brief_fix(f, keymap)  # 119 chars of alpha, then an ID that does not fit
        self.assertNotIn("[[", out)
        self.assertTrue(out.endswith("alpha…"))

    def test_fix_brief_never_cuts_a_reference_in_the_first_word(self):
        run = load_run(FIXTURE)
        keymap = apply_rules(run)
        f = next(x for x in roadmap(run) if x.id == "MSG-01")
        f.fix_brief = ""
        f.fix = "a" * 115 + "[[schema]]" + "b" * 20 + " tail"  # the ID would end at 121 characters
        out = brief_fix(f, keymap)
        self.assertEqual(out, "a" * 115 + "…")
        f.fix = "a" * 100 + "[[schema]]" + "b" * 30 + " tail"
        out = brief_fix(f, keymap)
        self.assertEqual(out, "a" * 100 + "[[schema]]" + "b" * 14 + "…")

    def test_fix_brief_reference_straddling_the_cut_stays_whole(self):
        run = load_run(FIXTURE)
        keymap = apply_rules(run)
        f = next(x for x in roadmap(run) if x.id == "MSG-01")
        f.fix_brief = ""
        # the reference spans characters 114-124 of the source but renders as a 6-character ID, so it fits
        f.fix = "alpha " * 19 + "[[schema]] and more words follow here"
        out = brief_fix(f, keymap)
        self.assertIn("alpha [[schema]]", out)
        self.assertEqual((out.count("[["), out.count("]]")), (1, 1))
        self.assertLessEqual(len(out.replace("[[schema]]", "SEO-02")), 121)
        self.assertTrue(out.endswith("…"))

    def test_fix_brief_link_with_parentheses_in_url(self):
        run = load_run(FIXTURE)
        keymap = apply_rules(run)
        f = next(x for x in roadmap(run) if x.id == "MSG-01")
        f.fix_brief = ""
        f.fix = "Read [the guide](https://en.wikipedia.org/wiki/A_(b)) first. Then more."
        self.assertEqual(brief_fix(f, keymap), "Read the guide first.")
        f.fix_brief = "See [x](https://en.wikipedia.org/wiki/A_(b))."
        self.assertEqual(brief_fix(f, keymap), "See x.")

    def test_author_fix_brief_resolved_and_flattened_in_md(self):
        run = load_run(FIXTURE)
        keymap = apply_rules(run)
        f = next(x for x in roadmap(run) if x.id == "MSG-01")
        f.fix_brief = "Use **bold** `code` and [[schema]]"
        self.assertEqual(brief_fix(f, keymap), "Use bold code and [[schema]]")
        html, md = render_action(run, keymap, False)
        self.assertIn("| Use bold code and SEO-02 |", md)
        self.assertNotIn("[[", md)
        self.assertNotIn("**", md.split("## Roadmap")[1])

    def test_benchmark_key_not_repeated_when_note_cites_it(self):
        bench = between(self.html, "<th>2026 standard</th>", "</section>")
        self.assertEqual(bench.count(">UX-01</a>"), 1)
        self.assertIn(">SEO-01</a>", bench)  # title-tags key, not cited in the note

    def test_cta_block_exact_and_only_here(self):
        block = CTA_BLOCK
        self.assertIn('class="ctablock"', block)
        self.assertEqual(self.html.count(block), 1)
        others = [render_snapshot(self.audit, False)[0], render_goals(self.audit, self.keymap, False)[0]]
        others += [render_dimension(self.audit, p, self.keymap, False)[0] for p in self.audit.dims]
        for h in others:
            self.assertNotIn('class="ctablock"', h)
        self.assertNotIn("ctablock", self.md)

    def test_run_mode_line(self):
        self.assertIn("<b>Run mode:</b> Extended (measured tools ran)", self.html)
        run = load_run(FIXTURE)
        run.mode = "basic"
        keymap = apply_rules(run)
        html, _ = render_action(run, keymap, False)
        self.assertIn("<b>Run mode:</b> Basic (reasoning only)", html)

    def test_benchmarks_pills_and_keys(self):
        bench = between(self.html, "<th>2026 standard</th>", "</section>")
        self.assertIn('<span class="pill covered">met</span>', bench)
        self.assertEqual(bench.count('<span class="pill gap">gap</span>'), 2)
        self.assertIn('<span class="tag skip">n/a</span>', bench)
        self.assertIn('title="UX-01 —', bench)  # mobile-overflow key rendered as an id link

    def test_exec_summary_and_plan(self):
        summary = between(self.html, "Executive summary", 'class="block"><h2 class="section"><span class="no">4')
        self.assertIn("Biggest opportunity", summary)
        self.assertIn(">MSG-01</a>", summary)
        self.assertIn("Plain language", summary)
        self.assertIn("Rated on the scans in this run only", summary)
        plan = self.html[self.html.index("Your first two weeks"):]
        self.assertIn("Book discovery calls with small-business owners (for example GA4 conversions "
                      "or form completions)", plan)
        self.assertIn("e-run the audit to see the grades move", plan)
        self.assertIn("### Your first two weeks\n- [ ] MSG-01", self.md)

    def test_final_adds_pagenav(self):
        self.assertNotIn('class="pagenav"', self.html)
        html, _ = render_action(self.audit, self.keymap, True)
        self.assertIn('class="pagenav"', html)


# apply_hints wraps terms such as CRO in <abbr>, so stop at the open button, not at any "<a".
REPORT_HEAD = re.compile(r'<h2 class="section">(?:<span class="no">\d+</span> )?(.*?)(?:<a class="openbtn"|</h2>)')
COLGROUP = ('<table style="width:100%;min-width:860px">\n'
            '<colgroup><col style="width:8%"><col style="width:19%"><col style="width:28%">\n'
            '<col style="width:28%"><col style="width:6%"><col style="width:11%"></colgroup>\n'
            '<tr><th>ID</th><th>Finding</th><th>Issue</th><th>Fix</th>\n'
            '<th style="text-align:center">I&nbsp;/&nbsp;E</th><th>Priority</th></tr>')
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")


def plain(html):
    return re.sub(r"<[^>]+>", "", html)


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = load_run(FIXTURE)
        cls.keymap = apply_rules(cls.audit)
        cls.html, cls.md = render_report(cls.audit, cls.keymap)

    def titles(self, html=None):
        return [plain(t).replace("&amp;", "&") for t in REPORT_HEAD.findall(html or self.html)]

    def test_report_section_order(self):
        self.assertEqual(self.titles(), [
            "Executive summary", "Site Snapshot", "Goals & Discovery",
            "Messaging & Clarity — F 43/100", "Conversion (CRO) — D 67/100",
            "SEO & Content — F 42/100", "UX & Technical — F 50/100",
            "Design & Visual — F 57/100", "Action Plan"])
        self.assertIn('<h2 class="section">Executive summary', self.html)
        self.assertIn('<h2 class="section"><span class="no">1</span> Site Snapshot', self.html)
        self.assertIn('<h2 class="section"><span class="no">8</span> Action Plan', self.html)

    def test_findings_table_colgroup_exact(self):
        self.assertEqual(self.html.count(COLGROUP), 5)
        first = self.audit.dims["messaging"].findings[0]
        row = self.html[self.html.index(f">{first.id}</a>") - 200:]
        self.assertIn('<td style="white-space:nowrap">', row)
        self.assertIn('<td style="white-space:nowrap;text-align:center">', self.html)

    def test_findings_row_cells_nowrap_anchored_to_first_row(self):
        first = self.audit.dims["messaging"].findings[0]
        start = self.html.index(f'<tr><td style="white-space:nowrap"><a href="messaging.html"')
        row = self.html[start:self.html.index("</tr>", start)]
        self.assertIn(f">{first.id}</a></td>", row)
        self.assertEqual(row.count('style="white-space:nowrap'), 3)
        self.assertIn('<td style="white-space:nowrap;text-align:center">', row)
        self.assertTrue(row.endswith("</td>"))

    def test_report_digests_are_bare_full_width_tables(self):
        body = self.html[self.html.index("<body>"):]
        self.assertIn('<table style="width:100%"><tr><th>#</th><th>Criterion</th>', body)
        self.assertIn('<table style="width:100%"><tr><th>Dimension</th>', body)
        self.assertEqual(body.count('<table style="width:100%;min-width:860px">'), 5)
        self.assertNotIn("<table>", body)

    def test_flex_headings_in_real_output_keep_hints_in_one_span(self):
        from html.parser import HTMLParser

        class Flex(HTMLParser):
            def __init__(self):
                super().__init__()
                self.stack, self.bare, self.wrapped = [], [], {}

            def handle_starttag(self, tag, attrs):
                cls = dict(attrs).get("class", "")
                if tag == "abbr" and self.stack:
                    kind = self.flex_parent()
                    if kind and self.stack[-1][0] == kind[0]:
                        self.bare.append(kind)
                    elif kind:
                        self.wrapped[kind[1]] = self.wrapped.get(kind[1], 0) + 1
                if tag not in ("br", "img", "input", "meta", "link"):
                    self.stack.append((tag, cls))

            def handle_endtag(self, tag):
                while self.stack:
                    if self.stack.pop()[0] == tag:
                        break

            def flex_parent(self):
                for i in range(len(self.stack) - 1, -1, -1):
                    tag, cls = self.stack[i]
                    if tag == "h2" and "section" in cls:
                        return (tag, "h2")
                    if tag == "h4":
                        return (tag, "h4")
                    if tag == "h3":
                        return (tag, "h3")
                return None

        run = load_run(FIXTURE)
        run.dims["messaging"].findings[0].title = "Hero CTA is vague"
        run.goals.advice[0] = ("Fix the CTA first", run.goals.advice[0][1], run.goals.advice[0][2])
        keymap = apply_rules(run)
        pages = [render_report(run, keymap)[0], render_action(run, keymap, True)[0],
                 render_goals(run, keymap, True)[0], render_dimension(run, "messaging", keymap, True)[0]]
        parser = Flex()
        for html in pages:
            parser.feed(html)
        self.assertEqual(parser.bare, [])
        for kind in ("h2", "h4", "h3"):
            self.assertGreater(parser.wrapped.get(kind, 0), 0, kind)

    def test_digests_not_wrapped(self):
        body = self.html[self.html.index("<body>"):]
        for cls in ("tablewrap", "card"):
            self.assertNotRegex(body, r'class="(?:[^"]*\s)?%s[\s"]' % cls)
        # the Action Report keeps its wrappers
        self.assertIn('class="tablewrap"', render_action(self.audit, self.keymap, False)[0])

    def test_open_buttons_link_pages(self):
        hrefs = re.findall(r'<a class="openbtn" href="([^"]+)"', self.html)
        self.assertEqual(hrefs, ["site-snapshot.html", "goals.html", "messaging.html", "conversion.html",
                                 "seo.html", "ux-technical.html", "design.html", "action-report.html"])

    def test_logo_data_uri_or_name(self):
        self.assertNotIn("data:image", self.html)
        self.assertIn("<h1>Ananas Agency</h1>", self.html)
        self.assertIn("Website audit of Ananas Agency, built with the Website Audit Suite", self.html)
        self.assertIn("by Ananas Agency", self.html)
        run = load_run(FIXTURE)
        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "logo.png").write_bytes(PNG)
            run.dir, run.logo = pathlib.Path(tmp), "logo.png"
            html, _ = render_report(run, apply_rules(run))
        self.assertIn('src="data:image/png;base64,', html)
        run.logo = "missing.png"
        html, _ = render_report(run, apply_rules(run))
        self.assertNotIn("data:image", html)
        self.assertIn("<h1>Ananas Agency</h1>", html)

    def test_logo_must_be_plain_file_name_in_run_folder(self):
        run = load_run(FIXTURE)
        with tempfile.TemporaryDirectory() as tmp:
            outer = pathlib.Path(tmp)
            (outer / "run").mkdir()
            (outer / "x.png").write_bytes(PNG)
            run.dir = outer / "run"
            for name in ("../x.png", str(outer / "x.png"), "sub/x.png", "..\\x.png"):
                run.logo = name
                html, _ = render_report(run, apply_rules(run))
                self.assertNotIn("data:image", html, name)
                self.assertIn("<h1>Ananas Agency</h1>", html)

    def test_missing_dimension_marked(self):
        run = load_run(FIXTURE)
        del run.dims["seo"]
        run.goals = None
        html, md = render_report(run, apply_rules(run))
        self.assertEqual(html.count("— not yet completed —"), 2)
        self.assertEqual(self.titles(html)[2], "Goals & Discovery")
        self.assertIn("SEO & Content", self.titles(html))
        self.assertNotIn('href="seo.html">Open', html)
        self.assertEqual(html.count('class="openbtn"'), 6)
        self.assertEqual(html.count(COLGROUP), 4)

    def test_executive_summary_shows_rating_notes(self):
        run = load_run(FIXTURE)
        self.assertTrue(run.action.rating_notes)
        note = run.action.rating_notes[0]
        html, md = render_report(run, apply_rules(run))
        self.assertIn("Rating notes", between(html, "Executive summary", 'class="block"'))
        self.assertIn(plain(note)[:30], between(html, "Executive summary", 'class="block"'))
        self.assertIn("Rating note", md.split("## 1.")[0])
        run.action.rating_notes = []
        html, md = render_report(run, apply_rules(run))
        self.assertNotIn("Rating note", between(html, "Executive summary", 'class="block"'))

    def test_report_has_no_cta(self):
        self.assertNotIn('class="ctablock"', self.html)
        self.assertNotIn("Let's Grow Together", self.html)
        self.assertNotIn("ctablock", self.md)

    def test_executive_summary(self):
        summary = between(self.html, "Executive summary", 'class="block"')
        self.assertIn("Biggest opportunity", summary)
        self.assertIn("Top 3 quick wins", plain(summary))
        self.assertEqual(summary.count("<a href="), 4)  # 1 opportunity + 3 quick wins
        self.assertIn("Plain language", summary)
        self.assertIn("52/100", summary)
        run = load_run(FIXTURE)
        run.action = None
        html, _ = render_report(run, apply_rules(run))
        self.assertNotIn("working", between(html, "Executive summary", 'class="block"'))

    def test_action_plan_has_2026_table_and_nav(self):
        plan = self.html[self.html.index("Action Plan"):]
        self.assertIn("<th>2026 standard</th>", plan)
        self.assertIn('<div class="matrix">', plan)
        self.assertIn("<th>Fix (brief)</th>", plan)
        self.assertEqual(self.html.count('class="nextbtn" href="site-snapshot.html"'), 1)
        self.assertNotIn('class="prevbtn"', self.html)
        self.assertNotIn("[[", self.html)
        self.assertNotIn("[[", self.md)
        self.assertIn("## Executive summary", self.md)


if __name__ == "__main__":
    unittest.main()
