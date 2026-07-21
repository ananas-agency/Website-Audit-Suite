---
name: ux-technical
description: >
  Analyses a website's user experience and technical health in the Ananas-Agency Website Audit Suite.
  Fetches the homepage and key pages and inspects the things you can actually verify from the
  markup and what renders — navigation and information architecture, visual hierarchy and
  readability, mobile-friendliness (measured by rendering the page at phone widths — does it fit the
  screen, are elements or images too big, are tap targets and text large enough), page-speed signals
  (oversized images, render-blocking scripts), accessibility (alt text, form labels, contrast, heading order,
  lang attribute), broken links and errors, HTTPS and security basics, forms usability, UI
  consistency, and layout/whitespace. Produces graded findings in Issue · Impact · Fix format on an
  Impact × Effort priority scale, plus a 0–100 UX & Technical grade. Use this skill when the user
  wants to: check if their site is usable and mobile-friendly, find broken links or technical
  problems, review accessibility, or understand why the site feels clunky, slow, or hard to use.
  Trigger: "UX audit", "is my site mobile-friendly", "site speed", "page speed", "accessibility",
  "usability review", "broken links", "my navigation", "technical audit", "is my site accessible",
  "why is my site slow".
---

# UX & Technical (Ananas-Agency — Website Audit)

## Goal

Judge how **usable and technically sound** the website is (can visitors find their way, read the
page, use it on a phone, trust it, and complete a form without friction), and turn every weakness
into a prioritised, fixable **Finding**. Deliver a graded UX & Technical scorecard (0–100 → letter
grade) and a list of `UX-` findings in **Issue · Impact · Fix** format, each rated on Impact and
Effort so the user knows what to fix first.

This is **URL-first**: inspect the live pages and quote what's actually in the markup and on screen.
Written for **business owners and marketers**: plain language, and every piece of jargon explained
(viewport, alt text, contrast ratio, render-blocking, Core Web Vitals) with each finding tied to a
real effect on their visitors.

## Inputs

- **Site Snapshot** (from Skill 0). Paste it if you have it; it anchors the analysis to the site's
  **primary conversion goal**, audience, page inventory, and the observable platform/HTTPS signals
  already captured. If it's missing, do a quick mini-snapshot first (fetch the homepage; establish
  name, what it does, primary goal, key pages, HTTPS) so your findings have an anchor, but don't run
  the full intake.
- **The URL(s)**: the homepage plus any key pages the user cares about (a product/pricing page, the
  contact/booking page with the main form, a deep content page).

## The core unit: a Finding (Issue · Impact · Fix)

Every observation is a Finding. See [report-format.md](../../report-format.md) for the full definition,
the Impact/Effort scales (1–5), and the priority quadrants (quick win / big bet / fill-in / skip). In
short:
- **Issue**: the specific usability or technical problem, with the **actual element, attribute, or
  page quoted** as evidence (the missing viewport tag, the unlabeled input, the 404 link).
- **Impact**: what it costs (visitors can't navigate, bounce on mobile, can't submit the form, lose
  trust). Rated **Impact 1–5**.
- **Fix**: the concrete change, ideally with the exact markup or attribute to add.
- **Effort 1–5** and a **priority quadrant** derived from Impact × Effort.

Give each finding an ID: `UX-01`, `UX-02`, … in impact order.

## Conversation flow

### Step 1: Load context and fetch the pages

Take the Site Snapshot (or build the mini one) and **fetch the homepage and key pages**. Read the
markup, not just the rendered text: the `<head>` (viewport meta, `<html lang>`, HTTPS on asset URLs),
the navigation, the heading order (`<h1>`…`<h6>`), image `alt` attributes, form `<label>`s and input
types, link `href`s, and the weight/dimensions of hero images. Keep the site's **primary goal** in
mind. Usability is always "usable *toward completing that action*".

### Step 2: Run the UX/technical fast tests

Apply the fast diagnostic tests before the full rubric. Details and examples in
[references/rules-ux-technical.md](references/rules-ux-technical.md):
- **The three-click test**: can a visitor reach any key page (product, pricing, contact) in about
  three clicks from the homepage, or do they hit dead ends?
- **The squint test**: blur or squint at the page: does the visual hierarchy pull the eye to the one
  main action, or does everything shout equally (or nothing stands out)?
- **The mobile-viewport test**: is there a `<meta name="viewport">` tag, and (confirmed by the
  measured render in Step 2b) do the text size and tap targets survive a narrow phone-width screen
  without a horizontal scrollbar?

### Step 2b: Measure mobile-friendliness (headless render — the correct way)

Don't guess mobile behaviour from the markup; **render the page and measure it**. If Playwright is
available (`pip install playwright && playwright install chromium`, which bundles its own Chromium,
cross-platform), run the bundled tool:

```
python scripts/mobile-audit.py <URL> --out <folder> --widths 320,390,414
```

It renders the page with real mobile emulation at each phone width and reports, per width
(full detail and thresholds in [references/rules-ux-technical.md](references/rules-ux-technical.md),
"Measured mobile-friendliness test"):
- **Fits the screen?** Document scroll width vs viewport width (any horizontal scroll = fail).
- **Elements too big**: every element whose box extends past the screen edge (real overflow), kept
  separate from content merely clipped inside a carousel/`overflow` container.
- **Images wider than the screen.**
- **Tap targets under 44×44px**: buttons/links too small to tap reliably (Apple HIG / WCAG 2.5.5).
- **Text under 12px**: too small to read on a phone.
- A **full-page screenshot per width**: open them and eyeball the layout for anything the numbers miss.

Turn each measured problem into a `UX-` finding with the real numbers as evidence (e.g. "44 tap
targets below 44×44px at 390px: pagination, language switch, carousel controls"). If **no headless
browser is available** (Basic layer), say so and fall back to marking these "not measured", then describe the
observable signals but never assume the result.

### Step 2c: Measure performance, accessibility & security (headless — the correct way)

Don't guess "is it fast?", "is it accessible?", or "is it secure?"; **measure them**. If Playwright is available (bundled Chromium, cross-platform),
run the bundled scanner:

```
python scripts/perf-a11y-scan.py <URL> --out <folder>
```

It renders the page (mobile-emulated, as Google measures) and returns, all locally with no API keys:
**lab Core Web Vitals** (LCP, CLS, FCP, TTFB) **+ a lab INP proxy (Total Blocking Time)**, page weight + the
heaviest resources; **real WCAG violations** via **axe-core** (critical / serious / moderate / minor) **plus a
keyboard focus-order pass**; and a **security** read (HTTPS, TLS version, HSTS/CSP & security headers present
vs. missing, redirect chain, mixed content). Thresholds and full method:
[references/rules-ux-technical.md](references/rules-ux-technical.md), "Measured performance, accessibility & security".
Turn each into a `UX-` finding with the numbers as evidence. **Honesty:** this is a **lab** run. The INP
figure is the standard lab proxy (TBT), not the real-world field percentile; and full **screen-reader**
testing is manual and out of scope. Say so. If the scanner can't run (Basic layer), fall back to "not measured".

### Step 3: Work the rubric and generate findings

Go through the UX & Technical rubric criteria (see the reference, "Scoring rubric"): navigation & IA,
visual hierarchy & readability, mobile responsiveness, page-speed signals, accessibility, links &
errors, security & trust basics, forms usability, UI consistency, layout & whitespace, responsive
robustness. For each weakness, write a Finding (IIF) with quoted evidence, an Impact and Effort
rating, and a quadrant. **Also note genuine strengths**, so the report isn't only problems.

**Readability of the content templates is measured.** The Design & Visual scan (`design-scan.py --pages`)
renders representative interior templates (an article, a service page, a case study) and measures each one's
**body text-alignment** and **characters-per-line**. Use `design-pages.json` for the readability criterion:
centred body copy, or lines well outside ~45-75 characters, on an article or service template is a real
`UX-` readability finding even when the homepage reads fine. Cite the measured value.

### Step 4: Score the dimension

Rate each rubric criterion Pass / Partial / Fail. **Each criterion's "Pass" is the 2026 standard from
[benchmarks-2026.md](../../benchmarks-2026.md)** (Core Web Vitals ≤ 2.5s/200ms/0.1, tap targets ≥ 44px,
WCAG 2.2 AA, HTTPS + HSTS, and the **UI/UX & usability** bars: Nielsen's heuristics, clear IA in ~1–3
clicks, one focal point, ≥ 16px / 45–75-char / 1.5 text, consistency, visible feedback under 1s), so cite
the benchmark in findings. Apply the weights, and total to a **0–100 score**;
map to a **letter grade** (A–F, bands in [report-format.md](../../report-format.md)). Show the criteria
table so the grade is explainable. State plainly that the grade is an **expert judgement**, informed by the
measured numbers where the bundled tools ran (speed, mobile fit, accessibility, security, links), and by
observable markup signals where they didn't (Basic layer).

### Step 5: Deliver the files

Generate `ux-technical.md` and a styled, self-contained `ux-technical.html` and share them. Format,
the finding card component, and the scorecard layout: see the reference, "Output file format". End
the HTML with the Print hint; **no `pagenav`** mid-session.

### Step 6: Add to the Website Audit Report & hand off

Record the **UX & Technical** section (grade + criteria + findings) into the internal running
**Website Audit Report** (do not create/show a report file now; that's the Action Report skill's job
at the end). Format and section order: [report-format.md](../../report-format.md). Tell the user the
remaining analyses are any of **Messaging & Clarity**, **Conversion (CRO)**, or **SEO & Content**, and
that **Action Report** ties them together at the end.

## Critical rules

1. **Evidence, always.** Every finding quotes the actual element, attribute, or page: the missing
   `<meta name="viewport">`, the `<img>` with no `alt`, the link returning 404. No vague "the UX
   could be better".
2. **Measure what you can; be honest about the rest.** With a headless browser, these are now
   **measured, not guessed**, all locally with no API keys: **mobile-friendliness** (`mobile-audit.py`,
   Step 2b); **lab Core Web Vitals + a lab INP proxy (TBT) + page weight**, **WCAG violations via axe-core
   + a keyboard focus pass**, and **security** (HTTPS/TLS/headers/redirects/mixed content)
   (`perf-a11y-scan.py`, Step 2c); and **broken-link HTTP status** across the key pages
   (`interaction-scan.py`). Base those findings on the real numbers and quote them. The only thing a local
   run genuinely can't produce is the real-world **field percentile** (LCP/INP/CLS across many real users).
   Measure the lab equivalents and don't claim a field number; full **screen-reader** testing stays
   manual and out of scope. Never invent a load time, a CWV score, or a violation you didn't measure. In the
   **Basic layer** (no browser), these fall back to "not measured"; describe observable signals, don't name
   a third-party tool.
3. **Anchor to the primary goal.** Judge usability toward the site's one main conversion; friction
   on the path to the main action outranks cosmetic issues.
4. **Fixes are concrete.** Give the exact attribute, tag, or change (e.g. "add
   `<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">` to the `<head>`"), not
   "make it responsive".
5. **Impact + Effort on every finding.** So the Action Report can place it on the matrix.
6. **Don't invent.** Judge only what you can observe. If a page couldn't be read or rendered, say so
   and ask for the markup/screenshot; never assume behaviour you didn't see.
7. **Name strengths too.** Note what already works, so the grade and the report are balanced and
   credible.
8. **Plain language.** Business owners are the audience; explain every technical term the first time
   (viewport = the visible screen area; alt text = the text description of an image; contrast ratio =
   how readable text is against its background; render-blocking = scripts that delay the page
   appearing; Core Web Vitals = Google's set of real-world speed/stability scores).


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
