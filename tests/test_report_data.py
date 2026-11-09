import json
import pathlib
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO, load_script  # noqa: E402,F401

sys.path.insert(0, str(REPO / "scripts"))
from report import DIMENSIONS  # noqa: E402
from report import data  # noqa: E402
from report.data import DataError, load_run  # noqa: E402

FIXTURE = REPO / "tests" / "fixtures" / "sample-run"


class ReportDataTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name) / "run"
        shutil.copytree(FIXTURE, self.tmp)

    def edit(self, name, fn):
        path = self.tmp / "audit-data" / f"{name}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        fn(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def errors(self):
        with self.assertRaises(DataError) as cm:
            load_run(self.tmp)
        return cm.exception.errors

    def test_reference_with_inner_spaces_rejected(self):
        self.edit("messaging", lambda d: d.update(notes="See [[ hero ]] for details."))
        errs = self.errors()
        self.assertTrue(any("[[ hero ]]" in e and "space" in e for e in errs), errs)

    def test_load_sample_run(self):
        run = load_run(FIXTURE)
        self.assertEqual(run.slug, "ananas-agency")
        self.assertEqual(sorted(run.dims), ["conversion", "design", "messaging", "seo", "ux-technical"])
        self.assertIn("perf-a11y.json", run.scans)
        self.assertEqual(run.mode, "extended")

    def test_errors_name_file_and_path(self):
        self.edit("messaging", lambda d: d["findings"][0].update(impact=7))
        self.assertIn("messaging.json: findings[0].impact must be 1-5, got 7", self.errors())

    def test_all_errors_collected(self):
        self.edit("messaging", lambda d: d["findings"][0].update(impact=7))
        self.edit("design", lambda d: d["rubric"][0].update(result="Maybe"))
        self.assertEqual(len(self.errors()), 2)

    def test_unknown_key_reference(self):
        self.edit("messaging", lambda d: d.update(notes="See [[no-such-key]] for details."))
        self.assertTrue(any("[[no-such-key]]" in e for e in self.errors()))

    def test_duplicate_key_across_dimensions(self):
        self.edit("seo", lambda d: d["findings"][0].update(key="hero"))
        self.assertTrue(any("duplicate key" in e for e in self.errors()))

    def test_key_and_slug_with_trailing_newline_rejected(self):
        self.edit("seo", lambda d: d["findings"][0].update(key="abc\n"))
        self.assertTrue(any("seo.json: findings[0].key" in e for e in self.errors()))
        self.edit("seo", lambda d: d["findings"][0].update(key="title-tags"))
        self.edit("audit", lambda d: d.update(slug="abc\n"))
        self.assertTrue(any(e.startswith("audit.json: slug") for e in self.errors()))

    def test_compact_date_rejected(self):
        self.edit("audit", lambda d: d.update(date="20261106"))
        self.assertTrue(any(e.startswith("audit.json: date") for e in self.errors()))

    def test_duplicate_key_within_one_file_names_file_once(self):
        self.edit("seo", lambda d: d["findings"][1].update(key=d["findings"][0]["key"]))
        key = json.loads((self.tmp / "audit-data" / "seo.json").read_text(encoding="utf-8"))["findings"][0]["key"]
        self.assertIn(f"duplicate key '{key}' twice in seo.json", self.errors())

    def test_typo_field_rejected(self):
        self.edit("seo", lambda d: d.update(strenghts=d.pop("strengths")))
        self.assertTrue(any("seo.json: unknown field 'strenghts'" in e for e in self.errors()))

    def test_partial_run_loads(self):
        data = self.tmp / "audit-data"
        for p in data.iterdir():
            if p.name not in ("audit.json", "messaging.json"):
                p.unlink()
        run = load_run(self.tmp)
        self.assertEqual(list(run.dims), ["messaging"])
        self.assertIsNone(run.goals)

    def test_dimensions_constant(self):
        self.assertEqual(DIMENSIONS, (
            ("messaging", "MSG", "Messaging & Clarity", "messaging-clarity"),
            ("conversion", "CRO", "Conversion (CRO)", "conversion-cro"),
            ("seo", "SEO", "SEO & Content", "seo-content"),
            ("ux-technical", "UX", "UX & Technical", "ux-technical"),
            ("design", "DSN", "Design & Visual", "design-visual"),
        ))
        dim = load_run(FIXTURE).dims["seo"]
        self.assertEqual((dim.prefix, dim.title, dim.utm), ("SEO", "SEO & Content", "seo-content"))

    def test_missing_audit_json(self):
        (self.tmp / "audit-data" / "audit.json").unlink()
        self.assertTrue(any(e.startswith("audit.json:") for e in self.errors()))

    def test_basic_mode_without_scans(self):
        for p in self.tmp.glob("*.json"):
            p.unlink()
        for name in ("conversion", "ux-technical"):  # no scans ran, so no finding may claim to be measured
            self.edit(name, lambda d: [f.pop("measured", None) for f in d["findings"]])
        self.assertEqual(load_run(self.tmp).mode, "basic")

    def _mark_measured(self, name, mode=None, drop=()):
        def fn(d):
            d["findings"][0]["measured"] = True
        self.edit(name, fn)
        for f in drop:
            (self.tmp / f).unlink()
        if mode:
            self.edit("audit", lambda d: d.update(mode=mode))

    def test_measured_finding_without_its_scan_rejected(self):
        self._mark_measured("seo", drop=("seo-sweep.json",))
        self.assertIn("seo.json: findings[0] is marked measured but no scan for this page ran", self.errors())

    def test_measured_finding_backed_by_its_scan_loads(self):
        self._mark_measured("seo")
        load_run(self.tmp)

    NO_SCAN = "findings[0] is marked measured but no scan for this page ran"
    BASIC = "findings[0] is marked measured but this is a basic run, so no browser scan ran"

    def test_basic_run_accepts_a_finding_backed_by_the_sweep(self):
        for name in ("conversion", "ux-technical", "design"):  # these need a browser, so a basic run can't claim them
            self.edit(name, lambda d: [f.pop("measured", None) for f in d["findings"]])
        self._mark_measured("seo", mode="basic")  # seo-sweep.json needs no browser
        load_run(self.tmp)

    def test_basic_run_without_the_sweep_gets_the_missing_scan_message(self):
        self._mark_measured("seo", mode="basic", drop=("seo-sweep.json",))
        self.assertIn("seo.json: " + self.NO_SCAN, self.errors())

    def test_basic_run_rejects_a_ux_finding_that_needs_a_browser(self):
        for drop in ((), ("perf-a11y.json",)):  # a browser scan file lying around doesn't make the run extended
            with self.subTest(drop=drop):
                shutil.rmtree(self.tmp)
                shutil.copytree(FIXTURE, self.tmp)
                self._mark_measured("ux-technical", mode="basic", drop=drop)
                self.assertIn("ux-technical.json: " + self.BASIC, self.errors())

    def test_extended_run_accepts_a_ux_finding_backed_by_interaction_only(self):
        self._mark_measured("ux-technical", drop=("perf-a11y.json", "mobile-metrics.json", "design-tokens.json"))
        self.assertIn("interaction.json", load_run(self.tmp).scans)

    def test_extended_run_rejects_a_ux_finding_with_no_backing_scan(self):
        self._mark_measured("ux-technical", drop=("perf-a11y.json", "mobile-metrics.json",
                                                  "interaction.json", "design-tokens.json"))
        self.assertIn("ux-technical.json: " + self.NO_SCAN, self.errors())

    def test_measured_messaging_needs_some_scan(self):
        self._mark_measured("messaging")
        load_run(self.tmp)
        for p in list(self.tmp.glob("*.json")):
            p.unlink()
        self.edit("audit", lambda d: d.update(mode="extended"))
        self.assertIn("messaging.json: findings[0] is marked measured but no scan for this page ran",
                      self.errors())

    def test_bad_weight_and_status(self):
        self.edit("seo", lambda d: d["rubric"][0].update(weight=0))
        self.edit("action-report", lambda d: d["benchmarks"][0].update(status="open"))
        errs = self.errors()
        self.assertIn("seo.json: rubric[0].weight must be a positive integer, got 0", errs)
        self.assertTrue(any("benchmarks[0].status" in e for e in errs))

    def test_rubric_weights_must_sum_to_100(self):
        def two_rows(d):
            d["rubric"] = d["rubric"][:2]
            d["rubric"][0]["weight"], d["rubric"][1]["weight"] = 60, 30
        self.edit("seo", two_rows)
        self.assertIn("seo.json: rubric weights sum to 90, must be 100", self.errors())

    def test_rubric_weights_over_100_rejected(self):
        def two_rows(d):
            d["rubric"] = d["rubric"][:2]
            d["rubric"][0]["weight"], d["rubric"][1]["weight"] = 70, 50
        self.edit("seo", two_rows)
        self.assertIn("seo.json: rubric weights sum to 120, must be 100", self.errors())

    def test_benchmark_key_must_name_finding(self):
        self.edit("action-report", lambda d: d["benchmarks"][0].update(keys=["title-tags", "xyz"]))
        self.assertIn("action-report.json: benchmarks[0].keys[1] names unknown finding 'xyz'",
                      self.errors())


def minimal_page():
    return {
        "verdict": "Solid.",
        "rubric": [{"criterion": "Headers set", "result": "Pass", "weight": 100}],
        "findings": [{"key": "no-csp", "title": "No CSP", "issue": "No policy.", "impact_text": "XSS risk.",
                      "fix": "Add a CSP.", "impact": 3, "effort": 2}],
        "strengths": ["HTTPS everywhere"],
    }


class ValidateDimensionTest(unittest.TestCase):
    def test_sample_page_is_clean(self):
        raw = json.loads((FIXTURE / "audit-data" / "ux-technical.json").read_text(encoding="utf-8"))
        errors, rubric, findings = data.validate_dimension(raw, "ux-technical.json")
        self.assertEqual(errors, [])
        self.assertEqual(len(rubric), len(raw["rubric"]))
        self.assertEqual(len(findings), len(raw["findings"]))

    def test_messages_match_load_run(self):
        # weight sum 90, impact 7, an unknown [[key]]: same messages load_run gives for ux-technical.json
        raw = json.loads((FIXTURE / "audit-data" / "ux-technical.json").read_text(encoding="utf-8"))
        raw["rubric"][0]["weight"] -= 10
        raw["findings"][0]["impact"] = 7
        raw["verdict"] += " See [[unknown-key]]."
        errors, _, _ = data.validate_dimension(raw, "ux-technical.json")
        with tempfile.TemporaryDirectory() as tmp:
            run = pathlib.Path(tmp) / "run"
            shutil.copytree(FIXTURE, run)
            (run / "audit-data" / "ux-technical.json").write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(DataError) as cm:
                load_run(run)
        theirs = [e for e in cm.exception.errors if e.startswith("ux-technical.json: ")]
        self.assertEqual(len(errors), 3, errors)
        self.assertEqual(sorted(errors), sorted(theirs))

    def test_duplicate_key_within_file(self):
        raw = minimal_page()
        raw["findings"].append(dict(raw["findings"][0]))
        errors, _, _ = data.validate_dimension(raw, "security.json")
        self.assertEqual(errors, ["duplicate key 'no-csp' twice in security.json"])

    def test_page_name_not_needed(self):
        errors, _, findings = data.validate_dimension(minimal_page(), "security.json")
        self.assertEqual(errors, [])
        self.assertEqual(findings[0].dim, "")

    def test_non_object_reports_error(self):
        errors, rubric, findings = data.validate_dimension([], "security.json")
        self.assertTrue(errors and errors[0].startswith("security.json: "), errors)
        self.assertEqual((rubric, findings), ([], []))


if __name__ == "__main__":
    unittest.main()
