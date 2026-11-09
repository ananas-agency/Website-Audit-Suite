"""The Action Report page (HTML and Markdown) and the blocks the consolidated report reuses."""
from __future__ import annotations

import base64
import html
import re

from . import DIMENSIONS
from .chrome import dochead, esc, page, page_file, pagenav, sections, table_html
from .measured import run_file
from .pages_dim import criteria_table_html, findings_table_html
from .pages_intake import snapshot_rows_html, stated_vs_observed_html
from .rules import biggest_opportunity, grade, overall, phases, roadmap, top_quick_wins
from .text import _LINK, apply_hints, id_link, md_plain, md_to_html

MODEL = "Ananas-Agency Website Audit"
RUN_MODES = {"extended": "Extended (measured tools ran)", "basic": "Basic (reasoning only)"}
BRIEF_LIMIT = 120
EXAMPLE_METRICS = "(for example GA4 conversions or form completions)"
_QUADS = (("qw", "quickwin", "Quick Wins — do first", "Quick Wins"),
          ("bb", "bigbet", "Big Bets — plan &amp; schedule", "Big Bets"),
          ("fi", "fillin", "Fill-ins — when convenient", "Fill-ins"),
          ("sk", "skip", "Skip — backlog", "Skip"))
_PILLS = {"met": '<span class="pill covered">met</span>',
          "gap": '<span class="pill gap">gap</span>',
          "na": '<span class="tag skip">n/a</span>'}
# Exact copy from rules-action-report.md:61-66. Appended after apply_hints so it is never altered.
CTA_BLOCK = """<div class="ctablock">
  <div class="ctahead">Fresh eyes turned your site into a to-do list?</div>
  <div class="ctasub">We turn audits like this one into websites that actually convert.</div>
  <a class="ctabtn" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=action-report-cta" target="_blank" rel="noopener">Let's Grow Together</a>
</div>"""


def _flat(text: str) -> str:
    """Drop links (keep the label), code ticks and emphasis; collapse whitespace. [[key]] survives."""
    text = _LINK.sub(lambda m: m.group(1), text)
    return " ".join(re.sub(r"[`*]", "", text).split())


_ABBREV = re.compile(r"(?i)(?<![\w.])(?:e\.g|i\.e|vs|etc|approx|incl|cf)\.$")


def _first_sentence(text: str) -> str:
    """Up to the first sentence end, ignoring full stops that belong to abbreviations ("e.g.", "vs.")."""
    for m in re.finditer(r"[.!?]\s", text):
        if text[m.start()] == "." and _ABBREV.search(text[:m.start() + 1]):
            continue
        return text[:m.start() + 1]
    return text


_REF_SPLIT = re.compile(r"(\[\[[^\[\]\s]+\]\])")


def _cut_word(word: str, keymap) -> str:
    """The start of one over-long word within BRIEF_LIMIT plain characters; a [[key]] is kept whole or dropped."""
    out, length = "", 0
    for i, piece in enumerate(_REF_SPLIT.split(word)):
        if i % 2:  # a reference counts as the ID it resolves to
            size = len(md_plain(piece, keymap))
            if length + size > BRIEF_LIMIT:
                break
            out, length = out + piece, length + size
        else:
            take = piece[:BRIEF_LIMIT - length]
            out, length = out + take, length + len(take)
            if len(take) < len(piece):
                break
    return out


def brief_fix(f, keymap) -> str:
    """The fix in brief, as light Markdown: [[key]] references are kept so callers resolve them
    (md_to_html for an id_link, md_plain for the .md). The author's fix_brief wins; otherwise the
    first sentence of the fix, cut at 120 plain characters on a word boundary."""
    if f.fix_brief.strip():
        return _flat(f.fix_brief)
    first = _first_sentence(_flat(f.fix))
    if len(md_plain(first, keymap)) <= BRIEF_LIMIT:
        return first
    out, length = [], 0
    for word in first.split():
        add = len(md_plain(word, keymap)) + (1 if out else 0)
        if length + add > BRIEF_LIMIT:
            break
        out.append(word)
        length += add
    cut = " ".join(out) if out else _cut_word(first.split()[0], keymap)
    return cut.rstrip(" ,;:.-") + "…"


def _chip(score: int) -> str:
    letter, css = grade(score)
    return f'<span class="grade {css}">{letter}</span>'


def _join(items: list) -> str:
    return ", ".join(items[:-1]) + " and " + items[-1] if len(items) > 1 else "".join(items)


NO_ANALYSIS = "no analysis ran"


def _overall_text(run) -> str:
    """'F (52/100)', or 'no analysis ran' when the run has no dimension to average."""
    if not run.dims:
        return NO_ANALYSIS
    score, letter, _missing = overall(run)
    return f"{letter} ({score}/100)"


def _missing_note(run) -> str:
    score, letter, missing = overall(run)
    if not run.dims or not missing:
        return ""
    ran = [run.dims[p].title for p, *_ in DIMENSIONS if p in run.dims]
    return f"Overall {letter} ({score}), from {_join(ran)} only; {_join(missing)} not run."


def scorecard_html(run, wrap: bool = True) -> str:
    """The dimension table with the Overall row, plus the missing-dimension note."""
    score, _letter, _missing = overall(run)
    rows = "".join(
        f"<tr><td>{esc(run.dims[p].title)}</td><td>{_chip(run.dims[p].score)}</td>"
        f"<td>{run.dims[p].score}</td></tr>"
        for p, *_ in DIMENSIONS if p in run.dims)
    if run.dims:
        rows += f"<tr><td><b>Overall</b></td><td><b>{_chip(score)}</b></td><td><b>{score}</b></td></tr>"
    else:
        rows += f"<tr><td><b>Overall</b></td><td colspan=\"2\">{NO_ANALYSIS}</td></tr>"
    note = _missing_note(run)
    note_html = f'<div class="row"><span class="verdict-common">{esc(note)}</span></div>' if note else ""
    return table_html("<tr><th>Dimension</th><th>Grade</th><th>Score</th></tr>" + rows, wrap) + note_html


def _bench_counts(run) -> dict:
    return {s: sum(1 for b in run.action.benchmarks if b.status == s) for s in ("met", "gap", "na")}


def _extra_keys(b, keymap) -> list:
    """Benchmark keys whose finding the note does not already cite as [[key]]."""
    return [keymap[k.strip()] for k in b.keys
            if k.strip() in keymap and f"[[{k.strip()}]]" not in b.note]


def _key_links(b, keymap) -> str:
    return ", ".join(id_link(f) for f in _extra_keys(b, keymap))


def benchmarks_html(run, keymap, wrap: bool = True) -> str:
    """The '2026 standard vs your site' summary line and table."""
    n = _bench_counts(run)
    head = (f'<div class="row"><span class="pill covered">{n["met"]} met</span> &nbsp; '
            f'<span class="pill gap">{n["gap"]} gaps</span> &nbsp; '
            f'<span class="tag skip">{n["na"]} n/a</span> &nbsp;'
            '<span class="verdict-common">— measured against '
            '<a href="https://web.dev/vitals/" title="benchmarks-2026.md — what a website should be in 2026">'
            'the 2026 web standards</a>.</span></div>')
    rows = ""
    for b in run.action.benchmarks:
        links = _key_links(b, keymap)
        cell = md_to_html(b.note, keymap) + (f" ({links})" if links else "")
        rows += (f'<tr><td>{esc(b.standard)}</td><td style="white-space:nowrap">{_PILLS[b.status]}</td>'
                 f'<td>{cell}</td></tr>')
    return head + table_html("<tr><th>2026 standard</th><th>Status</th><th>This site</th></tr>" + rows, wrap)


def matrix_html(run) -> str:
    """The four .quad cells; an empty cell shows a dash."""
    fs = roadmap(run)
    cells = ""
    for css, quad, label, _plain in _QUADS:
        lis = "".join(f"<li>{id_link(f)} — {esc(f.title)}</li>" for f in fs if f.quad == quad) or "<li>—</li>"
        cells += f'<div class="quad {css}"><h4><span class="dot"></span>{label}</h4><ul>{lis}</ul></div>'
    return f'<div class="matrix">{cells}</div>'


def roadmap_html(run, keymap, wrap: bool = True) -> str:
    rows = "".join(
        f"<tr><td>{i}</td><td style=\"white-space:nowrap\">{id_link(f)}</td><td>{esc(f.title)}</td>"
        f"<td>{md_to_html(brief_fix(f, keymap), keymap)}</td><td>{f.impact}</td><td>{f.effort}</td>"
        f"<td>{esc(run.dims[f.dim].title)}</td></tr>"
        for i, f in enumerate(roadmap(run), 1))
    return table_html("<tr><th>#</th><th>ID</th><th>Issue</th><th>Fix (brief)</th>"
                      "<th>Impact</th><th>Effort</th><th>From</th></tr>" + rows, wrap)


def _row(label: str, inner: str) -> str:
    return f'<div class="row"><span class="k">{label}</span>{inner}</div>'


def _bullets(items: list) -> str:
    return '<ul class="clean">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def _linked(f) -> str:
    return f"{id_link(f)} — {esc(f.title)}"


def _summary_html(run, keymap) -> str:
    out = ""
    if roadmap(run):
        out += _row("Biggest opportunity", _linked(biggest_opportunity(run)))
        out += _row("Top 3 quick wins", ", ".join(id_link(f) for f in top_quick_wins(run)) or "—")
    out += _row("What&rsquo;s working", "") + _bullets([md_to_html(s, keymap) for s in run.action.strengths])
    if run.action.rating_notes:
        out += _row("Rating notes", "") + _bullets([md_to_html(n, keymap) for n in run.action.rating_notes])
    return out


def _plan_html(run) -> str:
    p = phases(run)
    start = esc(f"Start measuring against {run.primary_goal} {EXAMPLE_METRICS}")
    first = ["&#9744; " + _linked(f) for f in p["two_weeks"]]
    mid = [_linked(f) for f in p["days_30_60"]] + [start]
    late = [_linked(f) for f in p["days_60_90"]] + ["Re-run the audit to see the grades move"]
    return (_row("Your first two weeks", "Ship the quick wins:") + _bullets(first)
            + _row("Days 30–60", "Kick off the top big bets:") + _bullets(mid)
            + _row("Days 60–90", "Finish the big bets and fill-ins:") + _bullets(late))


def _cell(text: str) -> str:
    return text.replace("|", chr(92) + "|").replace("\n", " ")


def _md(run, keymap) -> str:
    score, letter, _missing = overall(run)
    out = (f"# Website Audit — Action Report — {run.site}\nDate: {run.date}\nModel: {MODEL}\n"
           f"Primary goal: {run.primary_goal}\nRun mode: {RUN_MODES[run.mode]}\n\n"
           f"## Overall grade: {_overall_text(run)}\n"
           "| Dimension | Grade | Score |\n|-----------|:-----:|:-----:|\n")
    for p, *_ in DIMENSIONS:
        if p in run.dims:
            d = run.dims[p]
            out += f"| {d.title} | {grade(d.score)[0]} | {d.score} |\n"
    out += (f"| **Overall** | **{letter}** | **{score}** |\n" if run.dims
            else f"| **Overall** | {NO_ANALYSIS} | |\n")
    note = _missing_note(run)
    if note:
        out += f"\n{note}\n"
    n = _bench_counts(run)
    out += (f"\n## 2026 standard vs your site\n_{n['met']} met · {n['gap']} gaps · {n['na']} n/a "
            "(against benchmarks-2026.md)._\n\n| 2026 standard | Status | This site |\n"
            "|---------------|:------:|-----------|\n")
    for b in run.action.benchmarks:
        ids = ", ".join(f.id for f in _extra_keys(b, keymap))
        text = _cell(md_plain(b.note, keymap)) + (f" ({ids})" if ids else "")
        out += f"| {_cell(b.standard)} | {b.status} | {text} |\n"
    fs = roadmap(run)
    out += "\n## Executive summary\n"
    if fs:
        big = biggest_opportunity(run)
        out += (f"- **Biggest opportunity:** {big.id} — {big.title}\n"
                f"- **Top 3 quick wins:** {', '.join(f.id for f in top_quick_wins(run)) or '—'}\n")
    out += f"- **What's working:** {'; '.join(md_plain(s, keymap) for s in run.action.strengths)}\n"
    for rating_note in run.action.rating_notes:
        out += f"- **Rating note:** {md_plain(rating_note, keymap)}\n"
    out += "\n## Priority matrix (Impact × Effort)\n"
    for _css, quad, _label, plain in _QUADS:
        out += f"- **{plain}:** {', '.join(f.id for f in fs if f.quad == quad) or '—'}\n"
    out += ("\n## Roadmap\n| # | ID | Issue | Fix (brief) | Impact | Effort | From |\n"
            "|---|----|-------|-------------|:------:|:------:|------|\n")
    for i, f in enumerate(fs, 1):
        out += (f"| {i} | {f.id} | {_cell(f.title)} | {_cell(md_plain(brief_fix(f, keymap), keymap))} | {f.impact} | "
                f"{f.effort} | {run.dims[f.dim].title} |\n")
    p = phases(run)
    out += "\n## Plan\n### Your first two weeks\n" + "".join(f"- [ ] {f.id} — {f.title}\n" for f in p["two_weeks"])
    out += ("### Days 30–60\n" + "".join(f"- {f.id} — {f.title}\n" for f in p["days_30_60"])
            + f"- Start measuring against {run.primary_goal} {EXAMPLE_METRICS}\n")
    out += ("### Days 60–90\n" + "".join(f"- {f.id} — {f.title}\n" for f in p["days_60_90"])
            + "- Re-run the audit to see the grades move\n")
    return out


def render_action(run, keymap, final: bool) -> tuple:
    """Return (html, markdown) for the Action Report. `final` adds the page navigation."""
    score, letter, _missing = overall(run)
    header = dochead(
        esc(f"Website Audit — Action Report — {run.site}"),
        f"<b>Date:</b> {esc(run.date)} &nbsp;·&nbsp; <b>Model:</b> {MODEL} &nbsp;·&nbsp; "
        f"<b>Overall:</b> {_overall_text(run)} &nbsp;·&nbsp; <b>Run mode:</b> {RUN_MODES[run.mode]}")
    lead = (f'<div class="row"><span class="grade {grade(score)[1]}">{letter}</span> <b>{score}/100</b> — '
            "the mean of the dimension scores. The grade is an expert judgement, not a measurement.</div>"
            if run.dims else "")
    items = [
        ("Overall scorecard", lead + scorecard_html(run), ""),
        ("2026 standard vs your site", benchmarks_html(run, keymap), ""),
        ("Executive summary", _summary_html(run, keymap), ""),
        ("Priority matrix", matrix_html(run), ""),
        ("Roadmap", roadmap_html(run, keymap), ""),
        ("Plan", _plan_html(run), ""),
    ]
    body = apply_hints(sections(items)) + CTA_BLOCK
    nav = pagenav(run, "action-report") if final else ""
    html_text = page(f"Website Audit — Action Report — {run.site}", "action-report", header, body, nav,
                     date=run.date)
    return html_text, _md(run, keymap)


# ---------------------------------------------------------------- consolidated report

NOT_DONE = "— not yet completed —"
_SHORT = {"messaging": "Messaging", "conversion": "Conversion", "seo": "SEO",
          "ux-technical": "UX/Technical", "design": "Design"}
_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
         ".svg": "image/svg+xml", ".webp": "image/webp"}


def _logo_uri(run) -> str:
    """The logo as a data URI, or '' when run.logo is unset, missing or not an image."""
    if not run.logo:
        return ""
    path = run_file(run.dir, run.logo)
    mime = _MIME.get(path.suffix.lower()) if path else None
    if not mime:
        return ""
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def _report_header(run) -> str:
    score, letter, _missing = overall(run)
    uri = _logo_uri(run)
    h1 = (f'<img src="{uri}" alt="{html.escape(run.site)}" style="display:block;height:48px;width:auto">'
          if uri else esc(run.site))
    meta = (f"Website audit of {esc(run.site)}, built with the Website Audit Suite <b>by Ananas Agency</b>"
            f"<br><b>Date:</b> {esc(run.date)} &nbsp;·&nbsp; <b>Site:</b> {esc(run.url)} &nbsp;·&nbsp; "
            f"<b>Overall:</b> {_overall_text(run)} &nbsp;·&nbsp; <b>Run mode:</b> {RUN_MODES[run.mode]}")
    return dochead(h1, meta, esc(run.tagline))


def _report_summary(run, keymap) -> str:
    score, letter, _missing = overall(run)
    glance = " · ".join(f"{_SHORT[p]} {_chip(run.dims[p].score)}" for p, *_ in DIMENSIONS if p in run.dims)
    if not run.dims:
        out = f'<div class="row"><b>Overall:</b> {NO_ANALYSIS}</div>'
    else:
        out = (f'<div class="row"><span class="grade {grade(score)[1]}">{letter}</span> <b>{score}/100 overall</b>'
               + (f" — {glance}" if glance else "") + "</div>")
    if roadmap(run):
        out += _row("Biggest opportunity", _linked(biggest_opportunity(run)))
        out += _row("Top 3 quick wins", ", ".join(id_link(f) for f in top_quick_wins(run)) or "—")
    if run.action is not None:
        out += _row("What&rsquo;s working", "") + _bullets([md_to_html(s, keymap) for s in run.action.strengths])
        if run.action.rating_notes:
            out += _row("Rating notes", "") + _bullets([md_to_html(n, keymap) for n in run.action.rating_notes])
    return out


def _goals_digest(run, keymap) -> str:
    g = run.goals
    out = f'<div class="row"><i>{md_to_html(g.framing, keymap)}</i></div>'
    out += "".join(_row(esc(label), md_to_html(value, keymap)) for label, value in g.brief)
    out += stated_vs_observed_html(g, keymap, wrap=False)
    out += "".join(_row("Advice", f"<b>{esc(h)}</b> — {md_to_html(d, keymap)} → {md_to_html(a, keymap)}")
                   for h, d, a in g.advice)
    return out


def _plan_digest(run, keymap) -> str:
    out = scorecard_html(run, wrap=False) if run.dims else ""
    if run.action is not None:
        out += benchmarks_html(run, keymap, wrap=False)
    return out + matrix_html(run) + roadmap_html(run, keymap, wrap=False)


def _report_sections(run, keymap) -> list:
    """(title, inner, open_href) for sections 1-8; open_href is '' when that page was not built."""
    def href(name: str) -> str:
        return f"{page_file(run, name)}.html"

    placeholder = f'<div class="row">{NOT_DONE}</div>'
    snap = run.snapshot
    items = [("Site Snapshot",
              "".join(snapshot_rows_html(rows) for _title, rows in snap.sections) if snap else placeholder,
              href("site-snapshot") if snap else ""),
             ("Goals &amp; Discovery",
              _goals_digest(run, keymap) if run.goals is not None else placeholder,
              href("goals") if run.goals is not None else "")]
    for page_name, _prefix, title, _utm in DIMENSIONS:
        dim = run.dims.get(page_name)
        if dim is None:
            items.append((esc(title), placeholder, ""))
            continue
        inner = (f'<div class="row">{md_to_html(dim.verdict, keymap)}</div>'
                 + criteria_table_html(dim, wrap=False) + findings_table_html(dim, keymap))
        items.append((f"{esc(title)} — {_chip(dim.score)} {dim.score}/100", inner, href(page_name)))
    items.append(("Action Plan", _plan_digest(run, keymap),
                  href("action-report") if run.action is not None else ""))
    return items


def _md_report(run, keymap) -> str:
    score, letter, _missing = overall(run)
    glance = " · ".join(f"{_SHORT[p]} {grade(run.dims[p].score)[0]}" for p, *_ in DIMENSIONS if p in run.dims)
    out = (f"# Website Audit — {run.site}\n" + (f"*{run.tagline}*\n" if run.tagline else "")
           + f"Date: {run.date} · Site: {run.url} · Run mode: {RUN_MODES[run.mode]}\n"
           f"Website audit of {run.site}, built with the Website Audit Suite by Ananas Agency.\n\n"
           f"## Executive summary\n**Overall: {_overall_text(run)}**"
           + (f" — {glance}" if glance else "") + "\n\n")
    if roadmap(run):
        big = biggest_opportunity(run)
        out += (f"- **Biggest opportunity:** {big.id} — {big.title}\n"
                f"- **Top 3 quick wins:** {', '.join(f.id for f in top_quick_wins(run)) or '—'}\n")
    if run.action is not None:
        out += f"- **What's working:** {'; '.join(md_plain(s, keymap) for s in run.action.strengths)}\n"
        for rating_note in run.action.rating_notes:
            out += f"- **Rating note:** {md_plain(rating_note, keymap)}\n"
    n = 0

    def head(title: str) -> str:
        nonlocal n
        n += 1
        return f"\n## {n}. {title}\n"

    out += head("Site Snapshot")
    if run.snapshot is None:
        out += f"{NOT_DONE}\n"
    else:
        for title, rows in run.snapshot.sections:
            out += f"### {title}\n" + "".join(f"- {label}: {md_plain(value, {})}\n" for label, value in rows)
    out += head("Goals & Discovery")
    if run.goals is None:
        out += f"{NOT_DONE}\n"
    else:
        g = run.goals
        out += "".join(f"- **{label}:** {md_plain(value, keymap)}\n" for label, value in g.brief)
        out += ("\n| You said | What the page + scans show | The gap |\n|---|---|---|\n"
                + "".join("| " + " | ".join(_cell(md_plain(c, keymap)) for c in row) + " |\n"
                          for row in g.stated_vs_observed))
        out += "\n" + "".join(f"{i}. **{h}** — {md_plain(d, keymap)} → {md_plain(a, keymap)}\n"
                              for i, (h, d, a) in enumerate(g.advice, 1))
    for page_name, _prefix, title, _utm in DIMENSIONS:
        dim = run.dims.get(page_name)
        if dim is None:
            out += head(title) + f"{NOT_DONE}\n"
            continue
        out += (head(f"{title} — {dim.grade} {dim.score}/100") + f"{md_plain(dim.verdict, keymap)}\n\n"
                "| ID | Finding | Issue | Fix | I / E | Priority |\n|---|---|---|---|:---:|---|\n")
        out += "".join(f"| {f.id} | {_cell(f.title)} | {_cell(md_plain(f.issue, keymap))} | "
                        f"{_cell(md_plain(f.fix, keymap))} | {f.impact} / {f.effort} | {f.quad} |\n"
                        for f in dim.findings)
    out += head("Action Plan")
    if run.dims:
        out += f"**Overall: {letter} ({score}/100)**\n"
    if run.action is not None:
        b = _bench_counts(run)
        out += f"\n2026 standard: {b['met']} met · {b['gap']} gaps · {b['na']} n/a.\n\n"
    for _css, quad, _label, plain in _QUADS:
        out += f"- **{plain}:** {', '.join(f.id for f in roadmap(run) if f.quad == quad) or '—'}\n"
    if run.action is not None:
        out += "\nSee action-report.md for the full roadmap and plan.\n"
    return out


def render_report(run, keymap) -> tuple:
    """Return (html, markdown) for the consolidated report, always with page navigation."""
    body = apply_hints(sections([("Executive summary", _report_summary(run, keymap), "")])
                       + sections(_report_sections(run, keymap)))
    html_text = page(f"Website Audit — {run.site}", "website-audit-report", _report_header(run), body,
                     pagenav(run, "report"), date=run.date)
    return html_text, _md_report(run, keymap)
