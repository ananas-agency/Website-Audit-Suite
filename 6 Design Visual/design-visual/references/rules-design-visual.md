# Design & Visual Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
adds the design-specific fast tests, the design scan, the scoring rubric, and worked finding examples.

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

**Run it** (needs Playwright: the install commands the setup check prints; it bundles its own Chromium, no browser to install):
```
python scripts/design-scan.py <URL> --pages <one-article,one-service-page,one-case-study> --out "audit-<slug>"
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

**DSN-04 — Low-quality generic stock imagery** · Impact 3 · Effort 2 · **quick win**
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

## Output
Write the results to the run folder as described in [audit-data-format.md](../../../audit-data-format.md),
section "Dimension files", then build the page.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
