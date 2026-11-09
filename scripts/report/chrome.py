"""Page frame, section wrapper, page walk and file writing for the report pages."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from . import DIMENSIONS
from .text import esc

LOGO = "https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png"
_UTM = "?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content="
AG = "https://ananas-agency.com/" + _UTM
PKG = "https://website-audit-suite.ananas-agency.com/" + _UTM
PRINTHINT = ('<p class="printhint">\U0001f5a8 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> '
             '(<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>')

_CSS_PATH = Path(__file__).resolve().parent / "style.css"

_FIXED_TITLES = {
    "report": "Audit Report",
    "site-snapshot": "Site Snapshot",
    "goals": "Goals & Discovery",
    "action-report": "Action Report",
}
_DIM_TITLES = {page: title for page, _prefix, title, _utm in DIMENSIONS}


def page_title(name: str) -> str:
    return _FIXED_TITLES.get(name) or _DIM_TITLES[name]


def page_file(run, name: str) -> str:
    """File basename (no extension) of a page in the walk."""
    return f"_{run.slug}-website-audit-report" if name == "report" else name


@lru_cache(maxsize=None)
def _read_css() -> str:
    return _CSS_PATH.read_text(encoding="utf-8")


def table_html(inner: str, wrap: bool) -> str:
    """A table, in a .tablewrap when `wrap` (own pages) or bare and full-width (consolidated report)."""
    if wrap:
        return f'<div class="tablewrap"><table>{inner}</table></div>'
    return f'<table style="width:100%">{inner}</table>'


def brandband(utm: str) -> str:
    return ('<div class="brandband"><div class="bwrap">'
            f'<a class="pkgname" href="{PKG}{utm}" target="_blank" rel="noopener">Website Audit Suite</a>'
            f'<a class="brandlink" href="{AG}{utm}" target="_blank" rel="noopener">'
            f'<span class="byline">by</span><img class="brandlogo" src="{LOGO}" alt="Ananas Agency"></a>'
            '</div></div>')


def footer(utm: str, date: str) -> str:
    year = date[:4]
    return ('<footer class="doc"><div class="fwrap">'
            f'<a class="brandlink" href="{AG}{utm}" target="_blank" rel="noopener">'
            f'<img class="footlogo" src="{LOGO}" alt="Ananas Agency"></a>'
            '<a class="footmail" href="mailto:juicy@ananas-agency.com">juicy@ananas-agency.com</a>'
            f'<div>© {esc(year)} Ananas-Agency — generated {esc(date)}. MIT License.</div></div></footer>')


def page(title: str, utm: str, header_html: str, body_html: str, nav_html: str = "",
         *, date: str = "") -> str:
    """The full document. `title` is plain text (escaped here); `date` feeds the footer."""
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
            f"<title>{esc(title)}</title>\n<style>\n{_read_css()}\n</style>\n</head>\n<body>\n"
            f"{brandband(utm)}\n"
            f'<div class="wrap">\n{header_html}\n{body_html}\n{nav_html}\n{PRINTHINT}\n</div>\n'
            f"{footer(utm, date)}\n</body>\n</html>\n")


def dochead(h1: str, meta_html: str, tagline: str = "") -> str:
    tag = f'<p class="tagline">{tagline}</p>' if tagline else ""
    return f'<header class="doc"><h1>{h1}</h1>{tag}<div class="meta">{meta_html}</div></header>'


def sections(items: list) -> str:
    """items: (title, inner, open_href). Numbers the chips only when there are 2 or more items."""
    numbered = len(items) >= 2
    out = []
    for n, (title, inner, open_href) in enumerate(items, 1):
        btn = f'<a class="openbtn" href="{open_href}">Open full document →</a>' if open_href else ""
        no = f'<span class="no">{n}</span> ' if numbered else ""
        out.append(f'<section class="block"><h2 class="section">{no}{title}{btn}</h2>{inner}</section>')
    return "".join(out)


def walk(run) -> list:
    """Names of the pages that will exist, in reading order (the report is always first)."""
    names = ["report"]
    if run.snapshot is not None:
        names.append("site-snapshot")
    if run.goals is not None:
        names.append("goals")
    names += [page_ for page_, *_ in DIMENSIONS if page_ in run.dims]
    if run.action is not None:
        names.append("action-report")
    return names


def pagenav(run, name: str) -> str:
    names = walk(run)
    i = names.index(name)

    def link(n: str) -> tuple:
        return f"{page_file(run, n)}.html", esc(page_title(n))

    prev_html = ('<span></span>' if i == 0 else
                 '<a class="prevbtn" href="%s">← %s</a>' % link(names[i - 1]))
    next_html = ('' if i == len(names) - 1 else
                 '<a class="nextbtn" href="%s">%s →</a>' % link(names[i + 1]))
    return f'<div class="pagenav">{prev_html}{next_html}</div>'


def write_page(run_dir, name: str, html_text: str, md_text) -> None:
    """Write <name>.html and <name>.md as UTF-8 with LF newlines (md skipped when None)."""
    run_dir = Path(run_dir)
    with open(run_dir / f"{name}.html", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html_text)
    if md_text is not None:
        with open(run_dir / f"{name}.md", "w", encoding="utf-8", newline="\n") as fh:
            fh.write(md_text)
