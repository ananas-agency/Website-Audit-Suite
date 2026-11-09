"""The Site Snapshot and Goals pages (HTML and Markdown)."""
from __future__ import annotations

import re

from .chrome import dochead, esc, page, pagenav, sections, table_html
from .text import apply_hints, md_plain, md_to_html

MODEL = "Ananas-Agency Website Audit intake"
SNAPSHOT_NEXT = ("Run the Messaging & Clarity skill (or any of the five analyses) and paste this snapshot "
                 "when asked about the site.")
GOALS_NEXT = ("Run any of the five analyses (Messaging, Conversion, SEO, UX & Technical, Design & Visual) "
              "and paste this brief with the Site Snapshot when asked about the site.")


# Light Markdown (**TBD**, _tbd_, `TBD`) and trailing punctuation ("TBD.") around the word.
_TBD_NOISE = re.compile(r"^[\s*_`]+|[\s*_`.!?:;,]+$")


def _is_tbd(value: str) -> bool:
    return _TBD_NOISE.sub("", value).lower() == "tbd"


def tbd_labels(run) -> list:
    """'Section / Label' for every snapshot row whose value is TBD."""
    if run.snapshot is None:
        return []
    return [f"{title} / {label}" for title, rows in run.snapshot.sections
            for label, value in rows if _is_tbd(value)]


def _row(label: str, value_html: str) -> str:
    return f'<div class="row"><span class="k">{esc(label)}</span>{value_html}</div>'


def _meta(run, lead: str = "") -> str:
    return (f"{lead}<b>Date:</b> {esc(run.date)} &nbsp;·&nbsp; <b>Model:</b> {MODEL} "
            f"&nbsp;·&nbsp; <b>URL:</b> {esc(run.url)}")


def _md_head(run, title: str, line: str) -> str:
    return f"# {title} — {run.site}\n*{line}*\nDate: {run.date}\nModel: {MODEL}\nURL(s): {run.url}\n\n"


def _cell(text: str, keymap) -> str:
    return md_plain(text, keymap).replace("|", chr(92) + "|").replace("\n", " ")


def snapshot_rows_html(rows) -> str:
    return "".join(_row(label, "<b>TBD</b>" if _is_tbd(value) else md_to_html(value, {}))
                   for label, value in rows)


def render_snapshot(run, final: bool) -> tuple:
    """Return (html, markdown) for the Site Snapshot page."""
    snap = run.snapshot
    header = dochead(esc(f"Site Snapshot — {run.site}"), _meta(run))
    items = [(esc(title), snapshot_rows_html(rows), "") for title, rows in snap.sections]
    items.append(("Next step", f'<div class="row">{esc(SNAPSHOT_NEXT)}</div>', ""))
    body = apply_hints(f'<p class="verdict-common">{md_to_html(snap.description, {})}</p>' + sections(items))
    nav = pagenav(run, "site-snapshot") if final else ""
    html_text = page(f"Site Snapshot — {run.site}", "site-snapshot", header, body, nav, date=run.date)

    md = _md_head(run, "Site Snapshot", md_plain(snap.description, {}))
    for title, rows in snap.sections:
        md += f"## {title}\n" + "".join(f"- {label}: {md_plain(value, {})}\n" for label, value in rows) + "\n"
    md += f"## Next step\n{SNAPSHOT_NEXT}\n"
    return html_text, md


def _advice_card(n: int, headline: str, detail: str, analysis: str, keymap) -> str:
    return (f'<article class="card"><h3><span class="id">{n}</span> <span class="ttl">{esc(headline)}</span></h3>'
            f'<div class="row">{md_to_html(detail, keymap)}</div>'
            f'<div class="row">→ {md_to_html(analysis, keymap)}</div></article>')


def stated_vs_observed_html(g, keymap, wrap: bool = True) -> str:
    rows = "".join("<tr>" + "".join(f"<td>{md_to_html(c, keymap)}</td>" for c in row) + "</tr>"
                   for row in g.stated_vs_observed)
    head = "<tr><th>You said</th><th>What the page + scans show</th><th>The gap</th></tr>"
    return table_html(head + rows, wrap)


def render_goals(run, keymap, final: bool) -> tuple:
    """Return (html, markdown) for the Goals page."""
    g = run.goals
    header = dochead(
        esc(f"Goals & Discovery — {run.site}"),
        _meta(run, f'<span style="font-style:italic;color:var(--soft)">{md_to_html(g.framing, keymap)}</span><br>'))

    table = stated_vs_observed_html(g, keymap)
    items = [
        ("Owner brief", "".join(_row(label, md_to_html(value, keymap)) for label, value in g.brief), ""),
        ("Stated vs. observed", table, ""),
        ("Tensions", "".join(f'<div class="row">{md_to_html(t, keymap)}</div>' for t in g.tensions), ""),
        ("How to reach your goal",
         "".join(_advice_card(i, h, d, a, keymap) for i, (h, d, a) in enumerate(g.advice, 1)), ""),
        ("How this shapes the audit", f'<div class="row">{md_to_html(g.shapes, keymap)}</div>', ""),
        ("Next step", f'<div class="row">{esc(GOALS_NEXT)}</div>', ""),
    ]
    body = apply_hints(sections(items))
    nav = pagenav(run, "goals") if final else ""
    html_text = page(f"Goals & Discovery — {run.site}", "goals-discovery", header, body, nav, date=run.date)

    md = _md_head(run, "Goals & Discovery", md_plain(g.framing, keymap))
    md += ("## Owner brief (what they told us)\n"
           + "".join(f"- **{label}:** {md_plain(value, keymap)}\n" for label, value in g.brief) + "\n")
    md += ("## Stated vs. observed (the reality-check)\n| You said | What the page + scans show | The gap |\n"
           "|----------|----------------------------|---------|\n"
           + "".join("| " + " | ".join(_cell(c, keymap) for c in row) + " |\n"
                     for row in g.stated_vs_observed) + "\n")
    md += "## Tensions\n" + "".join(f"- {md_plain(t, keymap)}\n" for t in g.tensions) + "\n"
    md += ("## How to reach your goal (prioritised)\n"
           + "".join(f"{i}. **{h}** — {md_plain(d, keymap)} → {md_plain(a, keymap)}\n"
                     for i, (h, d, a) in enumerate(g.advice, 1)) + "\n")
    md += f"## How this shapes the audit\n- {md_plain(g.shapes, keymap)}\n\n## Next step\n{GOALS_NEXT}\n"
    return html_text, md
