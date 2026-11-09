# Website Audit Report: shared method, scoring & style

This is the single shared method every skill in the **Website Audit Suite** points to. It defines:

1. the **Finding** format every analysis skill uses (Issue · Impact · Fix),
2. the **Impact × Effort** priority model and the **letter-grade scorecard**,
3. the writing style and the honesty rule,
4. how the builder assembles the pack.

The **standard the audit grades against** (what a website is expected to be, with concrete, sourced
thresholds) lives in [benchmarks-2026.md](benchmarks-2026.md). Every rubric "Pass" and every "the
standard is X, you're at Y" finding traces back to it; the Action Report renders a **"2026 standard vs
your site"** scorecard from it.

If a rule about findings, scoring, grades or the matrix is needed anywhere,
it lives here. The skills reference this file instead of re-stating it.

## Audit depth (two-tier)

The suite spends effort where it matters:

- **The homepage is the main page. It gets the full, in-depth audit** across all five dimensions
  (Messaging, Conversion, SEO, UX/Technical, Design & Visual), including the **measured mobile-friendliness render**
  (UX & Technical) at phone widths.
- **Secondary pages** (services, products, case studies, articles, about, contact) get **targeted
  multi-page checks** (broad coverage without a full audit of every page):
  - **SEO**, a site-wide static sweep (`seo-sweep.py`): titles, metas, H1s, canonicals, indexability,
    word count, alt, schema across a sample (~5 per type).
  - **Messaging**, a cross-page clarity/consistency read of the key pages (H1, CTA, hero), reusing the
    sweep + interaction data.
  - **Design & UX**, a template read of representative interior pages (`design-scan.py --pages`): renders
    and screenshots one article, one service/offering page, and one case study, compares their tokens for
    consistency, and **measures readability** (text-alignment, chars-per-line, words-per-visual). This
    catches the layout, text-density and readability problems that live on template pages, not the homepage.
  - **Conversion**, a multi-page interaction pass (`interaction-scan.py`): CTA reachability + form
    validation on the homepage, contact, and a top page (never submitting).
  This keeps coverage broad and token/time cost low. The user can widen or narrow it (`--per-type`,
  `--pages`, or naming specific pages).

The fetching, rendering, and sweeping run as **tools** (headless-browser render, static crawl) that
return compact summaries. They cost local compute, not model tokens; only the summaries enter the audit.

## Basic & Extended layers (both free)

Every skill runs in one of two layers, decided by the environment, **not** by payment (both are free):

- **Basic layer**: Claude reads the live page(s) and reasons. Produces the full graded audit from what's
  observable in the source + expert judgement. It's the fallback when the setup check
  (`scripts/setup-check.py`) reports that Playwright or its browser is missing, or when a scan can't reach
  the site.
- **Extended layer**: the bundled tools additionally **render/measure** the page (Python 3.9+, Playwright +
  Chromium, and network access to the site). The setup check prints the install commands for the
  Python that ran it. Adds the hard numbers a static read can't produce.
  The setup check reports this layer as `MODE: extended`.

**How each skill behaves:** every measured step already says *"if the bundled tool can run, measure it;
otherwise mark it 'not measured' (Basic layer) and describe the observable signals."* That fallback **is**
the layer switch. The same skill file produces a Basic report where the tool can't run and an Extended
report where it can. The bundled tools need no API keys; they never point the reader at a third-party
service.

**The `measured` tag.** Mark a finding backed by a tool render (Core Web Vitals, axe accessibility,
mobile fit/tap-targets, design tokens, tracking/consent, interaction) with `measured: true`. The builder adds
the chip and the run-mode line. Reasoning-only (Basic) findings carry no flag. In a Basic report, list the
Extended-only checks as **"not measured, available with the Extended layer,"** so the reader sees what an
Extended run would add.

---

## The Finding format (Issue · Impact · Fix)

Every observation any analysis skill makes is a **Finding**, the core unit of this suite (its
equivalent of a value proposition). A finding is a triple plus two ratings:

- **I (Issue).** The concrete, specific problem observed on the page, with **evidence**: quote the
  actual copy, name the element, or give the page/location. Not "the messaging is weak" but
  "the homepage H1 reads 'Welcome to our website', which says nothing about what you do or for whom."
- **I (Impact).** What the issue **costs the business**: lost conversions, an unclear message,
  missed search traffic, added friction, eroded trust. Rated **Impact 1–5** (see below).
- **F (Fix).** The specific, actionable recommendation: what to change and, where useful, to what.
  Not "improve the headline" but "replace with a benefit-led H1, e.g. 'Bookkeeping for tradespeople:
  sorted in an hour a week'."

Plus:

- **Effort 1–5**: how hard the fix is to implement (see below).
- **Priority**: derived from Impact × Effort (the quadrant, below).

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
Split each axis at its midpoint: **Impact High = 3–5, Low = 1–2**; **Effort Low = 1–2, High = 3–5.**

| | Low effort (1–2) | High effort (3–5) |
|---|---|---|
| **High impact (3–5)** | **Quick Win** — do first | **Big Bet** — plan & schedule |
| **Low impact (1–2)** | **Fill-in** — do when convenient | **Skip** — backlog / don't bother |

Within a quadrant, rank by Impact descending, then Effort ascending. Every finding carries exactly
one quadrant label: `quickwin`, `bigbet`, `fillin`, or `skip`. The builder computes the label from the
two ratings, so you only choose Impact and Effort.

> **Honesty rule (applies to every skill).** Report only what you can actually verify: from the page you
> fetched (its copy, HTML, headings, meta tags, alt text, links, structure), from what renders, and from the
> bundled measurement tools (which run locally, no API keys). Page-load time, Core Web Vitals, INP (lab
> proxy), accessibility, security, mobile fit, design tokens, links and structured data are **measured** when
> the tools can run; in the **Basic layer** (no browser) mark them **"not measured"** and describe the
> observable signals. Don't point at a third-party service. Metrics only the owner's analytics can show
> (conversion rates, traffic, rankings, index status) are **owner-reported** (from Goals & Discovery) or left
> out, never invented or estimated. A grade is an expert judgement, not a lab measurement; label it as such.

---

## Write like a human: no AI patterns (every deliverable)

Every `.md` and `.html` this suite generates is read by a business owner, so it must not read as
machine-written. Before delivering any file, self-check the connective prose against the list below. These
are the fingerprints the **[AI Pattern Detector](https://github.com/ananas-agency/ai-pattern-detector)**
flags; run that skill on the finished deliverables as a final QA if it's available. The findings themselves
(Issue · Impact · Fix) are already concrete, so keep the sentences around them just as plain.

**Punctuation (the biggest tell).**
- **Em-dashes: rare.** At most one per ~150 words, and never two in a paragraph (the detector calls em-dash
  density its single most reliable AI signal). Prefer a full stop, a comma, or brackets. Never the dramatic
  pivot "not X, it's Y".
- **Vary sentence length.** Mix short (3–6 words) with longer ones; don't cluster every sentence at 15–25 words.
- Don't stack hyphenated compounds (ever-evolving, cutting-edge, best-in-class).

**Banned vocabulary.** leverage, delve, robust, seamless(ly), elevate, unlock, empower, transformative,
cutting-edge, myriad, paradigm, boasts, foster, streamline, harness, holistic, "at its core", "when it comes
to", "in the realm of", "navigate the". Use the plain word instead.

**Banned constructions.**
- Stock openers ("In today's fast-paced world", "Let's dive in").
- Antithesis ("It's not X, it's Y"), rule-of-three triples, self-answered questions ("The result? …").
- Closers ("In conclusion", "At the end of the day", "The bottom line").
- Hedges and throat-clearing ("It's worth noting", "It's important to note").
- Meta-commentary ("Here's the thing", "Plot twist:").

**Structure and voice.**
- Vary list length; don't default every list to 3, 5, or 7 items.
- Name the actor. "The 11-field form loses visitors", not "friction emerges" (no false agency).
- Concrete beats abstract: a number or a quoted element beats "significant implications".

If a sentence could open any agency's report, cut it or rewrite it. When in doubt, remove a word.

---

## The scorecard (letter grade per dimension)

Each analysis skill (Messaging, Conversion, SEO, UX/Technical, Design & Visual) ends by scoring its dimension **0–100**
and mapping it to a **letter grade**. The score is rubric-based and transparent: each skill's reference
lists ~8–12 weighted **criteria**; rate each **Pass** (full weight), **Partial** (half), or **Fail**
(zero), sum the weights, and normalise to 0–100. Always show the reader the criteria table so the grade
is explainable, not a black box.

**Each criterion's "Pass" is the 2026 standard**, not a subjective preference. The thresholds come from
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

## Assembly (done by the builder)

You write the findings, grades and prose as JSON. `scripts/build-report.py` turns them into the pack: every
page, the consolidated report, cross-links, ID tooltips, hover hints on the shorthand terms, the
previous/next walk, and the ZIP. Don't write HTML, filenames or links yourself.

- **IDs** (`MSG-01`, `CRO-03` and so on) are assigned by the builder. Refer to another finding as `[[key]]`,
  never by a typed ID.
- **You still own** the quality of the prose, the `[[key]]` references, and reconciling the Site Snapshot's
  open `TBD`s (from what the session actually captured) before the `--final` build.

The data contract is in [audit-data-format.md](audit-data-format.md).

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)
