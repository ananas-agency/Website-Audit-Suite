#!/usr/bin/env python3
"""Website Audit Suite setup check: can this machine run the measured scans?

Prints one line each for Python, Playwright and the browser, the install commands when something is
missing, and a last line `MODE: extended | basic | unsupported`. `--json` prints the same as one JSON
object. Exit code is 1 only when Python is too old. Standard library only, and written so that Python
3.6+ reaches the version check (typing annotations instead of a future import, lazy importlib.metadata).

    python scripts/setup-check.py [--json]
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import sysconfig
from typing import List, Optional, Tuple

MIN_PYTHON = (3, 9)

# Runs in a child process so a hanging first launch can be timed out.
CHROMIUM_CODE = (
    "from playwright.sync_api import sync_playwright\n"
    "with sync_playwright() as p:\n"
    "    b = p.chromium.launch(headless=True)\n"
    "    page = b.new_page()\n"
    "    page.goto('data:text/html,<title>ok</title>')\n"
    "    print(page.title())\n"
    "    b.close()\n"
)

# Playwright wraps its launch errors in a box drawn with these characters.
BOX_CHARS = re.compile(r"[\u2500-\u257f]")


def check_python(version: Tuple[int, int]) -> dict:
    major, minor = version[0], version[1]
    return {
        "ok": (major, minor) >= MIN_PYTHON,
        "version": f"{major}.{minor}",
        "minimum": ".".join(str(n) for n in MIN_PYTHON),
    }


def check_playwright() -> dict:
    """Is the Playwright package importable? Doesn't start a browser."""
    if importlib.util.find_spec("playwright") is None:
        return {"installed": False, "version": None}
    try:
        import importlib.metadata as metadata  # Python 3.8+
        version = metadata.version("playwright")
    except Exception:
        version = None
    return {"installed": True, "version": version}


def clean_error(text: str) -> str:
    """Keep the message lines of a (possibly boxed) Playwright error, without the border."""
    lines = [BOX_CHARS.sub("", line).strip() for line in text.splitlines()]
    return " / ".join(line for line in lines if line)[:500]


def check_chromium(timeout: int = 60, cmd: Optional[List[str]] = None) -> dict:
    """Start headless Chromium in a child process and render a one-line page."""
    cmd = cmd or [sys.executable, "-c", CHROMIUM_CODE]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timed out after {timeout}s", "needs_deps": False}
    except OSError as e:
        return {"ok": False, "error": str(e)[:300], "needs_deps": False}
    if "ok" in proc.stdout:
        return {"ok": True, "error": None, "needs_deps": False}
    raw = proc.stderr or proc.stdout
    needs_deps = bool(re.search(r"install-deps|missing dependencies", raw, re.I))
    return {"ok": False, "error": clean_error(raw) or f"exit code {proc.returncode}", "needs_deps": needs_deps}


def pip_situation() -> dict:
    """Can this interpreter pip-install, and does it refuse system-wide installs (PEP 668)?"""
    in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    marker = os.path.join(sysconfig.get_path("stdlib"), "EXTERNALLY-MANAGED")
    return {
        "has_pip": importlib.util.find_spec("pip") is not None,
        "externally_managed": os.path.exists(marker) and not in_venv,
    }


def install_commands(executable: str, playwright_installed: bool, needs_deps: bool = False,
                     externally_managed: bool = False, has_pip: bool = True,
                     platform: str = sys.platform) -> List[str]:
    """Commands that use the interpreter running this check, quoted for paths with spaces."""
    exe = f'"{executable}"'
    cmds = []
    if not playwright_installed:
        if not has_pip:
            if platform.startswith("linux"):  # Debian/Ubuntu strip ensurepip from the system Python
                cmds.append("sudo apt install python3-pip   # Debian/Ubuntu; elsewhere install pip for this Python")
            else:
                cmds.append(f"{exe} -m ensurepip --upgrade")
        extra = "--user --break-system-packages " if externally_managed else ""
        cmds.append(f"{exe} -m pip install {extra}playwright")
    cmds.append(f"{exe} -m playwright install chromium")
    if needs_deps:
        cmds.append(f"{exe} -m playwright install-deps chromium")
    return cmds


def decide_mode(py: dict, pw: dict, chromium: dict) -> str:
    if not py["ok"]:
        return "unsupported"
    if pw["installed"] and chromium["ok"]:
        return "extended"
    return "basic"


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Can this machine run the Website Audit Suite's measured scans?")
    ap.add_argument("--json", action="store_true", help="print one JSON object instead of text")
    args = ap.parse_args(argv)

    py = check_python(tuple(sys.version_info[:2]))
    pw = check_playwright()
    if py["ok"] and pw["installed"]:
        chromium = check_chromium()
    else:
        note = "not checked: Playwright not installed" if py["ok"] else "not checked"
        chromium = {"ok": False, "error": note, "needs_deps": False}
    mode = decide_mode(py, pw, chromium)
    pip = pip_situation()
    install = []
    if mode == "basic":
        install = install_commands(sys.executable, pw["installed"], needs_deps=chromium["needs_deps"], **pip)

    if args.json:
        print(json.dumps({"mode": mode, "python": py, "playwright": pw, "chromium": chromium,
                          "pip": pip, "install": install}))
    else:
        state = "OK" if py["ok"] else "too old"
        print(f"Python: {py['version']} ({state}, minimum {py['minimum']})")
        print(f"Playwright: {pw['version'] or 'unknown version'} installed" if pw["installed"] else "Playwright: not installed")
        print("Browser (Chromium): starts" if chromium["ok"] else f"Browser (Chromium): not available ({chromium['error']})")
        if install:
            print("To turn on the measured scans, run:")
            for c in install:
                print(f"  {c}")
        print(f"MODE: {mode}")
    return 1 if mode == "unsupported" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
