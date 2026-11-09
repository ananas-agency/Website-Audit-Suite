import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO, load_script  # noqa: E402,F401

sys.path.insert(0, str(REPO / "scripts"))
from report import DIMENSIONS  # noqa: E402
from report.data import Dimension, Finding, RubricRow, Run  # noqa: E402
from report.rules import (  # noqa: E402
    all_findings, apply_rules, biggest_opportunity, grade, overall, phases,
    quadrant, roadmap, score_rubric, top_quick_wins,
)


def finding(key, impact, effort):
    return Finding(key=key, title=key, issue="i", impact_text="t", fix="f",
                   impact=impact, effort=effort)


def make_run(spec, scores=None):
    """spec: {page: [(impact, effort), ...]}; scores: {page: score} for dims with preset scores."""
    dims = {}
    for page, prefix, title, utm in DIMENSIONS:
        if page not in spec and page not in (scores or {}):
            continue
        fs = [finding(f"{page}-{n}", i, e) for n, (i, e) in enumerate(spec.get(page, []))]
        d = Dimension(page, prefix, title, utm, "verdict", findings=fs)
        if scores and page in scores:
            d.score = scores[page]
        dims[page] = d
    return Run(dir=pathlib.Path("."), site="S", url="https://s.test", slug="s", date="2026-01-01",
               tagline="", primary_goal="g", mode="basic", logo="", dims=dims)


class ReportRulesTests(unittest.TestCase):
    def test_quadrants(self):
        cases = {(5, 1): "quickwin", (3, 2): "quickwin", (3, 3): "bigbet", (4, 5): "bigbet",
                 (2, 2): "fillin", (1, 1): "fillin", (2, 3): "skip", (1, 5): "skip"}
        for (i, e), q in cases.items():
            self.assertEqual(quadrant(i, e), q, (i, e))

    def test_ids_strongest_first(self):
        run = make_run({"messaging": [(2, 1), (4, 3), (4, 1)]})
        apply_rules(run)
        dim = run.dims["messaging"]
        self.assertEqual([f.id for f in dim.findings], ["MSG-01", "MSG-02", "MSG-03"])
        self.assertEqual([(f.impact, f.effort) for f in dim.findings], [(4, 1), (4, 3), (2, 1)])

    def test_rubric_points_and_normalised_score(self):
        pts, score = score_rubric([RubricRow("a", "Pass", 60), RubricRow("b", "Partial", 40)])
        self.assertEqual((pts, score), ([60, 20.0], 80))
        self.assertEqual(score_rubric([RubricRow("a", "Pass", 3), RubricRow("b", "Fail", 5)])[1], 38)

    def test_rubric_half_up_exact_at_float_edges(self):
        # 14.5 points of 100: the divide-first float form gives 14.499999999999998; the rule requires 15.
        rows = [RubricRow("a", "Partial", 29), RubricRow("b", "Fail", 71)]
        self.assertEqual(score_rubric(rows)[1], 15)
        self.assertEqual(score_rubric([RubricRow("a", "Partial", 1), RubricRow("b", "Fail", 99)])[1], 1)

    def test_grade_bands(self):
        self.assertEqual([grade(s)[0] for s in (100, 90, 89, 80, 79, 70, 69, 60, 59, 0)],
                         list("AABBCCDDFF"))
        self.assertEqual(grade(85), ("B", "b"))

    def test_overall_half_up_and_missing(self):
        run = make_run({}, scores={"messaging": 62, "seo": 63})
        self.assertEqual(overall(run),
                         (63, "D", ["Conversion (CRO)", "UX & Technical", "Design & Visual"]))

    def test_biggest_and_top_quick_wins(self):
        run = make_run({"messaging": [(5, 3), (3, 2)], "conversion": [(5, 1)], "seo": [(4, 1)]})
        apply_rules(run)
        self.assertEqual(biggest_opportunity(run).id, "CRO-01")
        self.assertEqual([f.id for f in top_quick_wins(run)], ["CRO-01", "SEO-01", "MSG-02"])

    def test_roadmap_and_phases_order(self):
        run = make_run({"messaging": [(5, 3), (3, 2), (4, 4), (4, 5), (3, 3), (1, 1), (2, 5)],
                        "conversion": [(5, 1), (2, 2)], "seo": [(4, 1)]})
        apply_rules(run)
        rank = {"quickwin": 0, "bigbet": 1, "fillin": 2, "skip": 3}
        r = roadmap(run)
        self.assertEqual([rank[f.quad] for f in r], sorted(rank[f.quad] for f in r))
        self.assertEqual(len(r), len(all_findings(run)))
        p = phases(run)
        self.assertLessEqual(len(p["days_30_60"]), 3)
        self.assertEqual(len(p["two_weeks"]), sum(f.quad == "quickwin" for f in r))
        bigbets = [f for f in r if f.quad == "bigbet"]
        self.assertEqual(p["days_30_60"], bigbets[:3])
        self.assertEqual(p["days_60_90"], bigbets[3:] + [f for f in r if f.quad == "fillin"])

    def test_apply_rules_is_idempotent(self):
        run = make_run({"messaging": [(2, 1), (4, 3), (4, 1)], "seo": [(3, 3), (3, 1)]})
        first = {k: f.id for k, f in apply_rules(run).items()}
        self.assertEqual(first, {k: f.id for k, f in apply_rules(run).items()})
        self.assertEqual(len(first), 5)


if __name__ == "__main__":
    unittest.main()
