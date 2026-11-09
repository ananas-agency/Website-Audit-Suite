"""Priority, ID, scoring and roadmap rules for the report builder."""
from __future__ import annotations

import math

from . import DIMENSIONS
from .data import Finding, Run

QUAD_ORDER = ("quickwin", "bigbet", "fillin", "skip")
_CREDIT = {"Pass": 1.0, "Partial": 0.5, "Fail": 0.0}
_HALVES = {"Pass": 2, "Partial": 1, "Fail": 0}  # credit in half-points, for exact integer maths


def quadrant(impact: int, effort: int) -> str:
    """Impact 3-5 is high, Effort 1-2 is low."""
    high, low = impact >= 3, effort <= 2
    if high:
        return "quickwin" if low else "bigbet"
    return "fillin" if low else "skip"


def sort_key(f: Finding, index: int) -> tuple:
    return (-f.impact, f.effort, index)


def half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def grade(score: int) -> tuple:
    for floor, letter in ((90, "A"), (80, "B"), (70, "C"), (60, "D")):
        if score >= floor:
            return letter, letter.lower()
    return "F", "f"


def score_rubric(rows: list) -> tuple:
    """Points per row (weight x credit) and the score normalised to 0-100, rounded half-up."""
    points = [r.weight * _CREDIT[r.result] for r in rows]
    total = sum(r.weight for r in rows)
    # Exact half-up of halves*100 / (2*total): integer arithmetic, no float error at .5 edges.
    halves = sum(r.weight * _HALVES[r.result] for r in rows)
    score = (halves * 100 + total) // (2 * total) if total else 0
    return points, score


def apply_rules(run: Run) -> dict:
    """Set dim, quad, id on every finding, reorder findings, set score and grade. Idempotent."""
    by_key = {}
    for dim in run.dims.values():
        dim.findings = [f for _, f in sorted(
            ((sort_key(f, i), f) for i, f in enumerate(dim.findings)), key=lambda p: p[0])]
        for n, f in enumerate(dim.findings, 1):
            f.dim = dim.page
            f.quad = quadrant(f.impact, f.effort)
            f.id = f"{dim.prefix}-{n:02d}"
            by_key[f.key] = f
        dim.score = score_rubric(dim.rubric)[1]
        dim.grade = grade(dim.score)[0]
    return by_key


def overall(run: Run) -> tuple:
    scores = [d.score for d in run.dims.values()]
    missing = [title for page, _, title, _ in DIMENSIONS if page not in run.dims]
    n = len(scores)
    mean = (2 * sum(scores) + n) // (2 * n) if n else 0
    return mean, grade(mean)[0], missing


def all_findings(run: Run) -> list:
    """Every finding in walk order (DIMENSIONS order, then each dimension's order)."""
    return [f for page, *_ in DIMENSIONS if page in run.dims for f in run.dims[page].findings]


def _sorted(findings: list) -> list:
    return [f for _, f in sorted(((sort_key(f, i), f) for i, f in enumerate(findings)),
                                 key=lambda p: p[0])]


def biggest_opportunity(run: Run) -> Finding:
    return _sorted(all_findings(run))[0]


def top_quick_wins(run: Run, n: int = 3) -> list:
    return _sorted([f for f in all_findings(run) if f.quad == "quickwin"])[:n]


def roadmap(run: Run) -> list:
    fs = all_findings(run)
    out = []
    for q in QUAD_ORDER:
        out.extend(_sorted([f for f in fs if f.quad == q]))
    return out


def phases(run: Run) -> dict:
    r = roadmap(run)
    bigbets = [f for f in r if f.quad == "bigbet"]
    return {
        "two_weeks": [f for f in r if f.quad == "quickwin"],
        "days_30_60": bigbets[:3],
        "days_60_90": bigbets[3:] + [f for f in r if f.quad == "fillin"],
    }
