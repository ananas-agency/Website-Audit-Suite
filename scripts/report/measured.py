"""Measured sections rendered from the scan JSON files (HTML and Markdown together).

Every value is read defensively: a scan may omit a field, and the section then shows
"?" or "—" for it instead of failing.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from .chrome import esc

NOT_MEASURED = "not measured — available with the Extended layer"
_FALLBACK_TITLE = "Measured checks"

# page -> (section title as HTML, scan files, checks listed when none of the files exist)
_PAGES = {
    "conversion": (
        "Measurement readiness &amp; interaction (measured)",
        ("tracking.json", "interaction.json"),
        ("Analytics, tag manager and conversion-event tracking", "Consent platform and consent mode",
         "Trackers firing before consent and cookies on first load",
         "Primary CTA reaches a destination", "Form validation", "Broken links"),
    ),
    "seo": (
        "Site structure &amp; structured data (measured)",
        ("seo-sweep.json",),
        ("Pages discovered and swept", "Homepage structured data (schema types and issues)",
         "Per-page titles, descriptions, H1s and image alt text"),
    ),
    "ux-technical": (
        "Measured checks — performance, INP, security, accessibility &amp; mobile",
        ("perf-a11y.json", "mobile-metrics.json"),
        ("Core Web Vitals (LCP, CLS, FCP, TTFB, INP proxy)", "Page weight and requests",
         "HTTPS, TLS and security headers", "Accessibility (axe-core) and keyboard focus",
         "Mobile fit at 320, 390 and 414px", "Tap targets and text size on mobile"),
    ),
    "design": (
        "Design tokens &amp; rendered screenshots (measured)",
        ("design-tokens.json", "design-pages.json"),
        ("Palette, typefaces, font sizes and button styles", "Cross-page design consistency",
         "Desktop and mobile screenshots"),
    ),
}

# Checks that each scan file supplies, listed when a page has other scan files but not this one.
_FILE_CHECKS = {
    "tracking.json": _PAGES["conversion"][2][:3],
    "interaction.json": _PAGES["conversion"][2][3:],
    "perf-a11y.json": _PAGES["ux-technical"][2][:4],
    "mobile-metrics.json": _PAGES["ux-technical"][2][4:],
    "design-tokens.json": (_PAGES["design"][2][0], _PAGES["design"][2][2]),
    "design-pages.json": (_PAGES["design"][2][1],),
}

# (good limit, needs-work limit) from benchmarks-2026.md; FCP uses web.dev's 1.8s / 3s.
_LIMITS = {"lcp": (2500, 4000), "cls": (0.1, 0.25), "fcp": (1800, 3000),
           "ttfb": (800, 1800), "tbt": (200, 500)}
_SAFE_COLOR = re.compile(r"^(?:#[0-9a-fA-F]{3,8}|(?:rgb|rgba|hsl|hsla)\([0-9a-zA-Z\s.,%/-]*\))$")


# ---- tiny builders: every piece is a (html, md) pair -------------------------------------------

def _t(x) -> tuple:
    s = "?" if x is None else str(x)
    return esc(s), s


def _join(*parts) -> tuple:
    parts = [_t(p) if not isinstance(p, tuple) else p for p in parts]
    return "".join(p[0] for p in parts), "".join(p[1] for p in parts)


def _pill(label: str, good: bool) -> tuple:
    return f'<span class="pill {"covered" if good else "gap"}">{esc(label)}</span>', label


def _yesno(flag, good_when_true: bool = True) -> tuple:
    return _pill("yes" if flag else "no", bool(flag) == good_when_true)


def _rate(key: str, value) -> tuple:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return '<span class="tag skip">—</span>', "—"
    good, ok = _LIMITS[key]
    if v <= good:
        return _pill("good", True)
    return _pill("needs work", False) if v <= ok else _pill("poor", False)


def _sub(text: str) -> tuple:
    return (f'<div class="row" style="font-weight:650;margin:14px 0 4px">{esc(text)}</div>', f"### {text}\n\n")


def _row(label: str, *value) -> tuple:
    v = _join(*value)
    return f'<div class="row"><span class="k">{esc(label)}</span>{v[0]}</div>', f"- **{label}:** {v[1]}\n"


def _note(text: str) -> tuple:
    return f'<div class="row"><span class="verdict-common">{esc(text)}</span></div>', f"_{text}_\n\n"


def _table(headers, rows) -> tuple:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c[0]}</td>" for c in r) + "</tr>" for r in rows)
    md = "| " + " | ".join(headers) + " |\n|" + "---|" * len(headers) + "\n"
    for r in rows:
        md += "| " + " | ".join(c[1].replace("|", "\\|").replace("\n", " ") for c in r) + " |\n"
    return f'<div class="tablewrap"><table><tr>{head}</tr>{body}</table></div>', md + "\n"


def _cat(parts) -> tuple:
    return "".join(p[0] for p in parts), "".join(p[1] for p in parts)


NR = "not recorded"


def _nr() -> tuple:
    return '<span class="tag skip">not recorded</span>', NR


def _has(d: dict, key: str) -> bool:
    return d.get(key) is not None


def _names(d: dict, key: str, empty: str) -> str:
    """Comma list of d[key]; `empty` when the key holds an empty list; NR when the key is absent."""
    if not _has(d, key):
        return NR
    return ", ".join(map(str, _l(d[key]))) or empty


def _yn_key(d: dict, key: str, good_when_true: bool = True) -> tuple:
    """yes/no pill from the truthiness of d[key]; 'not recorded' when the key is absent."""
    return _yesno(d[key], good_when_true) if _has(d, key) else _nr()


def _d(x) -> dict:
    return x if isinstance(x, dict) else {}


def _l(x) -> list:
    return x if isinstance(x, list) else []


def _short(url) -> str:
    return re.sub(r"^https?://[^/]+", "", str(url or "")) or "/"


def run_file(run_dir, name):
    """The file `name` inside the run folder, or None. Only a plain file name is accepted: no folder,
    no `..`, no absolute path, so a scan or audit.json can't point the report at files elsewhere."""
    name = str(name or "")
    if not name or name in (".", "..") or any(c in name for c in "/\\:\x00"):
        return None
    path = Path(run_dir) / name
    return path if path.is_file() else None


def _figure(run, src_file, alt, caption, final, style) -> tuple:
    """A screenshot figure, or an empty pair when the file is not in the run folder."""
    if run_file(run.dir, src_file) is None:
        return "", ""
    src = ("assets/" if final else "") + str(src_file)
    h = (f'<figure style="{style}"><img src="{esc(src)}" alt="{html.escape(alt)}" '
         'style="width:100%;height:auto;border:1px solid var(--line);border-radius:2px">'
         f'<figcaption style="font-size:12px;color:var(--soft);text-align:center;margin-top:4px">'
         f'{esc(caption)}</figcaption></figure>')
    return h, f"![{alt}]({src})\n\n"


def _figures(figs) -> tuple:
    figs = [f for f in figs if f[0]]
    if not figs:
        return "", ""
    return ('<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:12px">'
            + "".join(f[0] for f in figs) + "</div>"), "".join(f[1] for f in figs)


# ---- one function per scan file ----------------------------------------------------------------

def _perf_a11y(scan) -> list:
    perf, a11y = _d(scan.get("perf")), _d(scan.get("a11y"))
    sec, kbd = _d(scan.get("security")), _d(scan.get("keyboard"))
    vit = _d(perf.get("vitals"))
    vrows = [
        (_t("LCP — largest content paints"), _join(vit.get("lcp"), " ms"), _t("≤ 2500 ms"), _rate("lcp", vit.get("lcp"))),
        (_t("CLS — layout shift"), _t(vit.get("cls")), _t("≤ 0.1"), _rate("cls", vit.get("cls"))),
        (_t("FCP — first paint"), _join(vit.get("fcp"), " ms"), _t("≤ 1800 ms"), _rate("fcp", vit.get("fcp"))),
        (_t("TTFB — server response"), _join(perf.get("ttfb"), " ms"), _t("≤ 800 ms"), _rate("ttfb", perf.get("ttfb"))),
        (_t("INP proxy — Total Blocking Time"), _join(vit.get("tbt"), " ms"), _t("≤ 200 ms"), _rate("tbt", vit.get("tbt"))),
    ]
    heavy = ", ".join(f'{b.get("name", "?")} ({b.get("kb", "?")} KB)'
                      for b in _l(perf.get("biggest"))[:3] if isinstance(b, dict)) or "—"
    headers = _d(sec.get("headers"))
    have_headers = isinstance(sec.get("headers"), dict)
    present = [k for k, v in headers.items() if v]
    missing = [k for k, v in headers.items() if not v]
    tls = f' · {sec["tls"]}' if sec.get("tls") else ""
    https = NR if not _has(sec, "https") else ("HTTPS" if sec["https"] else "NOT HTTPS")
    by = _d(a11y.get("byImpact"))
    top = [v for v in _l(a11y.get("top")) if isinstance(v, dict)]
    parts = [
        _sub("Performance — lab Core Web Vitals + INP proxy"),
        _table(["Core Web Vital (lab, mobile)", "Measured", "2026 target", "Status"], vrows),
        _row("Weight", f'{perf.get("totalKB", "?")} KB over {perf.get("requests", "?")} requests '
             f'(images {perf.get("imgKB", "?")} KB, JavaScript {perf.get("jsKB", "?")} KB) · '
             f'{perf.get("thirdPartyHosts", "?")} third-party hosts · heaviest: {heavy}'),
        _note("Lab run (one emulated mobile load); the INP figure is the standard lab proxy "
              "(Total Blocking Time). Real-world field percentiles need many real users and are out of scope."),
        _sub("Security (measured from the response)"),
        _row("HTTPS / TLS", https + tls
             + f' · status {sec.get("status", "?")}'),
        _row("Security headers present", (", ".join(present) or "none") if have_headers else NR),
        _row("Security headers missing", (", ".join(missing) or "none") if have_headers else NR),
        _row("Mixed content", f'{perf["mixedContent"]} http assets on the https page'
             if _has(perf, "mixedContent") else NR),
        _sub("Accessibility — axe-core + keyboard"),
        _row("axe-core (WCAG)", f'{a11y.get("violations", "?")} violation types'
             + ((" — " + ", ".join(f"{k}: {n}" for k, n in by.items())) if by else "")),
    ]
    if top:
        parts.append(_table(["Rule", "Impact", "Elements", "What"], [
            (_t(v.get("id")), _t(v.get("impact")), _t(v.get("nodes")), _t(v.get("help"))) for v in top]))
    parts += [
        _row("Keyboard focus", f'{kbd.get("tabStops", "?")} tab stops reached; '
             f'{kbd.get("noFocusIndicator", "?")} with no visible focus indicator'),
        _note("axe-core and the keyboard pass catch the automatable share of WCAG; "
              "full screen-reader testing is manual and out of scope."),
    ]
    return parts


def _mobile(run, scan, final) -> list:
    widths = {str(w): _d(m) for w, m in _d(scan.get("widths")).items()}
    rows = []
    for w, m in widths.items():
        if not isinstance(m.get("fits"), bool):
            fits = _nr()
        elif m["fits"]:
            fits = _pill("fits", True)
        else:
            fits = ('<span class="tag skip">overflows</span>', "overflows")
        rows.append((_t(f"{w}px"), fits, _t(m.get("overflowCount")), _t(m.get("oversizedImgCount")),
                     _t(m.get("smallTapCount")), _t(m.get("smallTextCount"))))
    parts = [_sub("Mobile — three phone widths"),
             _table(["Viewport", "Fits screen?", "Elements too big", "Oversized images",
                     "Tap targets <44px", "Text <12px"], rows)]
    parts.append(_figures([
        _figure(run, m.get("screenshot"), f"Page at {w}px", f"{w}px render", final,
                "margin:0;flex:1;min-width:120px;max-width:200px") for w, m in widths.items()]))
    parts.append(_note("Measured with a headless-Chrome render at three phone widths."))
    return parts


def _design_tokens(run, scan, final) -> list:
    tok = _d(scan.get("tokens"))
    palette = []
    for v, _c in ([x for x in _l(tok.get("topBackgrounds")) if isinstance(x, list) and x]
                  + [x for x in _l(tok.get("topTextColors")) if isinstance(x, list) and x]):
        v = str(v)
        if v not in palette and "0)" not in v and _SAFE_COLOR.match(v):
            palette.append(v)
    palette = palette[:8]
    swatches = "".join(
        f'<span title="{html.escape(v)}" style="display:inline-block;width:18px;height:18px;background:{html.escape(v)};'
        'border:1px solid #ccc;border-radius:2px;vertical-align:middle;margin-right:6px"></span>' for v in palette)
    pal_row = (
        f'<div class="row"><span class="k">Palette (measured)</span>{swatches} '
        f'<span class="verdict-common">{esc(str(tok.get("distinctTextColors", "?")))} text colours · '
        f'{esc(str(tok.get("distinctBackgrounds", "?")))} backgrounds</span></div>',
        f'- **Palette (measured):** {", ".join(palette) or "—"} ({tok.get("distinctTextColors", "?")} text colours, '
        f'{tok.get("distinctBackgrounds", "?")} backgrounds)\n')
    fams = ", ".join(str(f[0]) for f in _l(tok.get("fontFamilies")) if isinstance(f, list) and f) or "—"
    shots = _d(scan.get("screenshots"))
    return [
        pal_row,
        _row("Typeface(s)", f'{fams} · {tok.get("distinctFontSizes", "?")} distinct font sizes'
             + (f' · weights {", ".join(map(str, _l(tok.get("fontWeights"))))}' if tok.get("fontWeights") else "")),
        _row("Button styles", f'{tok.get("distinctButtonStyles", "?")} distinct (fewer is more consistent)'),
        _figures([
            _figure(run, shots.get("desktop"), "Desktop render", "Desktop render", final, "margin:0;flex:2;min-width:260px"),
            _figure(run, shots.get("mobile"), "Mobile render", "Mobile render", final,
                    "margin:0;flex:1;min-width:120px;max-width:220px")]),
    ]


def _design_pages(scan) -> list:
    cons = _d(scan.get("consistency"))
    rows = [(_t(_short(p.get("url"))), _t(p.get("font")), _t(p.get("fontSizes")), _t(p.get("buttonStyles")))
            for p in _l(cons.get("perPage")) if isinstance(p, dict)]
    if "fontsConsistent" not in cons or not isinstance(cons["fontsConsistent"], bool):
        verdict = _t(NR)
    else:
        verdict = _pill("consistent", True) if cons["fontsConsistent"] else _pill("drift", False)
    return [
        _sub("Design consistency across pages"),
        _row("Across " + str(cons.get("pages", "?")) + " pages", "Primary typeface ", verdict,
             f' ({", ".join(map(str, _l(cons.get("primaryFonts"))))}) · palette union {cons.get("paletteUnion", "?")} '
             f'colours · button styles union {cons.get("buttonStylesUnion", "?")}'),
        _table(["Page", "Typeface", "Font sizes", "Button styles"], rows) if rows else ("", ""),
        _note("Measured by rendering each page."),
    ]


def _seo_sweep(scan) -> list:
    schema = _d(scan.get("home_schema"))
    types = _names(schema, "types", "none")
    issues = _names(schema, "issues", "none")
    parts = [
        _row("Pages", f'discovered {scan.get("discovered", "?")}, swept {scan.get("swept", "?")} '
             f'(about {scan.get("per_type", "?")} per page type)'),
        _row("Homepage schema", f'types: {types} · issues: {issues}'),
    ]
    rows = []
    for r in (x for x in _l(scan.get("rows")) if isinstance(x, dict)):
        if not r.get("ok"):
            rows.append((_t(_short(r.get("url"))), _t(r.get("type")), _t(f'status {r.get("status", "?")}'),
                         _t(""), _t(""), _t(""), _t(""), _t(""), _t("")))
            continue
        rows.append((_t(_short(r.get("url"))), _t(r.get("type")), _t(r.get("title_len")), _t(r.get("desc_len")),
                     _t(r.get("h1_count")), _t(r.get("words")), _t(f'{r.get("imgs_alt", "?")}/{r.get("imgs", "?")}'),
                     _t(r.get("schema")), _t(", ".join(map(str, _l(r.get("flags")))))))
    if rows:
        parts.append(_table(["Page", "Type", "Title len", "Desc len", "H1", "Words", "Alt", "Schema", "Flags"], rows))
    parts.append(_note("Swept statically. The 2026 bar is unique 50–60-character titles, one H1, schema and a canonical."))
    return parts


def _tracking(scan) -> list:
    a, c = _d(scan.get("analytics")), _d(scan.get("cookies"))
    fired = _d(scan.get("firedOnLoadByCategory"))
    tools = (", ".join(map(str, scan["detected"])) or "—") if isinstance(scan.get("detected"), dict) else NR
    n_tools = _t(len(scan["detected"])) if isinstance(scan.get("detected"), dict) else _nr()
    counts = [fired.get("marketing"), fired.get("analytics")]
    if all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in counts):
        before_txt = f"{sum(counts):g} tracker(s) fire before consent"
    else:
        before_txt = NR  # a count needs both categories; a partial one would understate it
    if _has(scan, "consentMode"):
        gated_cells = (_yesno(scan["consentMode"]),
                       _t("gated" if scan["consentMode"] else before_txt))
    else:
        gated_cells = (_nr(), _t(before_txt))
    rows = [
        (_t("Analytics installed (GA4)"), _yn_key(a, "ga4"), _t(_names(a, "ga4", "—"))),
        (_t("Tag manager (GTM)"), _yn_key(a, "gtm"), _t(_names(a, "gtm", "not used"))),
        (_t("Pixels and tracking tools detected"), n_tools, _t(tools)),
        (_t("Consent platform (CMP)"), _yn_key(scan, "cmp"), _t(_names(scan, "cmp", "none detected"))),
        (_t("Consent Mode / trackers gated"),) + gated_cells,
    ]
    names = ", ".join(map(str, _l(c.get("names"))))
    if _has(c, "total"):
        cookies = (f'{c["total"]} ({c.get("analytics", NR)} analytics, {c.get("marketing", NR)} marketing, '
                   f'{c.get("thirdParty", NR)} third-party)' + (f" — {names}" if names else ""))
    else:
        cookies = NR
    return [
        _table(["Check", "Status", "Detail"], rows),
        _row("Cookies on first load", cookies),
        _note("Measured read-only with a headless render on a fresh load."),
    ]


def _interaction(scan) -> list:
    rows = []
    for r in (x for x in _l(scan.get("pages")) if isinstance(x, dict)):
        cta, form = r.get("cta"), r.get("form")
        if "cta" not in r:
            cta_cell = _nr()
        elif cta is not None and not isinstance(cta, dict):
            cta_cell = _nr()
        elif isinstance(cta, dict):
            cta_cell = _join(f'"{cta.get("text", "?")}" → {cta.get("dest", "?")}',
                             _pill("dead", False) if cta.get("dead") else ("", ""))
        else:
            cta_cell = _pill("none detected above the fold", False)
        if "form" not in r:
            form_cell = _nr()
        elif form is not None and not isinstance(form, dict):
            form_cell = _nr()
        elif isinstance(form, dict):
            blocks = (NR if not _has(form, "blocksEmptySubmit")
                      else "yes" if form["blocksEmptySubmit"] else "no")
            form_cell = _t(f'{form.get("fields", "?")} fields, {form.get("required", "?")} required, blocks empty '
                           f'submit: {blocks}'
                           + (f', submit "{form["submitLabel"]}"' if form.get("submitLabel") else ""))
        else:
            form_cell = _join(_pill("no form", False),
                              f' ({r["formsOnPage"]} form tags)' if _has(r, "formsOnPage") else "")
        rows.append((_t(_short(r.get("url"))), cta_cell, form_cell))
    links = _d(scan.get("links"))
    parts = [_sub("Conversion path — interaction & links (measured, never submits)")]
    if rows:
        parts.append(_table(["Page", "Primary CTA → destination", "Main form (not submitted)"], rows))
    parts += [
        _row("Links", f'{links["checked"]} checked' if _has(links, "checked") else NR,
             f' · {len(_l(links["broken"]))} broken' if _has(links, "broken") else ""),
        _note("Driven read-only — CTAs are followed and forms validated, but never submitted."),
    ]
    return parts


# ---- public entry point ------------------------------------------------------------------------

def measured_sections(run, page: str, final: bool) -> list:
    """(title, html, md) sections backed by the run's scan JSON; [] for pages with none."""
    if page not in _PAGES:
        return []
    title, files, checks = _PAGES[page]
    scans = dict(run.scans or {})
    present = [f for f in files if f in scans]
    if not present:
        items = [(f'<ul class="clean">' + "".join(f"<li>{esc(c)} — {NOT_MEASURED}</li>" for c in checks) + "</ul>",
                  "".join(f"- {c} — {NOT_MEASURED}\n" for c in checks) + "\n")]
        return [(_FALLBACK_TITLE, items[0][0], items[0][1])]
    parts = []
    for name in present:
        s = _d(scans[name])
        if name == "perf-a11y.json":
            parts += _perf_a11y(s)
        elif name == "mobile-metrics.json":
            parts += _mobile(run, s, final)
        elif name == "design-tokens.json":
            parts += _design_tokens(run, s, final)
        elif name == "design-pages.json":
            parts += _design_pages(s)
        elif name == "seo-sweep.json":
            parts += _seo_sweep(s)
        elif name == "tracking.json":
            parts += _tracking(s)
        elif name == "interaction.json":
            parts += _interaction(s)
    missing = [c for f in files if f not in scans for c in _FILE_CHECKS.get(f, ())]
    if missing:
        parts.append(("<ul class=\"clean\">" + "".join(f"<li>{esc(c)} — {NOT_MEASURED}</li>" for c in missing) + "</ul>",
                      "".join(f"- {c} — {NOT_MEASURED}\n" for c in missing) + "\n"))
    h, m = _cat(parts)
    return [(title, f'<div class="card">{h}</div>', m)]
