"""Tests for scripts/setup-check.py: which mode (extended, basic, unsupported) a machine gets."""
import json
import pathlib
import subprocess
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO, load_script  # noqa: E402

sc = load_script("scripts/setup-check.py")


class SetupCheckTest(unittest.TestCase):
    def test_python_below_minimum_is_not_ok(self):
        r = sc.check_python((3, 8))
        self.assertFalse(r["ok"])
        self.assertEqual(r["minimum"], "3.9")

    def test_python_at_minimum_is_ok(self):
        self.assertTrue(sc.check_python((3, 9))["ok"])

    def test_install_commands_without_playwright(self):
        self.assertEqual(
            sc.install_commands("/usr/bin/python3", False),
            ['"/usr/bin/python3" -m pip install playwright', '"/usr/bin/python3" -m playwright install chromium'],
        )

    def test_install_commands_with_playwright_only_browser(self):
        self.assertEqual(sc.install_commands("/usr/bin/python3", True), ['"/usr/bin/python3" -m playwright install chromium'])

    def test_install_commands_quote_paths_with_spaces(self):
        first = sc.install_commands("C:/Program Files/Python/python.exe", False)[0]
        self.assertTrue(first.startswith('"C:/Program Files/Python/python.exe" -m pip'), first)

    def test_decide_mode(self):
        ok, bad = {"ok": True}, {"ok": False}
        self.assertEqual(sc.decide_mode(bad, {"installed": True}, ok), "unsupported")
        self.assertEqual(sc.decide_mode(ok, {"installed": True}, ok), "extended")
        self.assertEqual(sc.decide_mode(ok, {"installed": False}, bad), "basic")
        self.assertEqual(sc.decide_mode(ok, {"installed": True}, bad), "basic")

    def test_chromium_check_times_out(self):
        r = sc.check_chromium(timeout=1, cmd=[sys.executable, "-c", "import time; time.sleep(5)"])
        self.assertFalse(r["ok"])
        self.assertIn("timed out", r["error"])

    def test_boxed_playwright_error_keeps_message(self):
        boxed = ("playwright._impl._errors.Error: BrowserType.launch:\n"
                 "╔══════════════════════════════════════════════════════╗\n"
                 "║ Host system is missing dependencies to run browsers. ║\n"
                 "║ Please install them with the following command:      ║\n"
                 "║                                                      ║\n"
                 "║     sudo playwright install-deps                     ║\n"
                 "╚══════════════════════════════════════════════════════╝\n").encode("utf-8")
        code = f"import sys; sys.stderr.buffer.write({boxed!r}); sys.exit(1)"
        r = sc.check_chromium(timeout=30, cmd=[sys.executable, "-c", code])
        self.assertFalse(r["ok"])
        self.assertIn("missing dependencies", r["error"])
        self.assertNotIn("╚", r["error"])
        self.assertTrue(r["needs_deps"])

    def test_install_commands_add_deps_when_missing(self):
        self.assertEqual(sc.install_commands("/usr/bin/python3", True, needs_deps=True),
                         ['"/usr/bin/python3" -m playwright install chromium',
                          '"/usr/bin/python3" -m playwright install-deps chromium'])

    def test_install_commands_externally_managed_python(self):
        self.assertEqual(sc.install_commands("/usr/bin/python3", False, externally_managed=True)[0],
                         '"/usr/bin/python3" -m pip install --user --break-system-packages playwright')

    def test_install_commands_without_pip(self):
        cmds = sc.install_commands("/usr/bin/python3", False, has_pip=False, platform="linux")
        self.assertTrue(cmds[0].startswith("sudo apt install python3-pip"), cmds[0])

    def test_install_commands_without_pip_on_windows(self):
        cmds = sc.install_commands("C:/Py/python.exe", False, has_pip=False, platform="win32")
        self.assertEqual(cmds[0], '"C:/Py/python.exe" -m ensurepip --upgrade')

    def test_main_survives_missing_importlib_metadata(self):
        # Python 3.6/3.7 have no importlib.metadata; the check must still reach its version test.
        code = ("import sys, runpy; sys.modules['importlib.metadata'] = None; "
                f"sys.argv = ['setup-check.py', '--json']; runpy.run_path({str(REPO / 'scripts/setup-check.py')!r}, run_name='__main__')")
        p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
        self.assertEqual(p.returncode, 0, p.stderr[-500:])
        self.assertIn(json.loads(p.stdout)["mode"], {"extended", "basic"})

    def test_script_avoids_future_annotations(self):
        # `from __future__ import annotations` is a SyntaxError on Python 3.6, before the version check runs.
        self.assertNotIn("from __future__ import annotations", (REPO / "scripts/setup-check.py").read_text(encoding="utf-8"))

    def test_main_json_on_this_machine(self):
        p = subprocess.run([sys.executable, str(REPO / "scripts/setup-check.py"), "--json"],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn(json.loads(p.stdout)["mode"], {"extended", "basic"})


if __name__ == "__main__":
    unittest.main()
