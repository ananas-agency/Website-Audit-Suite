# Design & Visual Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
adds the design-specific fast tests, the design scan, the scoring rubric, worked finding examples, and the
HTML output format.

## What is measured vs. what is expert judgement (read this first)

This dimension mixes two very different kinds of evidence, and the **honesty rule** requires you keep them
apart:

**MEASURED, objective, from `scripts/design-scan.py`.** The token **counts** are computed from the
rendered page's real styles, so quote them as facts:
- the **typeface(s)** actually in use (top font families),
- the **count of distinct font sizes** (and the weights present),
- the **colour palette**: the count of distinct text colours and backgrounds, plus the top ones,
- the **count of distinct button styles**: a design-system coherence signal (fewer is more consistent).

**EXPERT-SUBJECTIVE: the visual read, from looking at the screenshots.** Whether the hierarchy leads the
eye, whether the layout is balanced, whether the imagery is quality, whether it looks modern or dated, and
whether it reads as trustworthy, these are **expert judgements grounded in the benchmarks-2026.md §4
UI/UX principles** (Nielsen's 10 heuristics, visual hierarchy, consistency/Jakob's Law, aesthetic &
minimalist design, the aesthetic-usability effect, Stanford Web Credibility), **not lab metrics**. Label
them as judgement, never as measurement.

**A true "off-brand" call needs brand guidelines.** Deciding a colour or font is *off-brand* requires the
company's real **colours, fonts, and logo**. Without them, judge **general design quality + internal
consistency** only, and **ask the user for their brand guidelines** if they want brand-fit assessed.

**If there's no headless browser**, fall back to a **user-provided screenshot**; if none, mark the visual
read **"not assessed"** and ask for one; never invent what the page looks like.

| To assess… | How | In the report, mark |
|------------|-----|---------------------|
| Design tokens (colours, fonts, sizes, button styles) | **`scripts/design-scan.py`** (bundled) | **measured** (or "not available" if no browser/screenshot) |
| Visual hierarchy, whitespace, imagery, modern-vs-dated, polish | **Look at the rendered screenshots** | **expert judgement** (benchmarks §4 UI/UX) |
| Brand-fit / "off-brand" | Needs the company's **brand guidelines** | "not assessed — brand guidelines needed" |

---

## The design scan (the correct way to check "how does it look?")

Static HTML tells you nothing about how a page actually looks; that depends on CSS, images, and layout at a
real screen width. So render the page and both measure its tokens and capture it for the eye.

**Run it** (needs Playwright: `pip install playwright && playwright install chromium`; it bundles its own Chromium, no browser to install):
```
python scripts/design-scan.py <URL> --pages <one-article,one-service-page,one-case-study> --out <folder>
```
It renders the homepage at desktop (1440px) and mobile (390px, 2× density), extracts the design tokens from
computed styles, and saves full-page screenshots. With `--pages`, it also renders **one representative page
per key interior template** (an article, a service/offering page, a case study), screenshots each, and
measures their readability. Interior templates are where most real design problems live, so always pass them.

**What it produces:**

| Artefact | What it gives you |
|----------|-------------------|
| **`design-tokens.json`** | The full measured homepage tokens (raw counts + top colours/fonts/sizes/button styles). |
| **`design-scan.md`** | A readable summary: typeface(s), # distinct font sizes + weights, # distinct colours, # distinct button styles, plus the interior-template readability table. |
| **`design-desktop.png`** / **`design-mobile.png`** | Full-page homepage renders for the visual read. |
| **`page-<slug>.png`** (with `--pages`) | Full-page render of each interior template for the visual read. |
| **`design-pages.json`** (with `--pages`) | Cross-page token consistency + **per-page readability** (alignment, chars-per-line, words-per-visual). |

**Interior-template readability thresholds** (from `design-pages.json`; benchmarks-2026.md §4):

| Signal | Good | Flag it |
|--------|------|---------|
| **Body text-alignment** | `left` (or `justify` with care) | `center` on long body copy: hard to read (a `DSN-`/`UX-` finding) |
| **Characters per line** | ~45-75 | > 75 (lines too long) or < 40 (too narrow) |
| **Words per visual** | mixed (text + graphics) | very high (e.g. 100+): a wall of text with no diagrams or section variety |

**The consistency signals to read off the tokens** (fewer is more coherent; these are guides, not hard
thresholds):

| Token | Coherent | Getting noisy | Ad-hoc |
|-------|----------|---------------|--------|
| **Button styles** | 1–3 (primary/secondary/tertiary) | 4–6 | 7+ (no design system) |
| **Distinct font sizes** | ~4–8 (a type scale) | 9–12 | 13+ (no scale) |
| **Typefaces** | 1–2 (or a deliberate pair) | 3 | 4+ |
| **Core palette** | a controlled set (a few brand + neutrals) | drifting | dozens of unrelated colours |

**Then LOOK.** Open both screenshots and judge the things the counts can't: does one focal point emerge,
is the composition aligned and balanced, is there breathing room or is it crammed, is the imagery custom
and sharp or generic/low-res, does it look current or dated, is the colour harmonious, and does the whole
read as professional and trustworthy, on desktop **and** on the phone. Turn each problem into a `DSN-`
finding that pairs the number with the observation.

---

## The design fast tests

Run these fast before the full rubric; they surface the biggest issues quickly.

### The squint test
Blur your eyes (or mentally squint) at the rendered page. Does **one element, the primary action,
emerge as the clear focal point**, so the eye lands on it first, and does the overall layout feel
**balanced** (weight distributed, not lopsided or crammed to one side)? If everything competes at the same
visual weight, nothing stands out, or the composition is unbalanced, the **visual hierarchy** isn't guiding
the visitor. This is the visual analogue of the messaging 5-second test.

### The 5-second impression
Glance at the page for five seconds, as a first-time visitor would. Does it look **modern, professional,
and trustworthy**, or dated, generic, or amateur? First impressions form in well under a second and drive
credibility (the *aesthetic-usability effect*: a cleaner, more current design is also **trusted** more;
Stanford Web Credibility). Note the gut reaction and what drives it (dated gradients, clip-art, clutter, a
tidy modern grid).

### The consistency count
From the scan, count the **button styles**, the **distinct font sizes**, and the **distinct colours**. A
tight set (a few buttons, a real type scale, a controlled palette) signals a coherent **design system**; a
sprawling set (a dozen button styles, fifteen font sizes, colours everywhere) signals an ad-hoc build that
will read as inconsistent and unpolished. Quote the numbers.

---

## Scoring rubric (weights sum to 100)

Rate each criterion **Pass** (full weight), **Partial** (half), or **Fail** (0). Sum → 0–100 → letter
grade. Always show this table in the deliverable so the grade is explainable. Criteria marked
**(measured)** are anchored to a `design-scan.py` token count; the rest are **expert judgement** from the
rendered screenshots (benchmarks §4 UI/UX); note that in the finding.

**Judge each criterion across the homepage AND the sampled interior templates** (see "Read the interior
templates" in the SKILL). A template-level problem counts against the relevant criterion, e.g. a wall-of-text
service page hits **Visual hierarchy** and **Whitespace & density**; centred body copy or over-long lines on
an article hit **Typography**. Don't let a polished homepage hide broken interior templates.

| # | Criterion | What "Pass" looks like | Weight |
|---|-----------|------------------------|:------:|
| 1 | **Visual hierarchy** | One clear focal point; the eye is led to the primary action; size, colour, and spacing rank importance. | 12 |
| 2 | **Design-system consistency** *(measured — # button styles)* | Buttons, components, and spacing are consistent; a tight, reused set (few button styles), not ad-hoc. | 12 |
| 3 | **Typography** *(measured — # font families / # font sizes)* | A coherent typeface (or a deliberate pair) and a tight type scale; legible size and line length. | 12 |
| 4 | **Colour & palette** *(measured — # distinct colours)* | A controlled, harmonious, on-brand palette with sufficient contrast; not a scatter of unrelated colours. | 10 |
| 5 | **Layout, grid & alignment** | Structured, aligned, balanced composition; elements sit on a grid, edges line up. | 10 |
| 6 | **Whitespace & density** | Uncluttered, with breathing room; content isn't crammed or overwhelming. | 10 |
| 7 | **Imagery & media quality** | High-quality, relevant, consistent imagery — custom over generic stock, sharp resolution, no distortion. | 8 |
| 8 | **Modern vs dated** | Follows current design conventions; doesn't look visibly old (no 2010-era gradients/bevels/clip-art). | 8 |
| 9 | **Brand coherence & credibility** | Professional, trustworthy, a consistent identity — the aesthetic-usability effect: good design is trusted more. | 10 |
| 10 | **Mobile visual quality** *(measured — mobile render)* | The design itself (not just the responsive layout) holds up and looks good on a phone. | 8 |

> A criterion can generate **more than one finding** (e.g. two separate imagery problems), but score the
> criterion once overall. Findings are the fix list; the rubric is the grade.

Grade bands (from report-format.md): A 90–100 · B 80–89 · C 70–79 · D 60–69 · F 0–59.

---

## Worked finding examples (Issue · Impact · Fix)

**DSN-01 — 11 distinct button styles; no coherent design system** · Impact 3 · Effort 3 · **big bet**
- **Issue:** `design-scan.py` measured **11 distinct button styles** on the homepage (different fills,
  border radii, and padding), and the screenshots confirm it: the hero CTA, the nav button, and the card
  buttons all look different. *(Design system = a consistent, reused set of colours, type, and buttons.)*
- **Impact:** An ad-hoc button set reads as unpolished and makes the primary action harder to spot; every
  button competing dilutes the one that matters, and inconsistency quietly erodes trust (aesthetic-usability
  effect).
- **Fix:** Collapse to **two button styles**, one primary (the main CTA) and one secondary, with a single
  shared radius, padding, and colour rule, applied site-wide. Define them once as reusable components.
- **Evidence:** design-scan: 11 distinct button styles; buttonRadii include 0px, 4px, 8px, 24px, 999px.

**DSN-02 — Dated hero: glossy gradient, bevels, and a 2012-era look** · Impact 4 · Effort 3 · **big bet**
- **Issue:** The hero (desktop screenshot) uses a glossy top-to-bottom gradient, beveled buttons with
  drop shadows, and a skeuomorphic badge: visual conventions that read as roughly a decade old.
- **Impact:** The 5-second impression is "dated", which via the aesthetic-usability effect lowers perceived
  quality and trust before the visitor reads a word, costly on the primary entry page. *(Expert judgement
  against benchmarks §4 UI/UX, not a lab metric.)*
- **Fix:** Modernise the hero to current conventions: flat or subtly-layered colour, a clean sans type
  scale, generous whitespace, a single high-contrast primary button, and a sharp real photograph or a
  simple custom graphic instead of the badge.
- **Evidence:** `design-desktop.png`: glossy gradient hero + beveled/drop-shadowed buttons.

**DSN-03 — Cluttered layout with no clear focal point** · Impact 4 · Effort 3 · **big bet**
- **Issue:** The squint test fails: on the blurred desktop screenshot nothing stands out; the first screen
  packs a headline, two promo banners, a carousel, and six equal-weight cards with almost no whitespace.
  The scan backs this up: **9 distinct font sizes**, so text weight doesn't rank anything.
- **Impact:** With no focal point the eye has nowhere to land and the primary action gets lost in the
  noise; visitors don't know where to look or what to do next, hurting the main conversion.
- **Fix:** Establish one focal point: give the hero and its single primary CTA room and dominant weight,
  demote the promos below the fold, add generous whitespace, and cut the type scale to ~5 sizes so size
  signals importance.
- **Evidence:** design-scan: 9 distinct font sizes; `design-desktop.png`: dense first screen, no
  dominant element.

**DSN-04 — Low-quality generic stock imagery** · Impact 3 · Effort 2 · **fill-in**
- **Issue:** The three "team"/"service" images are recognisable generic stock photos (a posed handshake, a
  smiling headset agent), one visibly stretched out of its aspect ratio.
- **Impact:** Generic stock reads as impersonal and less credible than real imagery, and the distortion
  looks careless; both weaken the professional, trustworthy impression the page needs to make.
- **Fix:** Replace with real, on-brand photography (the actual team, product, or work) at correct aspect
  ratio and resolution; if stock is unavoidable, choose authentic, non-cliché shots and keep them
  consistent in tone.
- **Evidence:** `design-desktop.png`: posed-handshake stock image, ~third image stretched horizontally.

**Strength worth noting** (not a finding, but record it): "The palette is controlled (design-scan shows a
tight core of a brand navy, one warm accent, and neutral greys), and the type is a single clean sans on a
consistent scale; the base design system is coherent."

### Anti-patterns to catch (each becomes a finding)
- **Too many fonts / sizes:** 3+ typefaces or a sprawling, scale-less set of font sizes (measured).
- **Too many colours:** a scatter of unrelated colours with no controlled core palette (measured).
- **Inconsistent buttons:** many different button styles, radii, and sizes; no reusable component set
  (measured).
- **Generic stock photos:** cliché, impersonal, or distorted imagery instead of real, on-brand visuals.
- **Cluttered / dense layout:** everything crammed together, no whitespace, overwhelming first screen.
- **Poor alignment:** elements off-grid, ragged edges, nothing lining up.
- **Dated gradients / shadows / bevels:** glossy gradients, heavy drop shadows, skeuomorphic or clip-art
  styling that reads as a decade old.
- **No clear focal point:** everything the same visual weight; the eye has nowhere to land.
- **Low-contrast decoration over text:** decorative imagery or busy backgrounds behind copy that hurt
  legibility (ties to §3 Accessibility contrast).

---

## Output file format

### File 1: `design.md` (Markdown)

```markdown
# Design & Visual — [Site name]
Date: [date]
Model: Ananas-Agency Website Audit
Graded against: benchmarks-2026.md (§4 UI/UX)
Primary goal audited against: [the site's primary conversion]

## Grade: [A–F] ([score]/100)
[one-line verdict, e.g. "Fair — a coherent palette undermined by a dated hero, a cluttered first screen, and 11 different button styles."]

### Scorecard
| # | Criterion | Pass/Partial/Fail | Weight | Points |
|---|-----------|-------------------|:------:|:------:|
| 1 | Visual hierarchy | Fail | 12 | 0 |
| ... | ... | ... | ... | ... |
| | **Total** | | **100** | **[score]** |

### Design tokens (measured — design-scan.py)
- **Typeface(s):** [e.g. Inter (body), Poppins (headings)]
- **Distinct font sizes:** [n]  ·  weights: [list]
- **Palette:** [n] text colours · [n] backgrounds — core: [top few hex/rgb]
- **Distinct button styles:** [n]  (fewer is more consistent)

## Findings
### DSN-01. [short title] — Impact [1–5] · Effort [1–5] · [quick win/big bet/fill-in/skip]
- **Issue:** [I — the measured number and/or the visual observation]
- **Impact:** [what it costs] [+ "expert judgement" note where it's a visual call]
- **Fix:** [F, concrete — the specific design change and target]
> [evidence — e.g. "design-scan: 11 button styles" / "design-desktop.png — glossy gradient hero"]

[... further findings, impact order ...]

## What's working
- [1–3 genuine strengths]

## Summary
- Findings: [n] ([x] quick wins, [y] big bets, ...)
- Design tokens (measured): [typeface(s) · N font sizes · N colours · N button styles]
- Visual read: [expert judgement — benchmarks §4 UI/UX; or "not assessed — no render/screenshot"]
- Top priority: [DSN-ID — one line]
```

### File 2: `design.html` (styled, share-ready)

A single **self-contained** `.html` file (all CSS inline in one `<style>` block, **no external assets and
no JavaScript**, except the two rendered screenshots referenced by relative `src`, which ship in the same
folder/ZIP). Use the **shared design system**: the exact `<style>` block and page frame from
[rules-messaging-clarity.md](../../../2%20Messaging%20Clarity/messaging-clarity/references/rules-messaging-clarity.md),
reproduced in full below so this skill is self-contained. Only these differ: the `<title>`, the header, the
`utm_content=design-visual` in the two brand links, and the section content.

Components:
- **A grade section first:** the letter grade in a `.grade` chip (class `a`/`b`/`c`/`d`/`f`), the score,
  a one-line verdict, and the **scorecard `<table>`** (criteria × pass/partial/fail × weight × points).
- **A "Design tokens (measured)" section:** the palette rendered as small inline **swatches** (inline
  styles), the **typeface(s)**, the **# of distinct font sizes**, and the **# of distinct button styles**.
- **A "Rendered screenshots" section:** the desktop and mobile full-page renders embedded as `<img>` in a
  flex row, each with its `<figcaption>` label **above** the image (caption first in the `<figure>`, then the
  `<img>`). Mid-session use the flat path `<img src="design-desktop.png">` (the PNG
  sits beside this file). In the **final bundle** the screenshots move to `assets/`, so the Action Report's
  regeneration repoints them to `assets/design-desktop.png` / `assets/design-mobile.png` (see
  [report-format.md](../../../report-format.md), "Deliverables bundle").
- **A Findings section:** one `.card` per finding. Card header: the `.id` chip (`DSN-01`), the short
  title, an **Impact meter** (`<span class="scorewrap"><span class="meter"><i style="width:NN%"></i></span><span class="scoreno">Impact X/5</span></span>`,
  width = Impact/5×100), and the **priority `.tag`** (`quickwin` / `bigbet` / `fillin` / `skip`). Body:
  Issue / Impact / Fix as `.row`s (append `· Effort X/5` in the Impact row via `<span class="effort">`),
  and the evidence in a `<blockquote>` (the measured number and/or the screenshot reference). Where a claim
  is a visual call, say **"expert judgement"** in the row.
- **A "What's working" section:** `.row`s or `ul.clean` of strengths.
- **A Summary section:** findings count, the measured tokens in one line, a "visual read" note, and the
  top priority (cited by ID).

**Navigation & hints (required):** cross-link other deliverables and tooltip every ID and shorthand term
(IIF, CRO, SEO, UX, **DSN**, CTA, MSG/CRO/SEO/UX/DSN, quadrant labels), every occurrence, per
[report-format.md](../../../report-format.md). **No `pagenav`** mid-session; end with the Print hint.

Design-tokens block pattern (inline swatches):
```html
<div class="row"><span class="k">Palette</span>
  <span style="display:inline-block;width:14px;height:14px;background:#0a2147;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #0a2147 &nbsp;
  <span style="display:inline-block;width:14px;height:14px;background:#d99a2b;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #d99a2b &nbsp;
  <span style="display:inline-block;width:14px;height:14px;background:#f5f5f7;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #f5f5f7
</div>
<div class="row"><span class="k">Typeface(s)</span>Inter (body) · Poppins (headings)</div>
<div class="row"><span class="k">Distinct font sizes</span>9</div>
<div class="row"><span class="k">Distinct button styles</span>11 <span class="effort">· fewer is more consistent</span></div>
```

Rendered-screenshots block pattern:
```html
<div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px">
  <figure style="margin:0;flex:1 1 380px">
    <figcaption class="verdict-common" style="margin-bottom:6px">Desktop (1440px)</figcaption>
    <img src="design-desktop.png" alt="Full-page desktop render" style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:2px">
  </figure>
  <figure style="margin:0;flex:0 1 220px">
    <figcaption class="verdict-common" style="margin-bottom:6px">Mobile (390px)</figcaption>
    <img src="design-mobile.png" alt="Full-page mobile render" style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:2px">
  </figure>
</div>
```

Finding card pattern:
```html
<article class="card">
  <h3><span class="id">DSN-01</span> 11 distinct button styles; no coherent design system
      <span class="scorewrap"><span class="meter"><i style="width:60%"></i></span><span class="scoreno">Impact 3/5</span></span>
      <span class="tag bigbet">big bet</span></h3>
  <div class="row"><span class="k">Issue</span>design-scan measured 11 distinct button styles; the screenshots confirm the hero, nav, and card buttons all look different.</div>
  <div class="row"><span class="k">Impact</span>An ad-hoc button set reads as unpolished and makes the primary action harder to spot. <span class="effort">· Effort 3/5</span></div>
  <div class="row"><span class="k">Fix</span>Collapse to two button styles — one primary, one secondary — with a shared radius, padding, and colour, applied site-wide.</div>
  <blockquote>design-scan: 11 distinct button styles; radii 0/4/8/24/999px</blockquote>
</article>
```

Full page (reproduce the shared `<style>` block verbatim; it is identical suite-wide):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Design &amp; Visual — [Site name]</title>
<style>
:root{--page:#f5f5f7;--paper:#ffffff;--ink:#111111;--soft:#5b5852;--line:#e2e2e7;
--brand:#d99a2b;--brand-deep:#946618;--band:#0b0b0a;--band-ink:#b8b2a4}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);
font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.brandband{background:var(--band)}
.bwrap{max-width:1060px;margin:0 auto;padding:16px 20px;
display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.brandlink{display:inline-flex;align-items:center;text-decoration:none;border-radius:4px;
cursor:pointer;transition:opacity .18s ease}
.brandlink:hover{opacity:.85}
.brandlink:focus-visible{outline:2px solid var(--brand);outline-offset:3px}
.brandlogo{display:block;height:44px;width:auto}
.pkgname{font-size:16px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
color:#fff;line-height:1.5;text-decoration:none;transition:opacity .18s ease}
.pkgname:hover{opacity:.85}
.pkgname:focus-visible{outline:2px solid var(--brand);outline-offset:3px}
.byline{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--band-ink);margin-right:9px;white-space:nowrap}
@media (max-width:560px){.brandlogo{height:34px}}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px 40px}
header.doc{margin:28px 0 6px;padding:22px 24px 20px;background:var(--paper);
border:1px solid var(--line);border-top:3px solid var(--brand);border-radius:2px}
header.doc h1{margin:0 0 6px;font-size:28px;line-height:1.25;font-weight:700;letter-spacing:-.01em}
header.doc .tagline{margin:0 0 14px;color:var(--soft);font-size:16px;font-style:italic}
header.doc .meta{color:var(--soft);font-size:14px}
header.doc .meta b{color:var(--ink);font-weight:600}
section.block{margin-top:36px}
h2.section{margin:0 0 14px;font-size:18px;font-weight:800;letter-spacing:-.01em;
display:flex;align-items:center;gap:12px}
h2.section .no{flex:none;width:28px;height:28px;display:inline-flex;align-items:center;
justify-content:center;background:var(--band);color:#fff;font-size:14px;font-weight:700;
border-radius:2px;font-variant-numeric:tabular-nums}
h2.section::after{content:"";flex:1;height:1px;background:var(--line)}
article.card,.card{background:var(--paper);border:1px solid var(--line);border-radius:2px;
padding:16px 20px;margin:10px 0}
.card h3{margin:0 0 12px;padding-bottom:11px;border-bottom:1px solid var(--line);
font-size:16px;font-weight:700;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.id{font-size:12px;font-weight:700;color:#43444a;background:#eef0f4;
border:1px solid #d8dae1;border-radius:2px;padding:3px 8px;letter-spacing:.03em}
.badge,.scoreno{font-size:14px;color:var(--soft);font-variant-numeric:tabular-nums}
.scorewrap{margin-left:auto;display:flex;align-items:center;gap:8px;white-space:nowrap}
.meter{width:64px;height:5px;background:var(--line);overflow:hidden}
.meter i{display:block;height:100%;background:var(--ink)}
.tag,.pill{font-size:12px;font-weight:650;border-radius:2px;padding:2.5px 8px;line-height:1.35}
.tag.quickwin{background:#ddefe1;color:#14603c}
.tag.bigbet{background:#dce4f5;color:#1c3f7c}
.tag.fillin{background:#f6e6b6;color:#6d5410}
.tag.skip{background:#ececec;color:#555}
.grade{font-size:13px;font-weight:800;border-radius:2px;padding:3px 10px;letter-spacing:.02em;font-variant-numeric:tabular-nums}
.grade.a{background:#ddefe1;color:#14603c}
.grade.b{background:#e4efd9;color:#3f6b1c}
.grade.c{background:#f6e6b6;color:#6d5410}
.grade.d{background:#f7ded0;color:#a5542e}
.grade.f{background:#f7dad4;color:#a53d2e}
.effort{font-size:13px;color:var(--soft);font-variant-numeric:tabular-nums}
.pill.covered{background:#ddefe1;color:#14603c}
.pill.gap{background:#f7e6e1;color:#a53d2e}
.verdict-common{color:var(--soft);font-size:13px}
.row{margin:4px 0;font-size:16px}
.row .k{font-weight:650;margin-right:2px}
blockquote{margin:12px 0 2px;padding:0 0 0 14px;border-left:2px solid var(--ink);
color:#494540;font-style:italic;font-size:16px}
.tablewrap{overflow-x:auto;background:var(--paper);border:1px solid var(--line);
border-radius:2px;padding:6px 20px 10px;margin-top:10px}
table{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
th{text-align:left;padding:10px 12px 8px 0;font-size:14px;font-weight:700;
border-bottom:2px solid var(--ink)}
td{text-align:left;padding:9px 12px 9px 0;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:none}
ul.clean{margin:6px 0;padding-left:18px}
a{color:var(--brand-deep)}
abbr[title],.term[title]{text-decoration:none;border-bottom:1px dotted #9a958c;cursor:help}
.matrix{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.quad{border:1px solid var(--line);border-radius:2px;padding:14px 16px;background:var(--paper)}
.quad h4{margin:0 0 8px;font-size:14px;font-weight:800;display:flex;align-items:center;gap:8px}
.quad .dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.quad.qw .dot{background:#14603c}.quad.bb .dot{background:#1c3f7c}
.quad.fi .dot{background:#b8912a}.quad.sk .dot{background:#999}
.quad ul{margin:0;padding-left:16px;font-size:14px}
.quad li{margin:3px 0}
.nextbtn{display:inline-block;margin:36px 0 8px;background:var(--band);color:#fff;
padding:12px 22px;border-radius:2px;text-decoration:none;font-weight:650}
.nextbtn:hover{color:var(--brand)}
.pagenav{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:36px 0 8px}
.pagenav .nextbtn,.pagenav .prevbtn{margin:0}
.pagenav .nextbtn{margin-left:auto}
.prevbtn{display:inline-block;background:var(--paper);color:var(--ink);border:1px solid var(--line);
padding:12px 22px;border-radius:2px;text-decoration:none;font-weight:650}
.prevbtn:hover{border-color:var(--brand);color:var(--brand-deep)}
.printhint{margin:22px 0 8px;font-size:13px;color:var(--soft);text-align:center}
.printhint kbd{font:inherit;background:#eef0f4;border:1px solid #d8dae1;border-bottom-width:2px;border-radius:3px;padding:1px 6px;font-weight:650}
.ctablock{background:var(--band);border-radius:2px;padding:36px 28px;text-align:center;margin-top:36px}
.ctablock .ctahead{font-size:22px;font-weight:800;letter-spacing:-.01em;margin:0 0 6px;color:#fff}
.ctablock .ctasub{color:var(--band-ink);font-size:15px;margin:0 0 18px}
.ctabtn{display:inline-block;background:var(--brand);color:#231a06;font-weight:700;
padding:12px 26px;border-radius:2px;text-decoration:none}
.ctabtn:hover{background:#e2a83d}
.openbtn{font-size:13px;font-weight:650;color:var(--ink);background:var(--paper);
border:1px solid var(--line);border-radius:2px;padding:5px 12px;text-decoration:none;white-space:nowrap}
.openbtn:hover{border-color:var(--brand);color:var(--brand-deep)}
h2.section .openbtn{order:3;margin-left:12px}
h2.section::after{order:2}
footer.doc{margin-top:40px;background:var(--band);color:var(--band-ink);font-size:12px}
.fwrap{max-width:1060px;margin:0 auto;padding:28px 20px 30px;text-align:center;
display:flex;flex-direction:column;align-items:center;gap:10px}
.footlogo{display:block;height:32px;width:auto}
.footmail{color:var(--brand);font-weight:600;text-decoration:none}
.footmail:hover{text-decoration:underline}
.footmail:focus-visible{outline:2px solid var(--brand);outline-offset:3px}
@media print{body{background:#fff}
article.card,.card,.tablewrap,.quad{border-color:#ccc}
header.doc{border-color:#ccc;border-top-color:var(--brand)}
.nextbtn,.openbtn,.prevbtn,.pagenav,.printhint{display:none}
.brandband,footer.doc,.ctablock,.tag,.pill,.grade,.meter i,.id,h2.section .no{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style>
</head>
<body>
<div class="brandband">
  <div class="bwrap">
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=design-visual" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=design-visual" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>Design &amp; Visual — [Site name]</h1>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit &nbsp;·&nbsp; <b>Grade:</b> [A–F] ([score]/100) &nbsp;·&nbsp; <b>Graded against:</b> benchmarks-2026.md (§4 UI/UX)</div>
  </header>

  <section class="block">
    <h2 class="section"><span class="no">1</span> Grade &amp; scorecard</h2>
    <div class="row"><span class="grade c">C</span> <b>72/100</b> — [one-line verdict]</div>
    <div class="tablewrap"><table>
      <tr><th>#</th><th>Criterion</th><th>Result</th><th>Weight</th><th>Points</th></tr>
      <tr><td>1</td><td>Visual hierarchy</td><td>Fail</td><td>12</td><td>0</td></tr>
      <!-- one row per criterion -->
      <tr><td></td><td><b>Total</b></td><td></td><td><b>100</b></td><td><b>72</b></td></tr>
    </table></div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">2</span> Design tokens (measured)</h2>
    <div class="row"><span class="k">Palette</span>
      <span style="display:inline-block;width:14px;height:14px;background:#0a2147;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #0a2147 &nbsp;
      <span style="display:inline-block;width:14px;height:14px;background:#d99a2b;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #d99a2b &nbsp;
      <span style="display:inline-block;width:14px;height:14px;background:#f5f5f7;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #f5f5f7
    </div>
    <div class="row"><span class="k">Typeface(s)</span>[e.g. Inter (body) · Poppins (headings)]</div>
    <div class="row"><span class="k">Distinct font sizes</span>[n]</div>
    <div class="row"><span class="k">Distinct button styles</span>[n] <span class="effort">· fewer is more consistent</span></div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">3</span> Rendered screenshots</h2>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px">
      <figure style="margin:0;flex:1 1 380px">
        <figcaption class="verdict-common" style="margin-bottom:6px">Desktop (1440px)</figcaption>
        <img src="design-desktop.png" alt="Full-page desktop render" style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:2px">
      </figure>
      <figure style="margin:0;flex:0 1 220px">
        <figcaption class="verdict-common" style="margin-bottom:6px">Mobile (390px)</figcaption>
        <img src="design-mobile.png" alt="Full-page mobile render" style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:2px">
      </figure>
    </div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">4</span> Findings</h2>
    <!-- one .card per finding (see the finding card pattern above) -->
  </section>

  <section class="block">
    <h2 class="section"><span class="no">5</span> What's working</h2>
    <ul class="clean"><li>[genuine strength]</li></ul>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">6</span> Summary</h2>
    <div class="row"><span class="k">Findings</span>[n] ([x] quick wins, [y] big bets, …)</div>
    <div class="row"><span class="k">Design tokens (measured)</span>[typeface(s)] · [N] font sizes · [N] colours · [N] button styles</div>
    <div class="row"><span class="k">Visual read</span>expert judgement — benchmarks §4 UI/UX [or "not assessed — no render/screenshot"]</div>
    <div class="row"><span class="k">Top priority</span>[DSN-ID — one line]</div>
  </section>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=design-visual" target="_blank" rel="noopener">
      <img class="footlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
    <a class="footmail" href="mailto:juicy@ananas-agency.com">juicy@ananas-agency.com</a>
    <div>© 2026 Ananas-Agency — generated [date]. MIT License.</div>
  </div>
</footer>
</body>
</html>
```

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
