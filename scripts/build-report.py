#!/usr/bin/env python3
"""Website Audit Suite report builder.

    python scripts/build-report.py RUN_DIR (--page NAME | --final | --check)

--check validates the audit data only. --page renders one working copy (no page navigation).
--final renders every page that has data plus the report, then the ZIP. Exit codes: 0 success,
2 data errors (one per line on stderr), 1 usage error.
"""
import argparse
import shutil
import sys
from pathlib import Path

from report import DIMENSIONS
from report.bundle import make_zip
from report.chrome import page_file, write_page
from report.data import DataError, load_run
from report.pages_action import render_action, render_report
from report.pages_dim import render_dimension
from report.pages_intake import render_goals, render_snapshot, tbd_labels
from report.rules import apply_rules

DIM_NAMES = [d[0] for d in DIMENSIONS]
PAGES = ["site-snapshot", "goals"] + DIM_NAMES + ["action-report"]
DATA_FILE = {"site-snapshot": "site-snapshot.json", "goals": "goals.json", "action-report": "action-report.json"}
DATA_FILE.update({d: f"{d}.json" for d in DIM_NAMES})


def has_data(run, name):
    if name == "site-snapshot":
        return run.snapshot is not None
    if name == "goals":
        return run.goals is not None
    if name == "action-report":
        return run.action is not None
    return name in run.dims


def copy_screenshots(run_dir):
    """The final pages reference assets/*.png, so give the run folder its own assets/ copies
    (originals stay, so working copies keep resolving)."""
    pngs = [run_dir / n for n in ("design-desktop.png", "design-mobile.png") if (run_dir / n).is_file()]
    pngs += sorted(run_dir.glob("page-*.png")) + sorted(run_dir.glob("mobile-*.png"))
    if pngs:
        (run_dir / "assets").mkdir(exist_ok=True)
        for p in pngs:
            shutil.copyfile(p, run_dir / "assets" / p.name)


def render(run, keymap, name, final):
    if name == "site-snapshot":
        return render_snapshot(run, final)
    if name == "goals":
        return render_goals(run, keymap, final)
    if name == "action-report":
        return render_action(run, keymap, final)
    return render_dimension(run, name, keymap, final)


class _Parser(argparse.ArgumentParser):
    def error(self, message):  # usage errors exit 1 (2 is reserved for data errors)
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        sys.exit(1)


def main(argv):
    for stream in (sys.stdout, sys.stderr):  # a pipe on Windows defaults to cp1252
        stream.reconfigure(encoding="utf-8", errors="replace")
    ap = _Parser(prog="build-report.py", description=__doc__.split("\n")[0])
    ap.add_argument("run_dir")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--page", metavar="NAME", help="one of: " + ", ".join(PAGES))
    mode.add_argument("--final", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    if args.page is not None and args.page not in PAGES:
        print(f"unknown page '{args.page}'; expected one of: {', '.join(PAGES)}", file=sys.stderr)
        return 1
    run_dir = Path(args.run_dir)
    if not run_dir.is_dir():
        print(f"run folder not found: {run_dir}", file=sys.stderr)
        return 1
    try:
        run = load_run(run_dir)
        if args.page is not None and not has_data(run, args.page):
            raise DataError([f"{DATA_FILE[args.page]}: required for --page {args.page} but not found in audit-data/"])
    except DataError as exc:
        for line in exc.errors:
            print(line, file=sys.stderr)
        return 2

    # Site Snapshot and Goals build before the scans launch, so only later pages and the final build warn.
    if run.mode == "extended" and not run.scans and (args.final or args.page in DIM_NAMES + ["action-report"]):
        print("mode is extended but no scan results were found in the run folder "
              '(the scans write there with `--out "audit-<slug>"`)', file=sys.stderr)

    if args.check:
        print("OK")
        return 0
    keymap = apply_rules(run)
    if args.page is not None:
        html_text, md_text = render(run, keymap, args.page, False)
        write_page(run_dir, args.page, html_text, md_text)
        print(run_dir / f"{args.page}.html")
        return 0

    for name in PAGES:
        if has_data(run, name):
            html_text, md_text = render(run, keymap, name, True)
            write_page(run_dir, name, html_text, md_text)
    html_text, md_text = render_report(run, keymap)
    write_page(run_dir, page_file(run, "report"), html_text, md_text)
    copy_screenshots(run_dir)
    print(make_zip(run))
    for label in tbd_labels(run):
        print(f"TBD left: {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
