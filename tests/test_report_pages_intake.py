import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from report.data import load_run  # noqa: E402
from report.pages_intake import render_goals, render_snapshot, tbd_labels  # noqa: E402
from report.rules import apply_rules  # noqa: E402

FIXTURE = REPO / "tests" / "fixtures" / "sample-run"
HEAD = re.compile(r'<h2 class="section">(?:<span class="no">\d+</span> )?(.*?)(?:<a|</h2>)')


class IntakePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = load_run(FIXTURE)
        cls.keymap = apply_rules(cls.audit)

    def goals(self, final=False):
        return render_goals(self.audit, self.keymap, final)

    def test_snapshot_rows_and_tbd(self):
        html, _ = render_snapshot(self.audit, False)
        self.assertIn('<div class="row"><span class="k">Business</span>Digital agency</div>', html)
        self.assertIn('<span class="k">Platform / CMS</span><b>TBD</b>', html)
        self.assertEqual(tbd_labels(self.audit), ["Platform & signals / Platform / CMS"])
        heads = HEAD.findall(html)
        self.assertEqual(heads[0], "Site &amp; business")
        self.assertEqual(heads[-1], "Next step")
        self.assertIn(self.audit.snapshot.description, html)

    def test_snapshot_tbd_case_insensitive(self):
        from report.data import Snapshot
        saved = self.audit.snapshot
        try:
            self.audit.snapshot = Snapshot("d", [("S", [("A", "tbd"), ("B", " Tbd "), ("C", "TBDX")])])
            html, _ = render_snapshot(self.audit, False)
            self.assertEqual(html.count("<b>TBD</b>"), 2)
            self.assertEqual(tbd_labels(self.audit), ["S / A", "S / B"])
        finally:
            self.audit.snapshot = saved

    def test_snapshot_tbd_ignores_light_markdown_and_punctuation(self):
        from report.data import Snapshot
        saved = self.audit.snapshot
        try:
            self.audit.snapshot = Snapshot("d", [("S", [("A", "**TBD**"), ("B", "TBD."), ("C", "_tbd_!"),
                                                         ("D", "TBD later")])])
            self.assertEqual(tbd_labels(self.audit), ["S / A", "S / B", "S / C"])
        finally:
            self.audit.snapshot = saved

    def test_goals_sections_in_order(self):
        html, _ = self.goals()
        self.assertEqual(HEAD.findall(html), [
            "Owner brief", "Stated vs. observed", "Tensions", "How to reach your goal",
            "How this shapes the audit", "Next step"])
        self.assertIn("<th>You said</th><th>What the page + scans show</th><th>The gap</th>", html)
        self.assertIn('<h3><span class="id">1</span> <span class="ttl">Lead with one outcome</span></h3>', html)
        self.assertIn("→ ", html)
        self.assertNotIn("[[", html)

    def test_goals_table_cells_escaped(self):
        from report.data import Goals
        saved = self.audit.goals
        try:
            self.audit.goals = Goals("f", [("k", "v")], [("<script>x</script>", "a & b", "<i>")], [], [], "")
            html, md = render_goals(self.audit, self.keymap, False)
            self.assertNotIn("<script>", html)
            self.assertIn("&lt;script&gt;x&lt;/script&gt;", html)
            self.assertIn("a &amp; b", html)
        finally:
            self.audit.goals = saved

    def test_intake_markdown_headings(self):
        _, snap_md = render_snapshot(self.audit, False)
        self.assertIn("## Site & business", snap_md)
        self.assertIn("- Platform / CMS: TBD", snap_md)
        self.assertTrue(snap_md.endswith("about the site.\n"))
        _, md = self.goals()
        self.assertIn("## Stated vs. observed (the reality-check)", md)
        self.assertIn("## Owner brief (what they told us)", md)
        self.assertIn("| You said | What the page + scans show | The gap |", md)
        self.assertIn("1. **Lead with one outcome** — ", md)
        self.assertNotIn("[[", md)

    def test_nav_only_when_final(self):
        self.assertNotIn('class="pagenav"', render_snapshot(self.audit, False)[0])
        self.assertIn('class="pagenav"', render_snapshot(self.audit, True)[0])
        self.assertIn('class="pagenav"', self.goals(True)[0])


if __name__ == "__main__":
    unittest.main()
