"""Render the security page JSON as the owner-facing text list (security.md)."""
from __future__ import annotations

from report import rules
from report.data import validate_dimension

from . import DISCLAIMER_BODY, DISCLAIMER_HEADING

QUAD_LABEL = {"quickwin": "Quick win", "bigbet": "Big bet", "fillin": "Fill-in", "skip": "Skip"}


def _flag(impact: int) -> str:
    if impact >= 4:
        return "🔴 HIGH"
    return "🟠 MEDIUM" if impact == 3 else "🟢 LOW"


def _developer(evidence: str, fix: str) -> list:
    evidence = evidence.strip()
    if not evidence:
        return ["*For your developer:* " + fix]
    if "\n" in evidence:
        return ["*For your developer:* Seen:", "```", *evidence.split("\n"), "```", "", fix]
    shown = evidence if "`" in evidence else "`%s`" % evidence
    if not shown.endswith("."):
        shown += "."
    return ["*For your developer:* Seen: %s %s" % (shown, fix)]


def render_text(page: dict, url: str, date: str) -> str:
    errors, rubric, findings = validate_dimension(page, "security.json")
    if errors:
        raise ValueError("; ".join(errors))
    score = rules.score_rubric(rubric)[1]
    out = ["# Security check: %s (%s)" % (url, date), "", "> **%s**" % DISCLAIMER_HEADING, ">"]
    paras = DISCLAIMER_BODY.split("\n\n")
    for i, para in enumerate(paras):
        out.append("> " + para)
        if i < len(paras) - 1:
            out.append(">")
    out += ["", "**Grade: %s (%d/100)**" % (rules.grade(score)[0], score), "", page["verdict"].strip(), ""]
    if page["strengths"]:
        out += ["## What's working", ""] + ["- " + s for s in page["strengths"]] + [""]
    for block in page.get("extra", [])[1:]:
        out += ["## " + block["title"].strip(), "", block["body"].strip(), ""]
    notes = [n for n in page.get("notes", "").split("\n") if n.strip()]
    if notes:
        out += ["## Not checked", ""] + ["- " + n for n in notes] + [""]
    out += ["## Findings", ""]
    ordered = sorted(enumerate(findings), key=lambda p: rules.sort_key(p[1], p[0]))
    for n, (_, f) in enumerate(ordered, 1):
        quad = QUAD_LABEL[rules.quadrant(f.impact, f.effort)]
        out += ["### SEC-%02d %s · %s: %s" % (n, _flag(f.impact), quad, f.title),
                "*In plain words:* " + f.issue, "",
                "*Why you should care:* " + f.impact_text, "",
                *_developer(f.evidence, f.fix), ""]
    return "\n".join(out).rstrip("\n") + "\n"
