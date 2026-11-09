"""The scan scripts print their usage on --help or with no URL; they never scan a default site."""
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

HAS_PLAYWRIGHT = importlib.util.find_spec("playwright") is not None
PLAYWRIGHT_SCANS = ["perf-a11y-scan.py", "mobile-audit.py", "tracking-scan.py", "design-scan.py", "interaction-scan.py"]
STDLIB_SCANS = ["seo-sweep.py", "security-scan.py", "security-report.py"]  # no Playwright needed, so these cases always run


class ScanUsageTest(unittest.TestCase):
    def check_usage(self, script):
        for args in (["--help"], ["-h"], []):
            with self.subTest(script=script, args=args), tempfile.TemporaryDirectory() as tmp:
                r = subprocess.run(
                    [sys.executable, str(REPO / "scripts" / script), *args],
                    cwd=tmp, capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                self.assertIn("usage:", r.stdout)
                self.assertEqual(list(pathlib.Path(tmp).iterdir()), [])

    @unittest.skipUnless(HAS_PLAYWRIGHT, "Playwright is not installed; the scans exit 3 before main() runs")
    def test_playwright_scans_print_usage_on_help(self):
        for script in PLAYWRIGHT_SCANS:
            self.check_usage(script)

    def test_stdlib_scans_print_usage_on_help(self):
        for script in STDLIB_SCANS:
            self.check_usage(script)


if __name__ == "__main__":
    unittest.main()
