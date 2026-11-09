"""Light Markdown, finding-ID links and hover hints for report prose."""
from __future__ import annotations

import html
import re

from . import DIMENSIONS, KEY_REF

HINTS = {
    "IIF": "Issue · Impact · Fix — the finding format",
    "CRO": "Conversion Rate Optimisation",
    "SEO": "Search engine optimisation — being found in search",
    "UX": "User experience — how easy the site is to use",
    "CTA": "Call to action — the button or link that asks the visitor to act",
    "MSG": "Messaging & Clarity finding",
    "DSN": "Design & Visual finding",
    "quick win": "High impact, low effort — do first",
    "big bet": "High impact, high effort — plan and schedule",
    "fill-in": "Low impact, low effort — do when convenient",
    "skip": "Low impact, high effort — backlog",
}

_PAGE_BY_PREFIX = {prefix: page for page, prefix, _t, _u in DIMENSIONS}
_TAG_LABELS = {"quickwin": "quick win", "bigbet": "big bet", "fillin": "fill-in", "skip": "skip"}


def esc(s: str, quote: bool = False) -> str:
    """Escape text. Quotes stay as typed (so curly and straight quotes read well) unless `quote` is set."""
    return html.escape(s, quote=quote)


def id_link(f) -> str:
    prefix = f.id.split("-")[0]
    if prefix not in _PAGE_BY_PREFIX:
        raise ValueError(f"finding id {f.id!r} does not start with one of "
                         f"{', '.join(_PAGE_BY_PREFIX)}; cannot link to its page")
    page = _PAGE_BY_PREFIX[prefix]
    return '<a href="%s.html" title="%s">%s</a>' % (
        page, esc(f"{f.id} — {f.title}", quote=True), esc(f.id, quote=True))


_CODE = re.compile(r"`([^`\n]+)`")
_KEY = re.compile(KEY_REF)
_LINK = re.compile(r"\[([^\]\n]+)\]\(((?:[^()\s]|\([^()\s]*\))+)\)")  # the URL may hold one level of ( )
_BOLD = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*")
_ITALIC = re.compile(r"\*(?=[^\s*])([^*\n]+?)(?<=[^\s*])\*")
_SAFE_URL = re.compile(r"(?i)^(https?://|mailto:)")
_STASH = re.compile("\x00(\\d+)\x00")


def _emphasis(s: str) -> str:
    return _ITALIC.sub(r"<i>\1</i>", _BOLD.sub(r"<b>\1</b>", s))


def md_to_html(text: str, keymap) -> str:
    # \x00 delimits stash slots, so it must not occur in prose; \r\n and \r are plain newlines.
    s = esc(text.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n"), quote=True)
    stash: list = []

    def keep(h: str) -> str:
        stash.append(h)
        return "\x00%d\x00" % (len(stash) - 1)

    s = _CODE.sub(lambda m: keep("<code>%s</code>" % m.group(1)), s)

    def key_ref(m):
        f = keymap.get(m.group(1))
        return keep(id_link(f)) if f is not None else m.group(0)

    s = _KEY.sub(key_ref, s)

    def link(m):
        if not _SAFE_URL.match(m.group(2)):
            return m.group(0)
        return keep('<a href="%s" target="_blank" rel="noopener">%s</a>'
                    % (m.group(2), _emphasis(m.group(1))))

    s = _LINK.sub(link, s)
    s = _emphasis(s)
    s = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)*", "<br><br>", s)
    # Restore (stashed items may nest, e.g. a code span inside a link label).
    while _STASH.search(s):
        s = _STASH.sub(lambda m: stash[int(m.group(1))], s)
    return s


def md_plain(text: str, keymap) -> str:
    def key_ref(m):
        f = keymap.get(m.group(1))
        return f.id if f is not None else m.group(0)

    return _KEY.sub(key_ref, text)


_SKIP_TAGS = {"a", "abbr", "code", "title", "script", "style"}
_TERMS = re.compile(
    r"(?<![\w-])(IIF|CRO|SEO|UX|CTA|MSG|DSN)(?=s?(?![\w]))(?!-\d)"
    r"|(?<![\w-])(quick win|big bet|fill-in)(?=s?(?![A-Za-z]))",
    re.IGNORECASE,
)
_TAG_NAME = re.compile(r"^<\s*(/?)\s*([A-Za-z][A-Za-z0-9-]*)")
_TAG_SPAN = re.compile(r"""(?i)^<\s*span\b[^>]*\bclass\s*=\s*["'](?:[^"']*\s)?tag(?:\s[^"']*)?["']""")


def _wrap(m) -> str:
    acro, phrase = m.group(1), m.group(2)
    if acro is not None:
        if acro != acro.upper() or acro not in HINTS:
            return m.group(0)  # acronyms are case-sensitive
        key = acro
    else:
        key = phrase.lower()
    return '<abbr title="%s">%s</abbr>' % (esc(HINTS[key], quote=True), m.group(0))


# Matches the heading builders that emit flex rows: chrome.sections (h2.section, optionally with its number
# chip) and pages_action.matrix_html (the quad h4 with its dot). If either changes, update this pattern.
_FLEX_HEAD = re.compile(r'(<h2 class="section">(?:<span class="no">\d+</span> )?|<h4><span class="dot"></span>)'
                        r'(.*?)(?=<span class="grade|<a class="openbtn"|</h[24]>)')


def _glue(m) -> str:
    # h2.section and .quad h4 are flex rows: a bare <abbr> would become its own item and
    # pick up the row gap ("Quick Win  s"), so keep the label run together in one span.
    return f"{m.group(1)}<span>{m.group(2)}</span>" if "<abbr" in m.group(2) else m.group(0)


def apply_hints(html_text: str) -> str:
    return _FLEX_HEAD.sub(_glue, _apply_hints(html_text))


def _apply_hints(html_text: str) -> str:
    depth = 0
    in_tag_span = 0  # inside <span class="tag ..."> (tag() labels carry their own title)
    out = []
    for part in re.split(r"(<[^>]+>)", html_text):
        if part.startswith("<") and part.endswith(">"):
            m = _TAG_NAME.match(part)
            if m and m.group(2).lower() in _SKIP_TAGS and not part.endswith("/>"):
                depth = max(0, depth - 1) if m.group(1) else depth + 1
            elif m and m.group(2).lower() == "span" and not part.endswith("/>"):
                if m.group(1):
                    in_tag_span = max(0, in_tag_span - 1)
                elif in_tag_span or _TAG_SPAN.match(part):
                    in_tag_span += 1
            out.append(part)
        elif depth or in_tag_span or not part:
            out.append(part)
        else:
            out.append(_TERMS.sub(_wrap, part))
    return "".join(out)


def tag(quad: str) -> str:
    label = _TAG_LABELS[quad]
    return '<span class="tag %s" title="%s">%s</span>' % (quad, esc(HINTS[label], quote=True), label)
