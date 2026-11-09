"""The five dimension pages (HTML and Markdown)."""
from __future__ import annotations

import html

from .chrome import dochead, esc, page, pagenav, sections, table_html
from .measured import measured_sections
from .rules import grade, score_rubric
from .text import apply_hints, id_link, md_plain, md_to_html, tag

MODEL = "Ananas-Agency Website Audit"
CHIP_MEASURED = ('<span class="chip-measured" style="font-size:11px;font-weight:650;border-radius:2px;'
                 'padding:2px 7px;background:#dce4f5;color:#1c3f7c;letter-spacing:.02em" '
                 'title="Backed by a real render — measured locally, no API keys">measured</span>')
_QUAD_LABEL = {"quickwin": "quick win", "bigbet": "big bet", "fillin": "fill-in", "skip": "skip"}


def _finding_card(f, keymap) -> str:
    width = int(round(f.impact / 5 * 100))
    chip = " " + CHIP_MEASURED if f.measured else ""
    evidence = f"<blockquote>{md_to_html(f.evidence, keymap)}</blockquote>" if f.evidence else ""
    return (f'<article class="card"><h3><span class="id">{esc(f.id)}</span> <span class="ttl">{esc(f.title)}</span>'
            f'<span class="scorewrap"><span class="meter"><i style="width:{width}%"></i></span>'
            f'<span class="scoreno">Impact {f.impact}/5</span></span>'
            f'{tag(f.quad)}{chip}</h3>'
            f'<div class="row"><span class="k">Issue</span>{md_to_html(f.issue, keymap)}</div>'
            f'<div class="row"><span class="k">Impact</span>{md_to_html(f.impact_text, keymap)} '
            f'<span class="effort">· Effort {f.effort}/5</span></div>'
            f'<div class="row"><span class="k">Fix</span>{md_to_html(f.fix, keymap)}</div>'
            f'{evidence}</article>')


def criteria_table_html(dim, wrap: bool = True) -> str:
    points, _score = score_rubric(dim.rubric)
    rows = "".join(
        f"<tr><td>{i}</td><td>{esc(r.criterion)}</td><td>{esc(r.result)}</td>"
        f"<td>{r.weight}</td><td>{p:g}</td></tr>"
        for i, (r, p) in enumerate(zip(dim.rubric, points), 1))
    rows += (f"<tr><td></td><td><b>Total</b></td><td></td><td><b>{sum(r.weight for r in dim.rubric)}</b></td>"
             f"<td><b>{sum(points):g}</b></td></tr>")
    head = "<tr><th>#</th><th>Criterion</th><th>Result</th><th>Weight</th><th>Points</th></tr>"
    return table_html(head + rows, wrap)


# Exact copy from report-format.md: all six widths are percentages that total 100.
FINDINGS_HEAD = ('<table style="width:100%;min-width:860px">\n'
                 '<colgroup><col style="width:8%"><col style="width:19%"><col style="width:28%">\n'
                 '<col style="width:28%"><col style="width:6%"><col style="width:11%"></colgroup>\n'
                 '<tr><th>ID</th><th>Finding</th><th>Issue</th><th>Fix</th>\n'
                 '<th style="text-align:center">I&nbsp;/&nbsp;E</th><th>Priority</th></tr>')


def findings_table_html(dim, keymap) -> str:
    """Every finding of a dimension as one full-width table (for the consolidated report)."""
    rows = "".join(
        f'<tr><td style="white-space:nowrap">{id_link(f)}</td><td>{esc(f.title)}</td>'
        f'<td>{md_to_html(f.issue, keymap)}</td><td>{md_to_html(f.fix, keymap)}</td>'
        f'<td style="white-space:nowrap;text-align:center">{f.impact}&nbsp;/&nbsp;{f.effort}</td>'
        f'<td style="white-space:nowrap">{tag(f.quad)}</td></tr>'
        for f in dim.findings)
    return FINDINGS_HEAD + rows + "</table>"


def _counts(dim) -> tuple:
    quick = sum(1 for f in dim.findings if f.quad == "quickwin")
    big = sum(1 for f in dim.findings if f.quad == "bigbet")
    return len(dim.findings), quick, big


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def _summary_html(dim) -> str:
    total, quick, big = _counts(dim)
    out = (f'<div class="row"><span class="k">Findings</span>{total} '
           f'({_plural(quick, "quick win")}, {_plural(big, "big bet")})</div>')
    if dim.findings:
        top = dim.findings[0]
        out += (f'<div class="row"><span class="k">Top priority</span>{id_link(top)} — {esc(top.title)}</div>')
    return out


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _md_scorecard(dim) -> str:
    points, _score = score_rubric(dim.rubric)
    out = "| # | Criterion | Result | Weight | Points |\n|---|-----------|--------|:------:|:------:|\n"
    for i, (r, p) in enumerate(zip(dim.rubric, points), 1):
        out += f"| {i} | {_cell(r.criterion)} | {r.result} | {r.weight} | {p:g} |\n"
    return out + f"| | **Total** | | **{sum(r.weight for r in dim.rubric)}** | **{sum(points):g}** |\n"


def _md_findings(dim, keymap) -> str:
    if not dim.findings:
        return "No findings in this dimension.\n\n"
    out = ""
    for f in dim.findings:
        out += (f"### {f.id}. {f.title} — Impact {f.impact} · Effort {f.effort} · {_QUAD_LABEL[f.quad]}\n"
                f"- **Issue:** {md_plain(f.issue, keymap)}\n"
                f"- **Impact:** {md_plain(f.impact_text, keymap)}\n"
                f"- **Fix:** {md_plain(f.fix, keymap)}\n")
        if f.evidence:
            out += f"> {md_plain(f.evidence, keymap)}\n"
        out += "\n"
    return out


def _md(run, dim, keymap, measured) -> str:
    out = (f"# {dim.title} — {run.site}\nDate: {run.date}\nModel: {MODEL}\n"
           f"Graded against: benchmarks-2026.md (2026 web standards)\nPrimary goal: {run.primary_goal}\n\n"
           f"## Grade: {dim.grade} ({dim.score}/100)\n{md_plain(dim.verdict, keymap)}\n\n"
           f"### Scorecard\n{_md_scorecard(dim)}\n## Findings\n{_md_findings(dim, keymap)}")
    for title, _inner, md in measured:
        out += f"## {html.unescape(title)}\n{md}\n"
    for title, body in dim.extra:
        out += f"## {title}\n{md_plain(body, keymap)}\n\n"
    if dim.notes:
        out += f"## Measurement notes\n{md_plain(dim.notes, keymap)}\n\n"
    out += "## What's working\n" + "".join(f"- {md_plain(s, keymap)}\n" for s in dim.strengths) + "\n"
    total, quick, big = _counts(dim)
    out += f"## Summary\n- Findings: {total} ({_plural(quick, 'quick win')}, {_plural(big, 'big bet')})\n"
    if dim.findings:
        out += f"- Top priority: {dim.findings[0].id} — {dim.findings[0].title}\n"
    return out


def render_dimension(run, page_name: str, keymap, final: bool) -> tuple:
    """Return (html, markdown) for one dimension page. `final` adds the page navigation."""
    dim = run.dims[page_name]
    letter, css = grade(dim.score)
    header = dochead(
        esc(f"{dim.title} — {run.site}"),
        f"<b>Date:</b> {esc(run.date)} &nbsp;·&nbsp; <b>Model:</b> {MODEL} &nbsp;·&nbsp; "
        f"<b>Grade:</b> {letter} ({dim.score}/100)")

    items = [
        ("Grade &amp; scorecard",
         f'<div class="row"><span class="grade {css}">{letter}</span> <b>{dim.score}/100</b> — '
         f'{md_to_html(dim.verdict, keymap)}</div>' + criteria_table_html(dim), ""),
        ("Findings", "".join(_finding_card(f, keymap) for f in dim.findings)
         or '<div class="row">No findings in this dimension.</div>', ""),
    ]
    measured = measured_sections(run, page_name, final)
    items.extend((title, inner, "") for title, inner, _md in measured)
    for title, body in dim.extra:
        items.append((esc(title), f'<div class="card">{md_to_html(body, keymap)}</div>', ""))
    if dim.notes:
        items.append(("Measurement notes", f'<div class="card">{md_to_html(dim.notes, keymap)}</div>', ""))
    items.append(("What&rsquo;s working",
                  '<ul class="clean">' + "".join(f"<li>{md_to_html(s, keymap)}</li>" for s in dim.strengths)
                  + "</ul>", ""))
    items.append(("Summary", _summary_html(dim), ""))

    body = apply_hints(sections(items))
    nav = pagenav(run, page_name) if final else ""
    html_text = page(f"{dim.title} — {run.site}", dim.utm, header, body, nav, date=run.date)
    return html_text, _md(run, dim, keymap, measured)
