---
name: action-report
description: >
  The capstone of the Ananas-Agency Website Audit Suite. Synthesises the findings from the Messaging,
  Conversion, SEO, and UX/Technical analyses into one prioritised action plan: an overall site
  scorecard (letter grades per dimension + overall), an Impact × Effort priority matrix that sorts
  every finding into Quick Wins / Big Bets / Fill-ins / Skip, a phased roadmap (first two weeks /
  30–60 / 60–90 days), and the single consolidated Website Audit Report the user takes away. Use this
  skill when the user wants to: pull the audit together, get the action plan / roadmap / priorities,
  see the overall grade, know what to fix first, or produce the final report. Trigger: "action plan",
  "what should I fix first", "prioritise the findings", "overall grade", "final report", "audit
  summary", "roadmap", "put it all together", "quick wins".
---

# Action Report (Ananas-Agency — Website Audit capstone)

## Goal

Turn the five analyses into a decision. Produce: an **overall scorecard**, an **Impact × Effort priority
matrix**, a **prioritised roadmap** phased into first-two-weeks / 30–60 / 60–90 days, and the single
consolidated **Website Audit Report** the user keeps. This is where a pile of findings becomes "do these
three things Monday."

Written for **business owners and marketers**: the report leads with the decision, not the detail.

## Inputs

- The **Site Snapshot** (Skill 0), the **Goals & Discovery** brief if it was captured (owner satisfaction,
  the one goal + success metric, appetite & constraints; context, not findings), and whichever of the five
  analyses were run: **Messaging & Clarity** (`MSG-`), **Conversion (CRO)** (`CRO-`), **SEO & Content**
  (`SEO-`), **UX & Technical** (`UX-`), **Design & Visual** (`DSN-`).
- Pull the findings, grades, and "what's working" notes from the session. **Do not re-analyse.** If some
  analyses weren't run, proceed with what exists and say clearly which dimensions are missing.

## What it produces

1. **Overall scorecard**: the completed dimension grades side by side, plus an **overall grade** (average
   of the completed dimension scores, mapped to the same A–F bands). See
   [report-format.md](../../report-format.md).
1b. **"2026 standard vs your site" scorecard**: a compact table of the key benchmarks from
   [benchmarks-2026.md](../../benchmarks-2026.md) (Core Web Vitals, mobile/tap targets, WCAG 2.2 AA, title
   tags, HTTPS, clear value prop, trust at the ask, consent) each marked **met / gap / not measured** for
   this site, so the reader sees exactly where they stand against what a website should be in 2026.
2. **Impact × Effort matrix**: every finding from every dimension placed in its quadrant
   (**Quick Win / Big Bet / Fill-in / Skip**), cited by ID.
3. **Prioritised roadmap**: an ordered do-this list: all Quick Wins first (highest impact first), then
   Big Bets, then Fill-ins; Skip items are listed but flagged as backlog.
4. **Phased plan**: first two weeks (the quick wins), days 30–60 (start the big bets, measure), days
   60–90 (finish big bets, re-audit).
5. **Executive summary**: overall grade, the biggest single opportunity (by ID), the top 3 quick wins,
   and what's genuinely working.
6. **The consolidated Website Audit Report**: one merged entry document (`_[site]-website-audit-report`)
   that carries the whole audit, plus the ZIP bundle.

## Conversation flow

### Step 1: Gather everything from the session
Collect every finding (ID, issue, impact, effort, quadrant) and every dimension grade produced so far,
plus the Site Snapshot. Note which analyses are missing.

### Step 2: Build the overall scorecard
Show the completed dimension grades and compute the **overall grade** (average of completed dimension
scores → A–F). State it's an expert judgement, not a lab score. If dimensions are missing, average only
what exists and say so.

### Step 3: Place every finding on the matrix
Assign each finding to its quadrant from its Impact × Effort (rules in
[report-format.md](../../report-format.md)). Build the 2×2. Sanity-check the ratings for consistency across
dimensions (an "Impact 5" in one analysis should be as serious as an "Impact 5" in another) and adjust
outliers, noting any change.

### Step 4: Order the roadmap and phase it
Order: **Quick Wins** (impact desc) → **Big Bets** (impact desc) → **Fill-ins**; list **Skip** separately
as backlog. Then split into **first two weeks** (quick wins), **30–60 days** (kick off big bets + start
measuring against the site's primary goal), **60–90 days** (finish big bets, then re-audit).

### Step 5: Write the executive summary
Overall grade + dimension grades; the biggest single opportunity (highest-impact finding, by ID); the top
3 quick wins (by ID); and 1–2 real strengths.

### Step 6: Deliver the Action Report files
Generate `action-report.md` and a styled `action-report.html` (scorecard, matrix, roadmap, phased plan,
exec summary, and the one agency CTA block). Format and components: see
[references/rules-action-report.md](references/rules-action-report.md).

### Step 7: Assemble & deliver the consolidated Website Audit Report
Now assemble the internal running report into the single merged deliverable
**`_[site]-website-audit-report`** (`.md` + `.html`): executive summary at the top, then every section in
fixed order with full-substance digests, logo/name header, per-section "Open full document →" buttons.
Full spec: [report-format.md](../../report-format.md).

### Step 8: Final consistency pass (regenerate every page)
Regenerate **every** `.html` in the pack in sequence order to wire the **Previous/Next walk**, tooltip
**every** finding ID, ensure the **hover hints** are on every shorthand term, fix cross-links now that all
files exist, and **reconcile the Site Snapshot's `TBD`s** (backfill any the session answered; never
invent). The walk: `_[site]-website-audit-report` → `site-snapshot` → `goals` → `messaging` → `conversion` → `seo`
→ `ux-technical` → `design` → `action-report`. (`goals` is in the walk only if Goals & Discovery ran; if
not, `site-snapshot` links straight to `messaging`.) **Also repoint the screenshots:** since the final pack
files screenshots under `assets/`, regenerate `design.html` (and the consolidated report's design digest)
with `<img src="assets/design-desktop.png">` / `assets/design-mobile.png`. **De-AI pass:** while
regenerating, run the house-style self-check on every page and rewrite any flagged prose: em-dash density
above ~1/150 words is the main offender ([report-format.md](../../report-format.md), "Write like a human:
no AI patterns"). Details: [report-format.md](../../report-format.md), "Final consistency pass" and
"Deliverables bundle".

### Step 9: Bundle the ZIP
Pack **`[site]-website-audit.zip`** (built with code execution) in the layout from
[report-format.md](../../report-format.md), "Deliverables bundle": the `.md`/`.html` deliverables **flat at
the root** (so their cross-links and the walk resolve), the **screenshots in `assets/`**
(`design-desktop.png`, `design-mobile.png`, `mobile-320/390/414.png`), and the **raw measured JSON in
`data/`** (`perf-a11y.json`, `mobile-metrics.json`, `design-tokens.json`, `design-pages.json`,
`seo-sweep.json`, `interaction.json`, `tracking.json`). Offer it as the
primary download: "Open `_[site]-website-audit-report.html` inside the zip first." For partial runs,
bundle only what exists and say what's missing.

## Critical rules

1. **Don't re-analyse.** Synthesise from the findings already produced. New insight is fine; re-running
   the analyses is not.
2. **Every finding lands in exactly one quadrant.** No orphans. The matrix must account for all of them.
3. **Lead with the decision.** Quick wins and the overall grade come first; detail follows.
4. **Consistency across dimensions.** Normalise Impact/Effort so a "5" means the same everywhere; note any
   adjustment.
5. **Handle partial runs honestly.** Average and report only the dimensions that ran; name the gaps.
6. **One CTA, once.** The agency CTA block appears in exactly one place (the Action Report / consolidated
   report closing), nowhere else in the pack.
7. **The regenerated pack is canonical.** Mid-session files are working copies; the ZIP's regenerated set
   is the one that ships, with the full walk, tooltips, and reconciled TBDs.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
