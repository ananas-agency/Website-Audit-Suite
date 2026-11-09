import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

FIXTURE = REPO / "tests" / "fixtures" / "sample-run"
SCRIPT = REPO / "scripts" / "build-report.py"
REPORT = "_ananas-agency-website-audit-report"


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = pathlib.Path(self.tmp.name) / "run"
        shutil.copytree(FIXTURE, self.dir)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.dir), *args],
                              capture_output=True, text=True, encoding="utf-8")

    def drop_measured_flags(self):
        """Remove measured: true from every finding (a run without scans can't claim them)."""
        for name in ("conversion", "ux-technical"):
            path = self.dir / "audit-data" / f"{name}.json"
            d = json.loads(path.read_text(encoding="utf-8"))
            for f in d["findings"]:
                f.pop("measured", None)
            path.write_text(json.dumps(d), encoding="utf-8")

    def final(self):
        res = self.cli("--final")
        self.assertEqual(res.returncode, 0, res.stderr)
        return res

    def read(self, name):
        return (self.dir / name).read_text(encoding="utf-8")

    def test_page_writes_working_copy(self):
        res = self.cli("--page", "seo")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertNotIn('class="pagenav"', self.read("seo.html"))
        self.assertTrue((self.dir / "seo.md").is_file())
        self.assertFalse((self.dir / "messaging.html").exists())

    def test_page_missing_data_names_file(self):
        (self.dir / "audit-data" / "goals.json").unlink()
        res = self.cli("--page", "goals")
        self.assertEqual(res.returncode, 2)
        self.assertIn("goals.json", res.stderr)

    def test_unknown_page_exit_1(self):
        res = self.cli("--page", "nope")
        self.assertEqual(res.returncode, 1)
        self.assertIn("nope", res.stderr)

    def test_check_validates_only(self):
        res = self.cli("--check")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertFalse((self.dir / "seo.html").exists())

    def test_final_writes_pack_and_zip(self):
        res = self.final()
        zip_path = self.dir / "ananas-agency-website-audit.zip"
        self.assertTrue(zip_path.is_file())
        self.assertIn(str(zip_path), res.stdout)
        names = set(zipfile.ZipFile(zip_path).namelist())
        self.assertIn(REPORT + ".html", names)
        self.assertIn("data/perf-a11y.json", names)
        self.assertTrue(all("/" not in n for n in names if n.endswith((".html", ".md"))))
        self.assertFalse(any(n.startswith("audit-data") or n.endswith(".zip") for n in names))
        self.assertIn('class="pagenav"', self.read("seo.html"))

    def test_final_reports_tbds(self):
        res = self.final()
        self.assertIn("TBD left: Platform & signals / Platform / CMS", res.stdout)

    def test_non_ascii_run_path_and_tbd_label(self):
        base = pathlib.Path(self.tmp.name) / "ананас"
        shutil.copytree(FIXTURE, base)
        path = base / "audit-data" / "site-snapshot.json"
        path.write_text(path.read_text(encoding="utf-8").replace('"Platform / CMS"', '"Мова"'), encoding="utf-8")
        self.dir = base
        res = self.cli("--page", "seo")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("ананас", res.stdout)
        res = self.final()
        self.assertIn("TBD left: Platform & signals / Мова", res.stdout)

    def test_final_copies_screenshots_into_assets(self):
        names = ["design-desktop.png", "design-mobile.png", "page-home.png", "mobile-320.png", "mobile-390.png"]
        for n in names:
            (self.dir / n).write_bytes(b"png")
        self.final()
        for n in names:
            self.assertTrue((self.dir / "assets" / n).is_file(), n)
            self.assertTrue((self.dir / n).is_file(), n)
        checked = 0
        for p in self.dir.glob("*.html"):
            for src in re.findall(r'<img src="(assets/[^"]+)"', p.read_text(encoding="utf-8")):
                checked += 1
                self.assertTrue((self.dir / src).is_file(), f"{p.name}: {src}")
        self.assertGreater(checked, 0)

    def test_data_error_exit_code(self):
        path = self.dir / "audit-data" / "seo.json"
        text = path.read_text(encoding="utf-8")
        path.write_text(re.sub(r'"impact":\s*\d', '"impact": 9', text, count=1), encoding="utf-8")
        res = self.cli("--final")
        self.assertEqual(res.returncode, 2)
        self.assertIn("seo.json", res.stderr)
        self.assertIn("impact", res.stderr)

    def test_partial_run_overall_and_walk(self):
        data = self.dir / "audit-data"
        for name in ("conversion", "ux-technical", "design"):
            (data / f"{name}.json").unlink()
        kept = set()
        for name in ("messaging", "seo"):
            kept |= {f["key"] for f in json.loads((data / f"{name}.json").read_text(encoding="utf-8"))["findings"]}
        for name in ("goals", "action-report"):  # drop references to the removed dimensions' findings
            text = (data / f"{name}.json").read_text(encoding="utf-8")
            text = re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(0) if m.group(1) in kept else "it", text)
            obj = json.loads(text)
            for b in obj.get("benchmarks", []):
                b["keys"] = [k for k in b.get("keys", []) if k in kept]
            (data / f"{name}.json").write_text(json.dumps(obj), encoding="utf-8")
        self.final()
        action = self.read("action-report.html")
        text = html.unescape(re.sub(r"<[^>]+>", "", action))
        self.assertIn("from Messaging & Clarity and SEO & Content only", text)
        for missing in ("Conversion (CRO)", "UX & Technical", "Design & Visual"):
            self.assertIn(missing, text.split("only;")[1].split("not run")[0])
        self.assertRegex(self.read("goals.html"), r'class="nextbtn" href="messaging.html"')
        self.assertNotIn('href="conversion.html"', self.read(REPORT + ".html"))
        built = {p.name for p in self.dir.glob("*.html")}
        for p in self.dir.glob("*.html"):
            for href in re.findall(r'href="([^"#:]+\.html)"', p.read_text(encoding="utf-8")):
                self.assertIn(href, built, f"{p.name} links to {href}")

    def test_no_links_to_unbuilt_pages_without_snapshot_and_action(self):
        (self.dir / "audit-data" / "site-snapshot.json").unlink()
        (self.dir / "audit-data" / "action-report.json").unlink()
        self.final()
        built = {p.name for p in self.dir.glob("*.html")}
        for p in self.dir.glob("*.html"):
            for href in re.findall(r'href="([^"#:]+\.html)"', p.read_text(encoding="utf-8")):
                self.assertIn(href, built, f"{p.name} links to {href}")

    def extended_without_scans(self):
        for p in self.dir.glob("*.json"):
            p.unlink()
        audit = self.dir / "audit-data" / "audit.json"
        data = json.loads(audit.read_text(encoding="utf-8"))
        data["mode"] = "extended"
        audit.write_text(json.dumps(data), encoding="utf-8")
        for path in (self.dir / "audit-data").glob("*.json"):
            d = json.loads(path.read_text(encoding="utf-8"))
            for f in d.get("findings", []):
                f.pop("measured", None)
            path.write_text(json.dumps(d), encoding="utf-8")

    WARNING = "mode is extended but no scan results were found in the run folder"

    def test_extended_without_scans_warns_where_scans_should_exist(self):
        self.extended_without_scans()
        for args in (("--final",), ("--page", "messaging"), ("--page", "seo"), ("--page", "action-report")):
            with self.subTest(args=args):
                res = self.cli(*args)
                self.assertEqual(res.returncode, 0, res.stderr)
                self.assertIn(self.WARNING, res.stderr)

    def test_extended_without_scans_is_quiet_before_the_scans_run(self):
        self.extended_without_scans()
        for args in (("--page", "site-snapshot"), ("--page", "goals"), ("--check",)):
            with self.subTest(args=args):
                res = self.cli(*args)
                self.assertEqual(res.returncode, 0, res.stderr)
                self.assertEqual(res.stderr, "")

    def test_extended_with_scans_does_not_warn(self):
        res = self.cli("--check")
        self.assertEqual(res.returncode, 0)
        self.assertEqual(res.stderr, "")

    def _strip_dimensions(self):
        data = self.dir / "audit-data"
        for name in ("messaging", "conversion", "seo", "ux-technical", "design", "goals"):
            (data / f"{name}.json").unlink()
        path = data / "action-report.json"
        obj = json.loads(path.read_text(encoding="utf-8"))
        for b in obj["benchmarks"]:
            b.pop("keys", None)
        text = re.sub(r"\[\[[^\]]+\]\]", "it", json.dumps(obj))
        path.write_text(text, encoding="utf-8")

    def test_run_without_dimensions_says_no_analysis_ran(self):
        self._strip_dimensions()
        self.final()
        for name in ("action-report.html", "action-report.md", REPORT + ".html", REPORT + ".md"):
            text = self.read(name)
            self.assertNotIn("0/100", text, name)
            self.assertNotIn("from  only", text, name)
            self.assertNotIn("Overall F", text, name)
            self.assertIn("no analysis ran", text, name)

    def test_report_md_links_action_report_only_when_built(self):
        self.final()
        self.assertIn("See action-report.md", self.read(REPORT + ".md"))
        (self.dir / "audit-data" / "action-report.json").unlink()
        text = re.sub(r"\[\[[^\]]+\]\]", "it",
                      (self.dir / "audit-data" / "goals.json").read_text(encoding="utf-8"))
        (self.dir / "audit-data" / "goals.json").write_text(text, encoding="utf-8")
        self.final()
        self.assertNotIn("See action-report.md", self.read(REPORT + ".md"))

    def test_usage_errors_exit_1(self):
        self.assertEqual(self.cli().returncode, 1)
        self.assertEqual(self.cli("--final", "--check").returncode, 1)
        res = subprocess.run([sys.executable, str(SCRIPT), "--final"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 1)

    def test_run_with_no_findings_builds_every_page(self):
        def clear(o):
            if isinstance(o, str):
                return re.sub(r"\[\[[^\]]*\]\]", "the page", o)
            if isinstance(o, list):
                return [clear(x) for x in o]
            if isinstance(o, dict):
                return {k: clear(v) for k, v in o.items()}
            return o
        for path in (self.dir / "audit-data").glob("*.json"):
            d = json.loads(path.read_text(encoding="utf-8"))
            if "findings" in d:
                d["findings"] = []
            for b in d.get("benchmarks", []):
                b["keys"] = []
            path.write_text(json.dumps(clear(d)), encoding="utf-8")
        self.final()
        action, report = self.read("action-report.html"), self.read(REPORT + ".html")
        for html_text in (action, report):
            self.assertNotIn("Biggest opportunity", html_text)
            self.assertNotIn("Top 3 quick wins", html_text)
        self.assertNotIn("Biggest opportunity", self.read("action-report.md"))
        self.assertNotRegex(action, r"(?:MSG|CRO|SEO|UX|DSN)-\d\d")

    def test_zip_basic_run_has_no_evidence_folders(self):
        for f in self.dir.glob("*.json"):
            f.unlink()
        for name in ("other.png", "notes.png", "logo.png"):  # PNGs the zip never takes
            (self.dir / name).write_bytes(b"x")
        self.drop_measured_flags()  # a run without scans can't mark findings measured
        self.final()
        names = zipfile.ZipFile(self.dir / "ananas-agency-website-audit.zip").namelist()
        self.assertFalse(any(n.startswith(("assets/", "data/")) for n in names), names)

    def test_zip_includes_assets(self):
        (self.dir / "design-desktop.png").write_bytes(b"x")
        (self.dir / "page-home.png").write_bytes(b"x")
        (self.dir / "other.png").write_bytes(b"x")
        self.final()
        names = set(zipfile.ZipFile(self.dir / "ananas-agency-website-audit.zip").namelist())
        self.assertIn("assets/design-desktop.png", names)
        self.assertIn("assets/page-home.png", names)
        self.assertNotIn("assets/other.png", names)

    def test_no_bare_ids_and_no_raw_keys(self):
        self.final()
        dims = {"messaging": "MSG", "conversion": "CRO", "seo": "SEO", "ux-technical": "UX", "design": "DSN"}
        for p in self.dir.glob("*.html"):
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("[[", text, p.name)
            body = re.sub(r"<style>.*?</style>", "", text, flags=re.S)
            body = re.sub(r"<a [^>]*title=[^>]*>.*?</a>", "", body, flags=re.S)
            body = re.sub(r"<[^>]+>", " ", body)
            own = dims.get(p.stem)
            for m in re.finditer(r"\b(MSG|CRO|SEO|UX|DSN)-\d\d\b", body):
                self.assertEqual(m.group(1), own, f"{p.name}: bare {m.group(0)}")

    def test_dimension_without_findings_builds(self):
        path = self.dir / "audit-data" / "messaging.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["findings"] = []
        path.write_text(json.dumps(data), encoding="utf-8")
        for other in (self.dir / "audit-data").glob("*.json"):  # nothing may cite the removed finding
            text = other.read_text(encoding="utf-8")
            other.write_text(text.replace("[[hero]]", "the hero section"), encoding="utf-8")
        self.final()
        self.assertIn("No findings in this dimension.", self.read("messaging.html"))
        self.assertNotIn("Top priority", self.read("messaging.html"))
        self.assertNotIn("Top priority", self.read("messaging.md"))


if __name__ == "__main__":
    unittest.main()
