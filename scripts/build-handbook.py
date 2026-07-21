#!/usr/bin/env python3
"""Rebuild the compiled Handbook from the unpacked skill sources.

Run from anywhere:  python scripts/build-handbook.py

For each skill it emits:  # <N>. <Title> / Skill ID / <SKILL.md body> /
reference materials / <rules-*.md body>, matching the Handbook's format. Internal
links are rewritten to the Handbook's root context (any-depth ../LICENSE -> LICENSE,
../report-format.md -> report-format.md); references/ links are left as-is.

Run this after editing any skill so the Handbook stays in sync with <folder>/<slug>/.
"""
import os
import re

# repo root = parent of this scripts/ folder
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "Website Audit Suite - Handbook by Ananas Agency.md")

# (label, title, folder, slug, rules_filename)  — order = Handbook order
SKILLS = [
    ("0", "Site Snapshot",                              "0 Site Snapshot",      "site-snapshot",     "rules-snapshot.md"),
    ("1", "Goals & Discovery",                          "1 Goals Discovery",    "goals-discovery",   "rules-goals-discovery.md"),
    ("2", "Messaging & Clarity",                        "2 Messaging Clarity",  "messaging-clarity", "rules-messaging-clarity.md"),
    ("3", "Conversion (CRO)",                           "3 Conversion CRO",     "conversion-cro",    "rules-conversion.md"),
    ("4", "SEO & Content",                              "4 SEO Content",        "seo-content",       "rules-seo.md"),
    ("5", "UX & Technical",                             "5 UX Technical",       "ux-technical",      "rules-ux-technical.md"),
    ("6", "Design & Visual",                            "6 Design Visual",      "design-visual",     "rules-design-visual.md"),
    ("7", "Action Report",                              "7 Action Report",      "action-report",     "rules-action-report.md"),
]

SEP = "\n\n================================================================================\n\n"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_frontmatter(text):
    if text.startswith("---"):
        idx = text.find("\n---", 3)
        if idx != -1:
            return text[idx + 4:].lstrip("\n")
    return text.lstrip("\n")


def fix_links(t):
    # collapse any-depth relative links to the root-context paths the Handbook uses
    t = re.sub(r"\]\((?:\.\./)*LICENSE(?:\.md)?\)", "](LICENSE)", t)
    t = re.sub(r"\]\((?:\.\./)*report-format\.md\)", "](report-format.md)", t)
    t = re.sub(r"\]\((?:\.\./)*benchmarks-2026\.md\)", "](benchmarks-2026.md)", t)
    return t


def block(label, title, folder, slug, rules):
    skill = fix_links(strip_frontmatter(read(os.path.join(BASE, folder, slug, "SKILL.md")))).rstrip()
    rulesbody = fix_links(read(os.path.join(BASE, folder, slug, "references", rules))).lstrip("\n").rstrip()
    return (
        f"# {label}. {title}\n\n"
        f"**Skill ID:** `{slug}`\n\n"
        f"{skill}\n\n"
        f"---\n\n"
        f"## Skill reference materials: {slug}\n\n"
        f"### Reference: {rules}\n\n"
        f"{rulesbody}"
    )


def main():
    intro = ("# Website Audit Suite - Handbook\n\n"
             "_by Ananas Agency._ Every skill and its reference, compiled into one document. No stages - one suite.")
    blocks = [block(*s) for s in SKILLS]
    doc = intro + SEP + SEP.join(blocks) + "\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"wrote {OUT}  ({len(blocks)} skills, {len(doc)} chars)")


if __name__ == "__main__":
    main()
