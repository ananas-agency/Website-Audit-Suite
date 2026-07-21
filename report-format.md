# Website Audit Report — shared format, scoring & assembly

This is the single shared spec every skill in the **Website Audit Suite** points to. It defines:

1. the **Finding** format every analysis skill uses (Issue · Impact · Fix),
2. the **Impact × Effort** priority model and the **letter-grade scorecard**,
3. the **ID scheme** for findings,
4. how the **Website Audit Report** (the consolidated dossier) accretes across the session,
5. the **cross-linking / navigation** rules for every generated `.html`,
6. the final **bundle**.

The **standard the audit grades against** — what a website is expected to be, with concrete, sourced
thresholds — lives in [benchmarks-2026.md](benchmarks-2026.md). Every rubric "Pass" and every "the
standard is X, you're at Y" finding traces back to it; the Action Report renders a **"2026 standard vs
your site"** scorecard from it.

If a rule about findings, scoring, grades, matrix, cross-linking, or the bundle is needed anywhere,
it lives here — the skills reference this file instead of re-stating it.

## Audit depth (two-tier)

The suite spends effort where it matters:

- **The homepage is the main page — it gets the full, in-depth audit** across all five dimensions
  (Messaging, Conversion, SEO, UX/Technical, Design & Visual), including the **measured mobile-friendliness render**
  (UX & Technical) at phone widths.
- **Secondary pages** (services, products, case studies, articles, about, contact) get **targeted
  multi-page checks** — broad coverage without a full audit of every page:
  - **SEO** — a site-wide static sweep (`seo-sweep.py`): titles, metas, H1s, canonicals, indexability,
    word count, alt, schema across a sample (~5 per type).
  - **Messaging** — a cross-page clarity/consistency read of the key pages (H1, CTA, hero) — reusing the
    sweep + interaction data.
  - **Design** — a cross-page token comparison (`design-scan.py --pages`): same typeface/palette/button
    system across pages, or drift?
  - **Conversion** — a multi-page interaction pass (`interaction-scan.py`): CTA reachability + form
    validation on the homepage, contact, and a top page (never submitting).
  This keeps coverage broad and token/time cost low. The user can widen or narrow it (`--per-type`,
  `--pages`, or naming specific pages).

The fetching, rendering, and sweeping run as **tools** (headless-browser render, static crawl) that
return compact summaries — they cost local compute, not model tokens; only the summaries enter the audit.

## Basic & Extended layers (both free)

Every skill runs in one of two layers, decided by the environment — **not** by payment (both are free):

- **Basic layer** — Claude reads the live page(s) and reasons. Produces the full graded audit from what's
  observable in the source + expert judgement. Works in the Claude web app, Desktop, or Claude Code — no
  install. This is the default.
- **Extended layer** — the bundled tools additionally **render/measure** the page (Playwright + Chromium;
  `pip install playwright && playwright install chromium`). Adds the hard numbers a static read can't
  produce.

**How each skill behaves:** every measured step already says *"if the bundled tool can run, measure it;
otherwise mark it 'not measured' (Basic layer) and describe the observable signals."* That fallback **is**
the layer switch — the same skill file produces a Basic report where the tool can't run and an Extended
report where it can. The bundled tools need no API keys; they never point the reader at a third-party
service.

**The `measured` tag.** When a finding is backed by a tool render (Core Web Vitals, axe accessibility,
mobile fit/tap-targets, design tokens, tracking/consent, interaction), mark it in the deliverable with a
small **`measured`** chip:
`<span class="chip-measured" style="font-size:11px;font-weight:650;border-radius:2px;padding:2px 7px;background:#dce4f5;color:#1c3f7c;letter-spacing:.02em">measured</span>`
(rendered inline in the finding-card header, after the priority tag). Findings that are reasoning-only
(Basic) carry no chip. In a Basic report, the Extended-only checks are listed as **"not measured —
available with the Extended layer,"** so the reader sees exactly what an Extended run would add.

**Run-mode line.** Note the layer in the report header meta of the consolidated report and Action Report,
e.g. `Run mode: Extended (measured tools ran)` or `Run mode: Basic (reasoning only)`.

---

## The Finding format (Issue · Impact · Fix)

Every observation any analysis skill makes is a **Finding** — the core unit of this suite (its
equivalent of a value proposition). A finding is a triple plus two ratings:

- **I — Issue.** The concrete, specific problem observed on the page, with **evidence**: quote the
  actual copy, name the element, or give the page/location. Not "the messaging is weak" but
  "the homepage H1 reads 'Welcome to our website', which says nothing about what you do or for whom."
- **I — Impact.** What the issue **costs the business** — lost conversions, an unclear message,
  missed search traffic, added friction, eroded trust. Rated **Impact 1–5** (see below).
- **F — Fix.** The specific, actionable recommendation — what to change and, where useful, to what.
  Not "improve the headline" but "replace with a benefit-led H1, e.g. 'Bookkeeping for tradespeople —
  sorted in an hour a week'."

Plus:

- **Effort 1–5** — how hard the fix is to implement (see below).
- **Priority** — derived from Impact × Effort (the quadrant, below).

### Impact scale (1–5)
| Score | Meaning |
|-------|---------|
| 5 | Critical — directly blocks or badly leaks the primary conversion; affects every visitor. |
| 4 | High — materially hurts conversions, clarity, trust, or search visibility. |
| 3 | Moderate — a real problem for a meaningful share of visitors. |
| 2 | Minor — small friction or polish; limited reach. |
| 1 | Cosmetic — nice to fix, negligible business effect. |

### Effort scale (1–5)
| Score | Meaning |
|-------|---------|
| 1 | Trivial — a copy/setting change, minutes (edit a headline, add alt text). |
| 2 | Easy — an hour or two, no specialist (rewrite a section, add a meta description). |
| 3 | Moderate — half a day to a day, may need a designer/developer. |
| 4 | Hard — multi-day; new page, redesign of a flow, template change. |
| 5 | Major — a project; re-platforming, full IA rework, performance overhaul. |

### Priority quadrants (Impact × Effort)
Split each axis at its midpoint: **Impact High = 4–5, Low = 1–3**; **Effort Low = 1–2, High = 3–5.**

| | Low effort (1–2) | High effort (3–5) |
|---|---|---|
| **High impact (4–5)** | **Quick Win** — do first | **Big Bet** — plan & schedule |
| **Low impact (1–3)** | **Fill-in** — do when convenient | **Skip** — backlog / don't bother |

Within a quadrant, rank by Impact descending, then Effort ascending. Every finding carries exactly
one quadrant label: `quickwin`, `bigbet`, `fillin`, or `skip`.

> **Honesty rule (applies to every skill).** Report only what you can actually verify — from the page you
> fetched (its copy, HTML, headings, meta tags, alt text, links, structure), from what renders, and from the
> bundled measurement tools (which run locally, no API keys). Page-load time, Core Web Vitals, INP (lab
> proxy), accessibility, security, mobile fit, design tokens, links and structured data are **measured** when
> the tools can run; in the **Basic layer** (no browser) mark them **"not measured"** and describe the
> observable signals — don't point at a third-party service. Metrics only the owner's analytics can show —
> conversion rates, traffic, rankings, index status — are **owner-reported** (from Goals & Discovery) or left
> out, never invented or estimated. A grade is an expert judgement, not a lab measurement — label it as such.

---

## The scorecard (letter grade per dimension)

Each analysis skill (Messaging, Conversion, SEO, UX/Technical, Design & Visual) ends by scoring its dimension **0–100**
and mapping it to a **letter grade**. The score is rubric-based and transparent: each skill's reference
lists ~8–12 weighted **criteria**; rate each **Pass** (full weight), **Partial** (half), or **Fail**
(zero), sum the weights, and normalise to 0–100. Always show the reader the criteria table so the grade
is explainable, not a black box.

**Each criterion's "Pass" is the 2026 standard**, not a subjective preference — the thresholds come from
[benchmarks-2026.md](benchmarks-2026.md) (Core Web Vitals ≤ 2.5s/200ms/0.1, tap targets ≥ 44px, WCAG 2.2
AA, 50–60-char unique titles, and so on). Where a finding states a gap, cite the benchmark: "the standard
is X, this site is at Y." That's what makes the audit a concrete update plan rather than an opinion.

| Grade | Score | Read as |
|-------|-------|---------|
| **A** | 90–100 | Excellent — strong, few issues. |
| **B** | 80–89 | Good — solid with clear improvements available. |
| **C** | 70–79 | Fair — works, but leaving results on the table. |
| **D** | 60–69 | Weak — real problems hurting performance. |
| **F** | 0–59 | Poor — urgent work needed. |

The **overall site grade** (produced by the Action Report) is the average of the completed dimension
scores, mapped to the same bands. If a dimension wasn't run, say so and average only what exists.

---

## Finding ID scheme

Findings get stable IDs, prefixed by dimension, numbered within the dimension in the order they appear
(strongest impact first):

- `MSG-` — Messaging & Clarity
- `CRO-` — Conversion (CRO)
- `SEO-` — SEO & Content
- `UX-`  — UX & Technical
- `DSN-` — Design & Visual

e.g. `MSG-01`, `CRO-03`, `SEO-07`, `UX-02`. IDs are cited (with a tooltip) everywhere a finding is
referenced outside its own list — especially in the Action Report roadmap and the dossier.

---

## The Website Audit Report (consolidated dossier) — how it accretes

The **Website Audit Report** is the single consolidated document that accretes as you move through the
skills in one continuous session. Each analysis skill records its own section as it completes; the
final skill (**Action Report**) generates the executive summary + priority plan at the top and delivers
the whole thing.

- The report is an **internal, running working document** kept across the session. It is **NOT a
  deliverable mid-run** — do **not** create, show, or hand the user a report/dossier file mid-session.
  **Each skill delivers only its own two files** (`.md` + `.html`); the consolidated report is
  assembled and delivered **only at the very end**, by the Action Report skill.
- As each skill completes, **record its section into that internal running document** (order below).
  If the user revisits a skill or changes an input, refresh that section so it stays current.
- Sections not produced yet are marked `— not yet completed —`.
- **Place each section in its fixed slot** (order below) regardless of the order you complete skills.
  (Messaging, Conversion, SEO, UX/Technical, and Design & Visual are interchangeable — completion order won't always
  match the slots.)

### Section order
- **Executive summary** (unnumbered) — generated at the end by the Action Report (see below).
1. **Site Snapshot** — what the site is, who it's for, the primary conversion goal, the page inventory.
2. **Goals & Discovery** — the owner's voice, cross-examined against the site: a compressed owner brief, a
   **"Stated vs. observed"** reality-check (each belief vs. what the page + scans show, with the gap named),
   the **tensions**, and a prioritised **"How to reach your goal"** advice block. *Diagnostic intake, not
   graded analysis — no letter grade and no IIF findings; it orients the reader, the five analyses verify it.*
3. **Messaging & Clarity** — grade + criteria, and the `MSG-` findings.
4. **Conversion (CRO)** — grade + criteria, and the `CRO-` findings.
5. **SEO & Content** — grade + criteria, the `SEO-` findings, and the **site-wide SEO sweep table**
   (the homepage is audited in full; secondary pages get a quick per-page sweep — see below).
6. **UX & Technical** — grade + criteria, the `UX-` findings, and the **measured mobile-friendliness**
   results (rendered at phone widths).
7. **Design & Visual** — grade + criteria, the `DSN-` findings, the **measured design tokens** (palette,
   fonts, button-style count), and the rendered desktop + mobile screenshots.
8. **Action Plan** — the Impact × Effort matrix, the overall scorecard, the prioritised roadmap, and
   the "first two weeks / 30–60 / 60–90" plan.

The **Goals & Discovery** section is optional (it appears only if that skill ran) and carries no grade; it
gives the reader the owner's own goals and satisfaction — plus its **"How to reach your goal"** advice — as
context and direction for everything below it.

Each section reuses the content the skill already delivered. Don't re-analyse; pull from the session.

### Executive summary (generated at the end)
A short synthesis placed at the top once the sequence is complete (refresh it if sections change later):
- **Overall grade** and the five dimension grades at a glance.
- **The single biggest opportunity** — the highest-impact issue found, cited by ID.
- **Top 3 quick wins** — highest-impact, lowest-effort fixes, cited by ID.
- **What's working** — 1–2 genuine strengths (don't only list problems).

---

## The consolidated report file (`_[site]-website-audit-report.html`)

The report that accretes during the session is delivered as **one merged document** that is both the
entry point and the complete audit: **`_[site]-website-audit-report`** (`.md` + `.html`, e.g.
`_acme-website-audit-report.html`, where `[site]` is a short slug of the domain). The leading underscore
sorts it to the top of the folder. There is no other hub file.

Structure:
- **Header.** If the audited site yields a usable logo (header logo, `og:image`, or one the user
  provides), show it in the header alongside (or instead of) the site name — embed it as a data URI so
  the file stays self-contained; otherwise fall back to the site **name** as styled text. Never invent
  a logo. Attribution line phrased "**by Ananas Agency**" (e.g. "Website audit of [site] — built with
  the Website Audit Suite by Ananas Agency").
- **Executive summary first** — overall grade, the five dimension grades, the biggest opportunity, the
  top 3 quick wins, what's working. The executive-summary section is **unnumbered**; numbering starts at
  **Site Snapshot = 1**.
- **Then every section in the fixed order above — with real substance, not teasers.** Each section
  carries a meaningful digest: the Site Snapshot facts, each dimension's grade + criteria table + full
  findings list (ID, issue, impact, fix, quadrant), and the Action Plan's matrix + roadmap. A reader who
  never clicks a link still gets the whole audit.
- **Each section heading carries an "Open full document →" button** (`<a class="openbtn" …>`,
  right-aligned in the heading) linking to that skill's `.html`.
- **Every section digest renders full-width.** Each section spans the full content column (`.wrap`).
  Render tables as a bare `<table style="width:100%">` and text as `.row`s directly in the section — do
  **not** wrap a section's digest in `.tablewrap` or `.card` (their inset padding makes that section
  render narrower than its neighbours).

Deliver as two files (`.md` + `.html`), reusing the shared style block and page frame (brand band,
gold-top header card, footer band) so it matches every other deliverable.

---

## Cross-linking, hover hints & navigation

Every generated `.html` is part of one navigable pack. These rules apply to all of them:

1. **Cross-link everything, and tooltip every ID.** Any mention of another deliverable links to its
   canonical file (filenames below). **Every** occurrence of a finding ID outside its own list links
   back to that dimension's page with a `title` tooltip carrying the finding's issue in brief, e.g.
   `<a href="messaging.html" title="MSG-01 — vague homepage headline">MSG-01</a>`. No bare ID codes
   anywhere.
2. **Hover hints on short terms — every occurrence, consistently.** Give a plain-language `title`
   tooltip to **every** appearance (not just the first) of the fixed shorthand set — **IIF, CRO, SEO,
   UX, CTA, the ID prefixes (MSG/CRO/SEO/UX), and the quadrant labels
   (quick win / big bet / fill-in / skip)** — e.g.
   `<abbr title="Issue · Impact · Fix — the finding format">IIF</abbr>`. Apply it uniformly across
   every page; the final regeneration pass verifies the hints are present pack-wide.
3. **Previous / Next buttons — final pack only.** Mid-session, the per-skill `.html` files are working
   copies and carry **no `pagenav`** (they end with the Print hint instead). The prev/next walk is added
   **only by the final regeneration pass** (the Action Report skill), which wires every page in the fixed
   sequence: `site-snapshot.html` → `goals.html` → `messaging.html` → `conversion.html` → `seo.html` →
   `ux-technical.html` → `design.html` → `action-report.html`. The **consolidated report sits at the start**: it is the
   entry file (sorts first, no Previous) and its Next leads into `site-snapshot.html`; Site Snapshot's
   Previous leads back to the report. The Action Report is the end of the walk (no Next). (`goals.html` is
   in the walk only if the Goals & Discovery skill ran; if it didn't, Site Snapshot's Next leads straight
   to `messaging.html`.)
4. **Print hint on every page.** Every generated `.html` ends (after the last section, inside the content
   column) with a no-JavaScript Print hint —
   `<p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>` —
   which relies on the browser's own print and hides itself when printing. No button, no script.
5. **Section numbering.** Give section headings a number chip (`<span class="no">N</span>`) only when
   the page has **two or more** sections; a single-section page uses an unnumbered heading. In the
   consolidated report, the executive summary is unnumbered and numbering starts at Site Snapshot = 1.

**Final consistency pass.** Deliverables are generated as the session progresses, so links can point at
files that don't exist yet. The Action Report skill therefore **regenerates every `.html`** right before
bundling — adding the prev/next walk to every page (mid-session pages carried none), tooltipping every ID,
ensuring the hover hints are present on every term, and wiring the complete cross-link graph. It also
**reconciles the Site Snapshot's open `TBD`s** — backfilling any the session has since answered (from what
was actually captured, never invented) — so the finished pack never ships stale `TBD`s. Mid-session files
are working copies; the regenerated set in the ZIP is the canonical pack.

### Canonical filenames
| Skill | `.md` / `.html` basename |
|-------|--------------------------|
| Site Snapshot | `site-snapshot` |
| Goals & Discovery | `goals` |
| Messaging & Clarity | `messaging` |
| Conversion (CRO) | `conversion` |
| SEO & Content | `seo` |
| UX & Technical | `ux-technical` |
| Design & Visual | `design` |
| Action Report | `action-report` |
| Consolidated report (entry) | `_[site]-website-audit-report` |

---

## Deliverables bundle (`[site]-website-audit.zip`)

Because the skills deliver files one at a time through the chat, the closing step of the Action Report skill
**packs everything into a single ZIP** so the pack travels as one unit and the links work after unzip. The
report `.html` files cross-link each other by bare filename (and share the prev/next walk), so **every
`.md`/`.html` deliverable sits flat at the ZIP root**; the measured **screenshots** and **raw JSON** are
filed into two subfolders so the pack stays tidy — reports on top, evidence beneath.

- **Name:** `[site]-website-audit.zip` (e.g. `acme-website-audit.zip`).
- **Layout:**
  ```
  [site]-website-audit.zip
  ├── _[site]-website-audit-report.html   ← entry point (open first)
  ├── _[site]-website-audit-report.md
  ├── site-snapshot.html / .md
  ├── goals.html / .md
  ├── messaging.html / .md · conversion.html / .md · seo.html / .md
  ├── ux-technical.html / .md · design.html / .md · action-report.html / .md
  ├── assets/          ← screenshots (design.html references these)
  │   ├── design-desktop.png · design-mobile.png
  │   └── mobile-320.png · mobile-390.png · mobile-414.png
  └── data/            ← raw measured JSON (evidence)
      ├── perf-a11y.json · mobile-metrics.json
      ├── design-tokens.json · design-pages.json
      └── seo-sweep.json · interaction.json · tracking.json
  ```
  The `.md`/`.html` deliverables **must stay flat at the root** — that's what keeps their cross-links and the
  prev/next walk resolving. Only the screenshots (`assets/`) and the JSON (`data/`) go in subfolders.
- **Screenshot paths:** `design.html` embeds the renders with `<img src="…">`. In the final pack the
  screenshots live in `assets/`, so the Action Report's final regeneration writes them as
  `<img src="assets/design-desktop.png">` / `assets/design-mobile.png` (same for the design digest in the
  consolidated report). Mid-session working copies keep the flat `design-desktop.png` path — the PNG sits
  beside the file — so both contexts resolve.
- **Contents:**
  - **Root:** the merged report (`_[site]-website-audit-report.md` + `.html`, first by name) and every
    per-skill deliverable produced (`.md` + `.html`; the suite ships no `.txt`): `site-snapshot`, `goals`,
    `messaging`, `conversion`, `seo`, `ux-technical`, `design`, `action-report`.
  - **`assets/`:** every screenshot produced — `design-desktop.png`, `design-mobile.png`, and the mobile
    renders `mobile-320.png` / `mobile-390.png` / `mobile-414.png`.
  - **`data/`:** every raw measured JSON produced — `perf-a11y.json`, `mobile-metrics.json`,
    `design-tokens.json`, `design-pages.json`, `seo-sweep.json`, `interaction.json`, `tracking.json`.
- **How:** build it with code execution (the same capability used to write the files) — create the `assets/`
  and `data/` subfolders and place each file accordingly. If code execution isn't available, list the files
  with their folders and tell the user to recreate that structure so the links and images work.
- **Partial runs:** bundle only what was actually produced (skip any missing deliverable, screenshot, or
  JSON) and say which are missing. In a Basic run with no screenshots/JSON, omit the empty `assets/`·`data/`.

Offer the ZIP as the primary download: "Open `_[site]-website-audit-report.html` inside the zip first."

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)
