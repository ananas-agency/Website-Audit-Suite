---
name: design-visual
description: >
  Assesses a website's rendered visual design in the Ananas-Agency Website Audit Suite. Renders the
  homepage in headless Chrome (via the bundled design-scan.py) to MEASURE the real design tokens — the
  colour palette, the typefaces, the count of distinct font sizes, and the count of distinct button
  styles (a design-system coherence signal) — then actually LOOKS at full-page desktop and mobile
  screenshots to judge what a static-HTML read never can: visual hierarchy, whitespace, typography,
  imagery, modern-vs-dated, colour harmony, brand coherence, and trust/polish. Produces graded findings
  in Issue · Impact · Fix format on an Impact × Effort priority scale, plus a 0–100 Design & Visual
  grade. Use this skill when the user wants to: see how their site looks, know if the design is modern
  and professional, judge visual hierarchy and imagery, or check design-system and brand consistency.
  Trigger: "design review", "how does my website look", "is my design modern", "visual design audit",
  "my site looks dated", "brand consistency", "review my homepage design", "does my site look
  professional".
---

# Design & Visual (Ananas-Agency — Website Audit)

## Goal

Judge how the website **actually looks** (whether the rendered design leads the eye to the main action,
feels coherent and current, and reads as professional and trustworthy), and turn every weakness into a
prioritised, fixable **Finding**. Deliver a graded Design & Visual scorecard (0–100 → letter grade) and a
list of `DSN-` findings in **Issue · Impact · Fix** format, each rated on Impact and Effort so the user
knows what to fix first.

This is the one dimension a **static-HTML read can't do**: you have to see the page. So it works from two
inputs: the **measured design tokens** (objective counts, from the bundled `scripts/design-scan.py`) and a
**visual read** of the rendered desktop + mobile screenshots (expert judgement). Written for **business
owners and marketers**: plain language, no unexplained jargon, and every finding tied to a real effect on
their visitors.

## Inputs

- **Site Snapshot** (from Skill 0). Paste it if you have it; it anchors the analysis to the site's
  **primary conversion goal** and audience. If it's missing, do a quick mini-snapshot first (fetch the
  homepage; establish name, what it does, primary goal, audience) so your findings have an anchor, but
  don't run the full intake.
- **The URL**: the homepage (the main page gets the full visual audit); optionally a key landing/product
  page the user cares about.
- **Brand guidelines** (optional): the company's real colours, fonts, and logo. **Needed for a true
  "off-brand" call.** Without them, judge general design quality and internal consistency only, and ask
  the user for their brand guidelines if they want brand-*fit* assessed (see Critical rules).

## The core unit: a Finding (Issue · Impact · Fix)

Every observation is a Finding. See [report-format.md](../../report-format.md) for the full definition,
the Impact/Effort scales (1–5), and the priority quadrants (quick win / big bet / fill-in / skip). In
short:
- **Issue**: the specific design problem, with **evidence**: a measured token ("design-scan: 11 distinct
  button styles") and/or the visual observation ("the hero uses a 2012-era glossy gradient and a drop
  shadow on every card").
- **Impact**: what it costs (visitors don't know where to look, the site reads as dated or amateur, trust
  erodes via the aesthetic-usability effect). Rated **Impact 1–5**.
- **Fix**: the concrete design change, ideally with the target ("collapse to two button styles, one
  primary, one secondary").
- **Effort 1–5** and a **priority quadrant** derived from Impact × Effort.

Give each finding an ID: `DSN-01`, `DSN-02`, … in impact order.

## Conversation flow

### Step 1: Load context and identify the page

Take the Site Snapshot (or build the mini one) and confirm the URL to render (the homepage, plus any key
page the user names). Keep the site's **primary goal** and **audience** in mind. Good design is design
that leads the eye *toward the main action* and fits *who the site is for*.

### Step 2: Run the design scan (headless render — the correct way)

Don't guess how the page looks from the markup; **render it and measure it**. If Playwright is available
(`pip install playwright && playwright install chromium`, which bundles its own Chromium, cross-platform), run the bundled tool:

```
python scripts/design-scan.py <URL> --pages <one-article,one-service-page,one-case-study> --out <folder>
```

Pass `--pages` with **one representative page per key interior template**: an **article/blog post**, a
**service/offering page**, and a **case study** (pick them from the Snapshot's page inventory or the SEO
sweep's page types). A site's biggest design and readability problems usually live on these template pages,
not the homepage, so the tool renders each one, **screenshots it** (`page-<slug>.png`), compares tokens for
**cross-page consistency** (same typeface/palette/button system, or drift?), and **measures readability** per
page: body **text-alignment**, approximate **characters-per-line** (the 45-75 target), and **words-per-visual**
(a wall-of-text signal). This is what lets you judge the interior templates, not just the homepage.

It renders in headless Chrome at desktop (1440px) and mobile (390px) and produces (full detail and thresholds
in [references/rules-design-visual.md](references/rules-design-visual.md), "The design scan"):
- **`design-tokens.json` / `design-scan.md`**: the MEASURED tokens: the **typeface(s)**, the **count of
  distinct font sizes** (and weights), the **colour palette** (distinct text colours + backgrounds), and the
  **count of distinct BUTTON STYLES** (a coherence signal, fewer is more consistent). These counts are objective.
- **`design-desktop.png`** and **`design-mobile.png`**: full-page homepage screenshots for the visual read.
- With `--pages`: **`page-<slug>.png`** per interior template, plus `design-pages.json` with the cross-page
  token consistency and the **per-page readability** (alignment, chars-per-line, words-per-visual).

### Step 2b: Do the visual read — actually LOOK at the screenshots

Open `design-desktop.png` and `design-mobile.png` and **look at them**. This is the expert-judgement half:
grounded in the **benchmarks-2026.md §4 UI/UX principles** (Nielsen's heuristics, visual hierarchy,
consistency/Jakob's Law, aesthetic-usability, Stanford Web Credibility), judge visual hierarchy, whitespace,
typography, imagery quality, modern-vs-dated, colour harmony, brand coherence, and the trust/polish the
design conveys, on both desktop and the phone. Cross-reference the measured tokens (e.g. a "cluttered,
no focal point" observation next to "design-scan: 9 distinct font sizes, 11 button styles"). Run the three
fast tests first (Step 3).

**If no headless browser is available**, say so and fall back to a **user-provided screenshot** of the page.
If none is available either, mark the visual read **"not assessed"** and ask for a screenshot; never invent
what the page looks like. The measured token counts also require the render, so without either they're
unavailable too.

### Step 2c: Read the interior templates (not just the homepage)

Open each `page-<slug>.png` from the `--pages` render and read the interior templates the way you read the
homepage. This is where the biggest design problems on real sites hide. For each template, judge:
- **Layout & structure:** is the page designed (sections, cards, a clear structure), or is it a long
  undifferentiated column that reads like a pasted document?
- **Text density & visual variety:** does it mix text with graphics, diagrams, and varied section layouts,
  or is it a wall of text? The measured **words-per-visual** is the signal (a service or article page with
  hundreds of words and almost no visuals is text-heavy). This is the common offering-page failure.
- **What the page delivers:** a service/offering page should look like it answers *"what the client gets"*,
  not read like an essay on the technology or the process.
- **Readability (measured):** cross-check the numbers. **Centred body text**, or **chars-per-line well
  outside 45-75** (benchmarks-2026.md §4), makes a page hard to read regardless of how it looks. Quote the
  measured value in the finding.

Turn each template-level problem into a `DSN-` finding with the screenshot and the measured readability
value as evidence (e.g. *"the article template centres its body text at ~120 chars/line, which is hard to
read"*, or *"the service page is a wall of text: ~140 words per visual, no diagrams or section variety"*).
These are page-**template** findings, so one finding per template pattern, not one per page. If a readability
problem is really about legibility and line length, note that **UX & Technical** covers it too and align the
two.

### Step 3: Run the design fast tests

Apply the fast diagnostic tests before the full rubric. Details and examples in
[references/rules-design-visual.md](references/rules-design-visual.md):
- **The squint test**: blur the page (or squint): does **one clear focal point** emerge and lead the eye
  to the primary action, and is the layout balanced, or does everything compete (or nothing stands out)?
- **The 5-second impression**: glance for five seconds: does it look **modern, professional and
  trustworthy**, or dated, generic, or amateur?
- **The consistency count**: from the scan, how many **button styles / font sizes / colours**? A tight
  set signals a coherent design system; a sprawling one signals an ad-hoc, inconsistent build.

### Step 4: Work the rubric and generate findings

Go through the Design & Visual rubric criteria (see the reference, "Scoring rubric"): visual hierarchy,
design-system consistency, typography, colour & palette, layout/grid/alignment, whitespace & density,
imagery & media quality, modern-vs-dated, brand coherence & credibility, and mobile visual quality. For
each weakness, write a Finding (IIF): **cite the measured number as evidence where it applies AND the
visual observation**, with an Impact and Effort rating and a quadrant. **Also note genuine strengths**, so
the report isn't only problems.

### Step 5: Score the dimension

Rate each rubric criterion Pass / Partial / Fail. **Each criterion's "Pass" is the 2026 standard from
[benchmarks-2026.md](../../benchmarks-2026.md)** (§4 UI/UX & usability: one focal point, visual hierarchy,
consistency/Jakob's Law, ≥16px / 45–75-char / 1.5 readable type, aesthetic-minimalist design, and the
aesthetic-usability effect on trust), so cite the benchmark in findings. Apply the weights, and total to a
**0–100 score**; map to a **letter grade** (A–F, bands in [report-format.md](../../report-format.md)). Show the
criteria table so the grade is explainable. State plainly that the **token counts are measured** but the
**visual judgement is expert-subjective**, grounded in the §4 UI/UX principles, not a lab metric.

### Step 6: Deliver the files

Generate `design.md` and a styled, self-contained `design.html` (embedding the two rendered screenshots and
the measured tokens) and share them. Format, the finding card component, the design-tokens block, and the
scorecard layout: see the reference, "Output file format". End the HTML with the Print hint; **no
`pagenav`** mid-session.

### Step 7: Add to the Website Audit Report & hand off

Record the **Design & Visual** section (grade + criteria + findings) into the internal running **Website
Audit Report** (do not create/show a report file now; that's the Action Report skill's job at the end).
Format and section order: [report-format.md](../../report-format.md). Tell the user the remaining analyses are
any of **Messaging & Clarity**, **Conversion (CRO)**, **SEO & Content**, or **UX & Technical**, and that
**Action Report** ties them together at the end.

## Critical rules

1. **Measured vs. expert-subjective: say which is which.** The design-token **counts** (button styles,
   font sizes, colours, typefaces) are **objective and measured** by `design-scan.py`. The **visual
   judgement** (hierarchy, whitespace, modern-vs-dated, imagery, polish) is **expert-subjective**,
   grounded in the **benchmarks-2026.md §4 UI/UX** principles (Nielsen's heuristics, visual hierarchy,
   consistency, aesthetic-usability), **not a lab metric**. Label it as expert judgement; never dress an
   opinion up as a measurement.
2. **A true "off-brand" call needs brand guidelines.** Judging that a design is *off-brand* requires the
   company's real **colours, fonts, and logo**. Without them, judge **general design quality + internal
   consistency** only (does it hold together with itself?), and **ask the user for brand guidelines** if
   they want brand-fit assessed. Never assert a colour or font is "wrong for the brand" with no reference.
3. **Look, don't guess.** Base the visual read on the **rendered screenshots** (or a user-supplied one).
   If no headless browser and no screenshot are available, mark the visual read **"not assessed"** and ask
   for one; **never invent what the page looks like**.
4. **Evidence, always: the number and the eye.** Every finding cites the measured token where relevant
   ("design-scan: 11 button styles") **and/or** the concrete visual observation ("the hero is a glossy
   2012-era gradient"). No vague "the design could be better".
5. **Anchor to the primary goal and audience.** Judge the design toward the site's one main conversion and
   who it's for: a focal point that leads to the main action, and an aesthetic that fits the audience.
6. **Fixes are concrete.** Give the specific change and target (e.g. "collapse to two button styles",
   "cut to one display + one body typeface", "replace the generic stock photo with a real product shot"),
   not "make it look nicer".
7. **Impact + Effort on every finding.** So the Action Report can place it on the matrix.
8. **Name strengths too.** Note what already works visually, so the grade and the report are balanced and
   credible.
9. **Plain language.** Business owners are the audience; explain any shorthand (visual hierarchy = what the
   eye is led to first; design system = a consistent set of colours/type/buttons; focal point = the one
   thing that stands out; whitespace = the empty breathing room around elements).


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
