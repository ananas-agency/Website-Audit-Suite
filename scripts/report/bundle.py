"""The deliverable ZIP: pages flat at the root, PNGs in assets/, scan JSON in data/."""
from __future__ import annotations

import zipfile
from pathlib import Path

from . import SCAN_FILES
from .chrome import page_file, walk


def make_zip(run) -> Path:
    run_dir = Path(run.dir)
    out = run_dir / f"{run.slug}-website-audit.zip"
    entries = []
    for name in walk(run):
        base = page_file(run, name)
        for ext in (".md", ".html"):
            if (run_dir / (base + ext)).is_file():
                entries.append((run_dir / (base + ext), base + ext))
    for name in SCAN_FILES:
        if (run_dir / name).is_file():
            entries.append((run_dir / name, f"data/{name}"))
    pngs = [run_dir / n for n in ("design-desktop.png", "design-mobile.png") if (run_dir / n).is_file()]
    pngs += sorted(run_dir.glob("page-*.png")) + sorted(run_dir.glob("mobile-*.png"))
    entries += [(p, f"assets/{p.name}") for p in pngs]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for src, arc in entries:
            zf.write(src, arc)
    return out
