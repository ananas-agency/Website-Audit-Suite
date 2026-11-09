import dataclasses
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
from report.data import load_run  # noqa: E402
from report.measured import measured_sections  # noqa: E402
from report.pages_dim import render_dimension  # noqa: E402
from report.rules import apply_rules  # noqa: E402

FIXTURE = REPO / "tests" / "fixtures" / "sample-run"
NOT_MEASURED = "not measured — available with the Extended layer"


def joined(sections):
    return "\n".join(h for _t, h, _m in sections)


def joined_md(sections):
    return "\n".join(m for _t, _h, m in sections)


def clone(obj):
    return json.loads(json.dumps(obj))


class MeasuredTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = pathlib.Path(tempfile.mkdtemp())
        cls.addClassCleanup(shutil.rmtree, cls.tmp, True)
        cls.audit = load_run(FIXTURE)
        cls.keymap = apply_rules(cls.audit)
        cls.basic = dataclasses.replace(cls.audit, scans={}, mode="basic", dir=cls.tmp)

    def scans(self, name):
        return self.audit.scans[name]

    def tmpdir(self):
        d = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d, True)
        return d

    def test_perf_values_shown(self):
        html = joined(measured_sections(self.audit, "ux-technical", False))
        perf = self.scans("perf-a11y.json")
        self.assertIn(str(perf["perf"]["vitals"]["lcp"]), html)
        self.assertIn(str(perf["a11y"]["violations"]), html)
        self.assertIn(str(perf["perf"]["ttfb"]), html)
        self.assertIn(str(perf["keyboard"]["tabStops"]), html)
        self.assertIn(perf["a11y"]["top"][0]["id"], html)
        self.assertIn(perf["security"]["tls"], html)

    def test_pills_follow_benchmark_thresholds(self):
        html = joined(measured_sections(self.audit, "ux-technical", False))
        # fixture: LCP 10788 ms is poor, CLS 0 is good
        self.assertIn('<span class="pill gap">poor</span>', html)
        self.assertIn('<span class="pill covered">good</span>', html)
        perf = clone(self.scans("perf-a11y.json"))
        perf["perf"]["vitals"].update(lcp=3000, cls=0.2, fcp=1000, tbt=300)
        perf["perf"]["ttfb"] = 500
        run = dataclasses.replace(self.audit, scans={"perf-a11y.json": perf})
        out = joined(measured_sections(run, "ux-technical", False))
        self.assertEqual(out.count("needs work"), 3)

    def test_security_headers_present_and_missing(self):
        html = joined(measured_sections(self.audit, "ux-technical", False))
        for h in self.scans("perf-a11y.json")["security"]["headers"]:
            self.assertIn(h, html)

    def test_mobile_widths_shown(self):
        html = joined(measured_sections(self.audit, "ux-technical", False))
        for w in ("320", "390", "414"):
            self.assertIn(f"{w}px", html)

    def test_mobile_screenshot_only_when_file_exists(self):
        out = joined(measured_sections(self.audit, "ux-technical", False))
        self.assertNotIn("mobile-320.png", out)
        run_dir = self.tmpdir()
        (run_dir / "mobile-320.png").write_bytes(b"x")
        run = dataclasses.replace(self.audit, dir=run_dir)
        self.assertIn('src="mobile-320.png"', joined(measured_sections(run, "ux-technical", False)))
        self.assertIn('src="assets/mobile-320.png"', joined(measured_sections(run, "ux-technical", True)))
        self.assertNotIn("mobile-390.png", joined(measured_sections(run, "ux-technical", True)))

    def test_tracking_and_interaction(self):
        sections = measured_sections(self.audit, "conversion", False)
        html = joined(sections)
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0][0], "Measurement readiness &amp; interaction (measured)")
        self.assertIn(self.scans("tracking.json")["analytics"]["ga4"][0], html)
        self.assertIn(str(self.scans("interaction.json")["links"]["checked"]), html)
        self.assertIn("Microsoft Clarity", html)
        self.assertIn(self.scans("tracking.json")["cookies"]["names"][0], html)

    def test_interaction_form_and_cta(self):
        html = joined(measured_sections(self.audit, "conversion", False))
        self.assertIn("none detected above the fold", html)
        self.assertIn("3 fields", html)
        self.assertIn("Send", html)

    def test_seo_sweep_section(self):
        sections = measured_sections(self.audit, "seo", False)
        self.assertEqual(sections[0][0], "Site structure &amp; structured data (measured)")
        html = joined(sections)
        self.assertIn("Organization", html)
        self.assertNotIn("<th>Title len</th>", html)  # rows is empty
        sweep = clone(self.scans("seo-sweep.json"))
        sweep["rows"] = [
            {"url": "https://x.test/a", "ok": True, "type": "about", "title_len": 12, "desc_len": 99,
             "h1_count": 1, "words": 300, "imgs_alt": 2, "imgs": 3, "schema": 1, "flags": ["no canonical"]},
            {"url": "https://x.test/b", "ok": False, "status": 404, "type": "blog"}]
        audit = dataclasses.replace(self.audit, scans={"seo-sweep.json": sweep})
        out = joined(measured_sections(audit, "seo", False))
        self.assertIn("<th>Title len</th>", out)
        self.assertIn("no canonical", out)
        self.assertIn("2/3", out)
        self.assertIn("404", out)

    def test_screenshot_paths(self):
        run_dir = self.tmpdir()
        (run_dir / "design-desktop.png").write_bytes(b"x")
        run = dataclasses.replace(self.audit, dir=run_dir)
        draft = joined(measured_sections(run, "design", False))
        self.assertIn('src="design-desktop.png"', draft)
        self.assertNotIn("design-mobile.png", draft)  # file missing, left out
        self.assertIn('src="assets/design-desktop.png"', joined(measured_sections(run, "design", True)))

    def test_design_tokens_shown(self):
        sections = measured_sections(self.audit, "design", False)
        self.assertEqual(sections[0][0], "Design tokens &amp; rendered screenshots (measured)")
        html = joined(sections)
        self.assertIn("Roboto", html)
        self.assertIn("rgb(247, 236, 31)", html)
        self.assertNotIn("rgba(97, 206, 112, 0)", html)  # transparent colours are not swatches

    def test_design_pages_consistency(self):
        pages = {"consistency": {
            "pages": 2, "primaryFonts": ["Inter"], "fontsConsistent": False,
            "buttonStylesUnion": 7, "paletteUnion": 9,
            "perPage": [{"url": "https://x.test/", "font": "Inter", "fontSizes": 8, "buttonStyles": 3},
                        {"url": "https://x.test/about", "font": "Inter", "fontSizes": 11, "buttonStyles": 5}]}}
        run = dataclasses.replace(self.audit, scans={**self.audit.scans, "design-pages.json": pages})
        html = joined(measured_sections(run, "design", False))
        self.assertIn("Across 2 pages", html)
        self.assertIn("/about", html)
        self.assertIn("drift", html)
        self.assertIn("Inter", html)

    def test_design_pages_missing_fonts_consistent_not_recorded(self):
        pages = {"consistency": {"pages": 2, "primaryFonts": ["Inter"], "perPage": []}}
        run = dataclasses.replace(self.audit, scans={**self.audit.scans, "design-pages.json": pages})
        html = joined(measured_sections(run, "design", False))
        self.assertNotIn("drift", html)
        self.assertIn("not recorded", html)

    def test_partial_page_names_missing_scan_checks(self):
        run = dataclasses.replace(self.audit, scans={"perf-a11y.json": self.scans("perf-a11y.json")})
        md = joined_md(measured_sections(run, "ux-technical", False))
        html = joined(measured_sections(run, "ux-technical", False))
        for check in ("Mobile fit at 320, 390 and 414px", "Tap targets and text size on mobile"):
            self.assertIn(f"{check} — {NOT_MEASURED}", html)
            self.assertIn(f"{check} — {NOT_MEASURED}", md)
        self.assertNotIn("Core Web Vitals (LCP, CLS, FCP, TTFB, INP proxy) — " + NOT_MEASURED, html)

    def test_basic_run_not_measured(self):
        for page in ("conversion", "seo", "ux-technical", "design"):
            sections = measured_sections(self.basic, page, False)
            self.assertEqual(len(sections), 1)
            self.assertEqual(sections[0][0], "Measured checks")
            self.assertIn(NOT_MEASURED, sections[0][1])
            self.assertIn(NOT_MEASURED, sections[0][2])

    def test_messaging_has_no_measured_section(self):
        self.assertEqual(measured_sections(self.audit, "messaging", False), [])
        self.assertEqual(measured_sections(self.basic, "messaging", False), [])

    def test_missing_keys_do_not_crash(self):
        scans = {n: {} for n in self.audit.scans}
        run = dataclasses.replace(self.audit, scans=scans)
        for page in ("conversion", "seo", "ux-technical", "design"):
            self.assertTrue(measured_sections(run, page, True))

    def test_empty_scans_state_no_invented_measurements(self):
        run = dataclasses.replace(self.audit, scans={n: {} for n in self.audit.scans}, dir=self.tmpdir())
        for page in ("conversion", "seo", "ux-technical", "design"):
            out = joined(measured_sections(run, page, False)) + joined_md(measured_sections(run, page, False))
            for bad in ("0 broken", "0 checked", ">none<", ": none", "0 tracker", "0 http", ">no<", "| no |",
                        "0 form tags"):
                self.assertNotIn(bad, out, f"{page}: {bad}")
            if page == "conversion":
                self.assertIn("not recorded", out)

    def test_empty_list_is_distinct_from_absent_key(self):
        out = joined(measured_sections(self.audit, "conversion", False))
        self.assertIn("0 broken", out)  # fixture records broken: []
        self.assertIn("none detected", out)  # fixture records cmp: []

    def _with(self, name, **patch):
        scan = clone(self.scans(name))
        scan.update(patch)
        return dataclasses.replace(self.audit, scans={name: scan})

    def test_page_row_without_keys_is_not_recorded(self):
        run = self._with("interaction.json", pages=[{"url": "https://x.test/p"}])
        out = joined(measured_sections(run, "conversion", False))
        self.assertEqual(out.count("not recorded"), 2)  # CTA and form cells
        self.assertNotIn("no form", out)
        self.assertNotIn("none detected above the fold", out)

    def test_page_row_explicit_negatives(self):
        run = self._with("interaction.json", pages=[
            {"url": "https://x.test/p", "cta": None, "form": None, "formsOnPage": 0}])
        out = joined(measured_sections(run, "conversion", False))
        self.assertIn("none detected above the fold", out)
        self.assertIn("no form", out)
        self.assertIn("0 form tags", out)
        form = {"url": "https://x.test/q", "cta": None, "form": {"fields": 2, "required": 1}}
        out = joined(measured_sections(self._with("interaction.json", pages=[form]), "conversion", False))
        self.assertIn("blocks empty submit: not recorded", out)
        form["form"]["blocksEmptySubmit"] = False
        out = joined(measured_sections(self._with("interaction.json", pages=[form]), "conversion", False))
        self.assertIn("blocks empty submit: no", out)

    def test_mobile_fits_absent_vs_false(self):
        run = self._with("mobile-metrics.json", widths={"320": {}, "390": {"fits": False}, "414": {"fits": True}})
        out = joined(measured_sections(run, "ux-technical", False))
        self.assertEqual(out.count("overflows"), 1)
        self.assertEqual(out.count(">fits<"), 1)
        self.assertIn("not recorded", out)

    def test_screenshot_name_must_be_plain_file_in_run_folder(self):
        outer = self.tmpdir()
        run_dir = outer / "run"
        run_dir.mkdir()
        (outer / "x.png").write_bytes(b"x")
        run = dataclasses.replace(self.audit, dir=run_dir)
        for name in ("../x.png", str(outer / "x.png"), "sub/x.png", "..\\x.png"):
            scan = clone(self.scans("mobile-metrics.json"))
            scan["widths"]["320"]["screenshot"] = name
            run = dataclasses.replace(run, scans={"mobile-metrics.json": scan})
            self.assertNotIn("<img", joined(measured_sections(run, "ux-technical", False)), name)

    def test_cta_and_form_of_wrong_type_not_recorded(self):
        for bad in ("x", 0, []):
            run = self._with("interaction.json", pages=[{"url": "https://x.test/p", "cta": bad, "form": bad}])
            out = joined(measured_sections(run, "conversion", False))
            self.assertEqual(out.count("not recorded"), 2, bad)
            self.assertNotIn("no form", out)
            self.assertNotIn("none detected above the fold", out)

    def test_mobile_fits_non_bool_not_recorded(self):
        run = self._with("mobile-metrics.json", widths={"320": {"fits": "false"}})
        out = joined(measured_sections(run, "ux-technical", False))
        self.assertIn("not recorded", out)
        self.assertNotIn("overflows", out)
        self.assertNotIn(">fits<", out)

    def test_fired_categories_partial_and_non_numeric(self):
        for fired in ({"analytics": 2}, {"marketing": 1}, {"analytics": "x", "marketing": 1}, {}):
            run = self._with("tracking.json", consentMode=False, firedOnLoadByCategory=fired)
            out = joined(measured_sections(run, "conversion", False))
            self.assertNotIn("tracker(s) fire", out, fired)
        run = self._with("tracking.json", consentMode=False,
                         firedOnLoadByCategory={"analytics": 2, "marketing": 0})
        self.assertIn("2 tracker(s) fire before consent", joined(measured_sections(run, "conversion", False)))
        run = self._with("tracking.json", consentMode=False,
                         firedOnLoadByCategory={"analytics": 0, "marketing": 0})
        self.assertIn("0 tracker(s) fire before consent", joined(measured_sections(run, "conversion", False)))

    def test_design_pages_loaded_from_scans(self):
        from report import SCAN_FILES
        self.assertIn("design-pages.json", SCAN_FILES)
        self.assertEqual(len(SCAN_FILES), 7)

    def test_design_pages_json_loads_through_load_run(self):
        run_dir = self.tmp / "design-pages-run"
        shutil.copytree(FIXTURE, run_dir)
        payload = {"pages": [{"url": "https://example.com/", "typeface": "Inter"}]}
        (run_dir / "design-pages.json").write_text(json.dumps(payload), encoding="utf-8")
        self.assertEqual(load_run(run_dir).scans["design-pages.json"], payload)

    def test_values_are_escaped(self):
        trk = clone(self.scans("tracking.json"))
        trk["cmp"] = ["<script>alert(1)</script>"]
        run = dataclasses.replace(self.audit, scans={"tracking.json": trk})
        html = joined(measured_sections(run, "conversion", False))
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_markdown_output(self):
        md = joined_md(measured_sections(self.audit, "ux-technical", False))
        self.assertIn(str(self.scans("perf-a11y.json")["perf"]["vitals"]["lcp"]), md)
        self.assertNotIn("<span", md)
        self.assertIn("320px", md)

    def test_render_dimension_wires_sections_in_order(self):
        html, md = render_dimension(self.audit, "ux-technical", self.keymap, False)
        title = "Measured checks — performance, INP, security, accessibility &amp; mobile"
        self.assertIn(title, html)
        heads = re.findall(r'<h2 class="section">(?:<span class="no">\d+</span> )?(.*?)(?:<a|</h2>)', html)
        self.assertEqual(heads.index(title), heads.index("Findings") + 1)
        self.assertIn("## Measured checks — performance, INP, security, accessibility & mobile", md)
        self.assertLess(md.index("## Findings"), md.index("## Measured checks"))
        html, md = render_dimension(self.audit, "messaging", self.keymap, False)
        self.assertNotIn("(measured)", html)


if __name__ == "__main__":
    unittest.main()
