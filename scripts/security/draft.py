"""Draft the security page JSON from a scan Outcome, following audit-data-format.md "Dimension files"."""
from __future__ import annotations

from typing import Optional

from . import DISCLAIMER_BODY, DISCLAIMER_EXTRA_TITLE, RUBRIC
from .checks import Outcome
from .wording import CHECKS, STRENGTHS

HIGH_IMPACT = 4
SCOPE_TITLE = "What the file check covered"
NO_STRENGTHS = "Nothing on this list was already in place, so the findings below are the place to start."


def _plural(n: int, word: str) -> str:
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def draft_page(outcome: Outcome, scope: Optional[str] = None) -> dict:
    evidence = {}
    for hit in outcome.hits:
        evidence.setdefault(hit.check, hit.evidence)  # a repeated check id keeps its first hit
    findings = []
    for key, check in CHECKS.items():
        if key in evidence:
            findings.append({
                "key": key, "title": check.title, "issue": check.issue, "impact_text": check.impact_text,
                "fix": check.fix, "impact": check.impact, "effort": check.effort,
                "evidence": evidence[key], "measured": True,
            })
    unchecked = {criterion for criterion, _ in outcome.not_checked}
    rubric = []
    for criterion, weight in RUBRIC:
        impacts = [CHECKS[f["key"]].impact for f in findings if CHECKS[f["key"]].criterion == criterion]
        if any(i >= HIGH_IMPACT for i in impacts):
            result = "Fail"
        elif criterion in unchecked or impacts:
            result = "Partial"
        else:
            result = "Pass"
        rubric.append({"criterion": criterion, "result": result, "weight": weight})
    strengths = [text for key, text in STRENGTHS.items() if key in outcome.strengths]
    if not strengths:
        strengths = [NO_STRENGTHS]
    high = sum(1 for f in findings if f["impact"] >= HIGH_IMPACT)
    page = {
        "verdict": "%s found, %d of them high priority; %s already in place." % (
            _plural(len(findings), "security issue"), high, _plural(len([t for t in strengths if t != NO_STRENGTHS]), "protection")),
        "rubric": rubric,
        "findings": findings,
        "strengths": strengths,
        "extra": [{"title": DISCLAIMER_EXTRA_TITLE, "body": DISCLAIMER_BODY}],
    }
    if scope:
        page["extra"].append({"title": SCOPE_TITLE, "body": scope})
    notes = "\n".join(note for _, note in outcome.not_checked)
    if notes:
        page["notes"] = notes
    return page
