#!/usr/bin/env python3
"""Repack every unpacked skill folder back into its .skill archive.

Run from anywhere:  python scripts/repack-all-skills.py

For each entry below it zips  <folder>/<slug>/  ->  <folder>/<slug>.skill
with forward-slash internal paths (matching the original archives), then
removes the DO_NOT_FORGET_TO_REZIP.md marker for that folder.
"""
import zipfile
import os

# repo root = parent of this scripts/ folder
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPECS = [
    ("0 Site Snapshot", "site-snapshot", "rules-snapshot.md"),
    ("1 Goals Discovery", "goals-discovery", "rules-goals-discovery.md"),
    ("2 Messaging Clarity", "messaging-clarity", "rules-messaging-clarity.md"),
    ("3 Conversion CRO", "conversion-cro", "rules-conversion.md"),
    ("4 SEO Content", "seo-content", "rules-seo.md"),
    ("5 UX Technical", "ux-technical", "rules-ux-technical.md"),
    ("6 Design Visual", "design-visual", "rules-design-visual.md"),
    ("7 Action Report", "action-report", "rules-action-report.md"),
]


def main():
    for folder, slug, rules in SPECS:
        fdir = os.path.join(BASE, folder)
        srcdir = os.path.join(fdir, slug)
        skill_md = os.path.join(srcdir, "SKILL.md")
        rules_md = os.path.join(srcdir, "references", rules)
        if not (os.path.exists(skill_md) and os.path.exists(rules_md)):
            print(f"SKIP {slug}: unpacked files not found")
            continue
        out_zip = os.path.join(fdir, slug + ".skill")
        # Zip the whole unpacked slug/ folder recursively (SKILL.md, references/, and any
        # bundled extras such as scripts/) with forward-slash internal paths.
        files = []
        for root, _dirs, fnames in os.walk(srcdir):
            for fn in sorted(fnames):
                files.append(os.path.join(root, fn))
        with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(files):
                arc = os.path.relpath(f, fdir).replace(os.sep, "/")
                z.write(f, arc)
        marker = os.path.join(fdir, "DO_NOT_FORGET_TO_REZIP.md")
        if os.path.exists(marker):
            os.remove(marker)
        print(f"repacked {out_zip}  ({len(files)} files)")


if __name__ == "__main__":
    main()
