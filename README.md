# Ananas-Agency: Website Audit Suite

A suite of **AI agent skills** that turn an assistant (Claude, or any skill-compatible agent) into a
guided website auditor. You give it a URL; it reads the live site and produces a concrete, prioritised
audit (messaging clarity, conversion, SEO, and UX/technical health), each graded and each finding
sorted into a do-this-first action plan.

The skills are written as plain Markdown with YAML frontmatter, so they are version-controllable,
diffable, and editable outside any tool. They also ship as importable `.skill` packages.

> **License:** [MIT](LICENSE). Free to use, adapt, and share. A credit to the author,
> **Kostiantyn Ivanov** (Ananas-Agency, [ananas-agency.com](https://ananas-agency.com)), is warmly
> appreciated but not required.

---

## Two layers: Basic and Extended (both free)

The suite runs in two layers. **Both are free**. The only difference is a one-time setup that unlocks
*measured* evidence. You never lose anything by staying on Basic; Extended just fills in hard numbers.

### 🟢 Basic layer: works in any Claude, nothing to install
Runs in the **Claude web app, the Desktop app, or Claude Code**. Claude reads your live site and reasons
about it, producing the **full graded audit**: findings, priorities, the A–F scorecard, the 2026-standard
comparison, and the styled report. This is the expert-review layer, and it covers most of the audit.

### 🔵 Extended layer: adds hard, *measured* evidence
Adds the checks Claude can't do by only *reading* a page, because they need the page to be actually
**rendered and timed**: real Core Web Vitals, an accessibility (WCAG) scan, measured mobile fit & tap
targets, design-token analysis with screenshots, and live tracking/consent behaviour. These run via
bundled tools and need a real environment.

**Extended setup (one time, any OS: Windows / macOS / Linux):**
```bash
# 1. Claude Code (the environment that can run the tools):
npm install -g @anthropic-ai/claude-code
# 2. Python 3 (python.org), then the render engine — bundles its own Chromium, no browser to install:
pip install playwright
playwright install chromium
```
Then open the suite in Claude Code and ask *"Run the full website audit of https://mysite.com."* Claude
then runs the measurement tools automatically and fills the measured findings into the report.

### What each layer covers
| Dimension | 🟢 Basic (no install) | 🔵 Extended adds (needs the setup) |
|---|---|---|
| Site Snapshot | Full | — |
| Goals & Discovery | Full (owner interview) | — *(runs in parallel with the scans)* |
| Messaging & Clarity | Full (incl. cross-page) | *(optional: screenshot-based read)* |
| Conversion (CRO) | Full findings + CTA/link check + "is analytics installed?" | **Consent-before-load & cookie behaviour, runtime conversion-tracking proof** |
| SEO & Content | Full (Claude reads the key pages) | Automated site-wide sweep (faster, more pages, exact) |
| UX & Technical | Viewport/HTTPS, markup accessibility, navigation, speed *risk flags* | **Real Core Web Vitals · full axe accessibility scan · measured mobile fit & 44px tap-targets** |
| Design & Visual | Declared colours/fonts; visual read *if you paste a screenshot* | **Measured design tokens, auto desktop+mobile screenshots, cross-page consistency** |
| Action Report | Full synthesis + 2026 scorecard | Same, with the measured findings filled in |

In a Basic report, the Extended-only checks are honestly labelled **"not measured, available with the
Extended layer."** In an Extended report, the tool-backed findings carry a small **`measured`** tag so you
can see exactly which evidence came from a real render.

---

## What's inside

Eight skills, each in its own numbered folder, plus one compiled handbook.

| # | Skill | What it produces | Needs first |
|---|-------|------------------|-------------|
| 0 | **Site Snapshot** | Fetches the URL and captures what the site is, who it's for, its **primary conversion goal**, and its key pages — the reusable foundation. | — (start here) |
| 1 | **Goals & Discovery** | The owner's voice: are they happy with the site, and what do they want it to achieve? A short interview capturing satisfaction, the one goal + a success number, frustrations, appetite & constraints — then directional advice on how to reach them. Runs *while* the site is analysed. | 0 — **blocks 2–7** |
| 2 | **Messaging & Clarity** | Is the value proposition, headline, and call to action instantly clear? Graded, with `MSG-` findings. | 0 **+ 1** |
| 3 | **Conversion (CRO)** | Funnel, CTAs, forms, trust signals, distractions, pricing clarity. Graded, with `CRO-` findings. | 0 **+ 1** |
| 4 | **SEO & Content** | Titles, meta, headings, keywords/intent, content depth, schema, indexability. Graded, with `SEO-` findings. | 0 **+ 1** |
| 5 | **UX & Technical** | Navigation, **measured** mobile-friendliness (fit-to-screen, tap-target & text sizes via a real headless-browser render), speed signals, accessibility, links, security. Graded, with `UX-` findings. | 0 **+ 1** |
| 6 | **Design & Visual** | Renders the site (desktop + mobile) and judges the visual design: hierarchy, typography, colour, whitespace, imagery, modern-vs-dated — plus **measured** design tokens (palette, fonts, button-style count). `DSN-` findings. | 0 **+ 1** |
| 7 | **Action Report** | Overall scorecard, an Impact × Effort priority matrix, a phased roadmap, and the single consolidated **Website Audit Report**. | 2–6, **and 1** |

> **Skill 1 is not optional and not a side-quest.** "Runs in parallel" describes its *timing*, not its
> priority: it must be **started before any of 2–6 is written**, because every finding in 2–6 is graded
> against the owner's stated goal. A plan that lists 0, 2, 3, 4, 5, 6, 7 and omits 1 is a broken plan —
> if you are building a task list for this suite, **1 goes in it**.

### Recommended order

```
  LAYERS   🟢 Basic     Claude reads & reasons — works anywhere, nothing to install.
           🔵 Extended  🟢 + measured tools (Playwright/Chromium) that really render & time the page.
              *  = this skill gains hard, tool-backed "measured" evidence when the Extended tools can run.

        ┌───────────────────────┐   ┌────────────────────────┐
        │ 0. Site Snapshot      │──▶│ 1. Goals & Discovery   │  ← owner interview; runs WHILE the
        └───────────────────────┘   └────────────────────────┘     * scans below render (in parallel)
                    ▼
      ┌─────────────┼─────────────┬─────────────┬─────────────┐
      ▼             ▼             ▼             ▼             ▼
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│ 2. Msg    │ │ 3. CRO *  │ │ 4. SEO *  │ │ 5.UX/Tech*│ │ 6. Design*│  ← run any / all
└─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
      └─────────────┴─────────────┬─────────────┴─────────────┘
                                  ▼
                      ┌───────────────────────┐
                      │ 7. Action Report      │  ← ties it together; measured findings filled in
                      └───────────────────────┘

  🟢 Basic everywhere · 🔵 Extended adds the * measurements · both free — the only difference is the one-time tool setup.
```

Start with **Site Snapshot**, then **Goals & Discovery** — intake too, and mandatory: it captures the
owner's goals and, being paced by the owner answering, runs *concurrently* with the site read/scans (see
"Run the interview while the analysis runs" below). Skills 2–6 are independent; run one, some, or all.
Skill 7 synthesises whatever you ran into one plan.

### Run the interview while the analysis runs

**Goals & Discovery** and the site analysis use different resources, so they overlap instead of competing:
the interview is *owner-paced* (most of its time is spent waiting for the owner to answer), while the reads
and scans are *machine-paced*.

- **Extended layer (Claude Code):** genuinely parallel. As soon as it has the URL and a Snapshot, Claude
  launches the measured scans (`perf-a11y-scan.py`, `mobile-audit.py`, `design-scan.py`, …) **in the
  background**, then conducts the interview while they render, hiding the slowest part of the audit behind
  the conversation. When the interview wraps, the scan results are waiting.
- **Basic layer (Claude web/desktop app):** no background thread, so it *interleaves*: read a page, ask a
  question, read the next while the owner answers. It feels concurrent and nothing is wasted.

Either way, the owner never watches a progress bar. They're being talked to while the machine works.

### Never write the audit without asking the owner first

Even when the request sounds fully automatic ("run the full audit of mysite.com"), the interview still
happens — an audit graded against a goal nobody stated is guesswork wearing a grade. Concretely:

- **Ask the first question before writing any of skills 2–6.** Launch the scans, then ask. Not afterwards,
  and not once the analyses are already written.
- **Never infer, assume, or invent the owner's answers** from the page, the scans, or the industry. The
  value of the brief is the *gap* between what the owner believes and what the site shows; a brief you
  wrote yourself has no gap in it.
- **If you genuinely cannot ask** (a headless or scheduled run with no one to answer), don't fake it:
  produce the brief with every field marked **NOT CAPTURED**, say at the top of the report that the audit
  is ungrounded because no owner input was available, and note what the interview would have changed.

---

## The Finding format (IIF) and the priority model

Everything is built on one repeatable unit, a **Finding**, written as **Issue · Impact · Fix (IIF)**:

- **I (Issue):** the specific problem on the page, with the actual copy or element quoted as evidence.
- **I (Impact):** what it costs the business (lost conversions, unclear message, missed search traffic,
  friction), rated **1–5**.
- **F (Fix):** the concrete change to make, ideally with a worked example.

Each finding also gets an **Effort 1–5**, and the two combine into a **priority quadrant**:

| | Low effort | High effort |
|---|---|---|
| **High impact** | **Quick Win** — do first | **Big Bet** — plan & schedule |
| **Low impact** | **Fill-in** — when convenient | **Skip** — backlog |

Each analysis also gives the dimension a **letter grade** (A–F, 0–100) from a transparent rubric, and the
Action Report rolls the four up into an **overall grade** and a single prioritised roadmap.

### Graded against the 2026 standard

Findings aren't opinion. Every rubric "Pass" and every gap is measured against
[benchmarks-2026.md](benchmarks-2026.md): **what a website should be in 2026**, with concrete, sourced
thresholds (Core Web Vitals ≤ 2.5s / 200ms / 0.1, tap targets ≥ 44px, WCAG 2.2 **AA** (legally required
for many under the EU Accessibility Act since June 2025), unique 50–60-char titles, HTTPS + HSTS, schema,
AEO-readiness, and more). The Action Report renders a **"2026 standard vs your site"** scorecard so a
company sees exactly where it stands and what to update. It's a living file. The year is in the name.

> **Honesty by design.** What the bundled Python tools can measure locally is **measured, with no
> API keys**: Core Web Vitals, INP (a lab proxy), accessibility, security, mobile fit, design tokens, links,
> and structured data. What only the owner's own analytics can show (conversion rates, traffic, rankings, index
> status) is **owner-reported** (captured in the Goals & Discovery interview) or left out, never invented or
> estimated. In the Basic layer (no headless browser) the measured checks simply fall back to "not measured".

### Measured, not guessed (headless-Chrome tools)

Static HTML can't tell you whether a page *fits a phone*, how *fast* it is, whether it's *accessible*, or
what its *design system* looks like. Those need a real render. So the suite drives **headless Chrome** to
**measure** them, and quotes the real numbers as evidence:

- **Mobile-friendliness** (`mobile-audit.py`): fit-to-screen, oversized elements/images, tap targets ≥ 44px, text ≥ 12px, per width (320/390/414) + screenshots.
- **Performance + security** (`perf-a11y-scan.py`): lab Core Web Vitals (LCP, CLS, FCP, TTFB), an **INP lab proxy** (Total Blocking Time), page weight & heaviest resources; plus **HTTPS, TLS version, security headers (HSTS/CSP/…), the redirect chain, and mixed content**.
- **Accessibility, real WCAG violations** (`perf-a11y-scan.py`, injects **axe-core**): grouped by impact (critical/serious/moderate/minor) + a **keyboard focus-order pass**.
- **Design tokens + interior templates** (`design-scan.py`): the real palette, fonts, and button-style count + desktop/mobile renders; with `--pages`, screenshots of representative interior templates (article, service page, case study) and their **measured readability** (text-alignment, chars-per-line, words-per-visual).
- **Site-wide SEO + schema** (`seo-sweep.py`): a static per-page sweep of the secondary pages, with **local structured-data validation** (JSON parse + required-field checks per type).
- **Measurement-readiness** (`tracking-scan.py`): is GA4 / conversion tracking / a real consent layer actually set up? do trackers fire before consent?
- **Interaction + links** (`interaction-scan.py`): does the CTA reach a real destination and does the form validate, across key pages, **plus the HTTP status of every link**, all **without ever submitting**.

```bash
pip install playwright        # one-time
playwright install chromium   # one-time — bundles its own Chromium (no browser to install)
python scripts/perf-a11y-scan.py https://example.com/ --out out
```

The measured tools use **Playwright**, which downloads its own Chromium and runs the same on **Windows,
macOS, and Linux**, with nothing else to install and **no API keys** (the SEO sweep is pure Python, no browser
at all). If Playwright isn't installed, each skill falls back to "not measured" and describes the observable
signals. It never guesses and never sends you to a third-party service.

---

## Repository structure

```
.
├── README.md
├── LICENSE (MIT)
├── Website Audit Suite - Handbook by Ananas Agency.md   ← all six skills compiled into one document
├── report-format.md                                     ← the shared spec: Finding format, scoring, matrix, dossier, bundle
├── benchmarks-2026.md                                   ← what a website should be in 2026: the sourced standards the audit grades against
├── scripts/
│   ├── repack-all-skills.py                             ← rebuilds the .skill archives after editing
│   ├── build-handbook.py                                ← rebuilds the handbook from the skill sources
│   ├── mobile-audit.py                                  ← measured mobile-friendliness test (headless Chrome); bundled inside the UX & Technical skill
│   ├── perf-a11y-scan.py                                ← measured lab Core Web Vitals + axe-core accessibility; bundled inside the UX & Technical skill
│   ├── seo-sweep.py                                     ← site-wide quick SEO sweep (static crawl); bundled inside the SEO & Content skill
│   ├── design-scan.py                                   ← design-token extraction + desktop/mobile renders; bundled inside the Design & Visual skill
│   ├── tracking-scan.py                                 ← measurement-readiness: analytics/pixels/consent/conversion tracking; bundled inside the Conversion (CRO) skill
│   └── interaction-scan.py                              ← CTA reachability + form validation across key pages (never submits); bundled inside the Conversion (CRO) skill
│
├── 0 Site Snapshot/
│   ├── site-snapshot.skill                              ← installable package (zip)
│   └── site-snapshot/                                   ← unpacked source of the .skill
│       ├── SKILL.md
│       └── references/rules-snapshot.md                 ← also holds the shared HTML design system
│
├── 1 Goals Discovery/       ← (goals-discovery,   rules-goals-discovery.md) — owner interview, runs in parallel
├── 2 Messaging Clarity/     ← (messaging-clarity, rules-messaging-clarity.md)
├── 3 Conversion CRO/        ← (conversion-cro,    rules-conversion.md)
├── 4 SEO Content/           ← (seo-content,       rules-seo.md)
├── 5 UX Technical/          ← (ux-technical,      rules-ux-technical.md)
├── 6 Design Visual/         ← (design-visual,     rules-design-visual.md) — bundles scripts/design-scan.py
└── 7 Action Report/         ← (action-report,     rules-action-report.md)
```

### File types

| File | What it is |
|------|------------|
| **`<slug>.skill`** | The installable package — a ZIP containing `SKILL.md` + `references/`. Import this into an agent. |
| **`<slug>/SKILL.md`** | The skill definition: YAML frontmatter (`name`, `description`, triggers) + the body (goal, flow, rules). |
| **`references/rules-*.md`** | The detailed reference each skill links to: tests, scoring rubric, examples, output templates. |
| **`report-format.md`** | The one shared spec every skill points to — the Finding format, Impact/Effort scales, grade bands, the consolidated-report assembly, cross-linking, and the bundle. |
| **`Website Audit Suite - Handbook …md`** | Every skill and reference compiled into one readable document. Read this to understand the whole system without installing anything. |

---

## Which AI to use

These are **Agent Skills for Claude**, the AI assistant by Anthropic. Skills are a native Claude feature,
so Claude is the recommended way to run them. You can use any of:

- **Claude apps: [claude.ai](https://claude.ai) (web) or the Claude Desktop app.** Easiest, no coding.
  The Skills feature is available on paid plans.
- **Claude Code**: Anthropic's command-line/IDE tool, for developers who want the skills in their projects.
- **Claude API / Agent SDK**: for building the skills into your own application.

Because the suite is **URL-first**, run it on a setup that can **fetch web pages** (Claude with web access,
or Claude Code). If your model can't browse, paste the page text or screenshots and the skills work from that.

For the best results, run them on a top-tier model: **Claude Opus** (highest quality) or **Claude Sonnet**
(faster, still excellent).

---

## How to use: pick the path that fits you

### Path 1: Copy & paste (easiest, works on any plan, zero setup)
1. Open a skill's `SKILL.md`, e.g. [0 Site Snapshot/site-snapshot/SKILL.md](0%20Site%20Snapshot/site-snapshot/SKILL.md).
2. Copy everything from the first `#` heading down (you can ignore the small `---` metadata block at the top).
3. Paste it into a new Claude conversation and send: *"Follow these instructions and audit my website, here's the URL: …"*.
4. Answer the few questions it asks. It produces your finished document.

> Tip: do **Site Snapshot** first. The analyses build on it. When a later skill asks for your snapshot,
> paste the result you got from skill 0.

### Path 2: Install as a Skill in the Claude app (recommended for most people)
1. In Claude, open **Settings → Capabilities** and turn on **Skills** (and code execution if prompted).
2. Find the package you want, e.g. `0 Site Snapshot/site-snapshot.skill`. **It's a ZIP**. If the uploader
   only accepts `.zip`, rename it. Click **Upload skill** and select it. Repeat for each skill.
3. Start a chat and describe what you need (*"Audit my website"*, *"Is my homepage message clear?"*,
   *"Give me an SEO review of …"*), and Claude runs the matching skill.

### Path 3: Use in Claude Code (for developers)
1. Install Claude Code (`npm install -g @anthropic-ai/claude-code`) and open your project.
2. Copy a skill's **unpacked folder** into your skills directory:
   - For all projects: `~/.claude/skills/site-snapshot/`
   - For one project only: `<your-project>/.claude/skills/site-snapshot/`

   The folder must contain `SKILL.md` and the `references/` folder, which is exactly what the
   `site-snapshot/` folder in this repo already is.
3. Run `claude` and ask in plain language. Claude invokes the skill by its description.

### What happens when a skill runs
- It **fetches your site** and reads it, then confirms a few facts with you (it comes with a draft, not a
  blank form).
- It delivers **two files** per skill: a `.md` (documentation) and a styled, self-contained `.html`
  (share-ready, prints cleanly to PDF).
- The **Action Report** bundles everything into one `.zip` with a single consolidated report as the entry
  point: the reports (`.md`/`.html`) sit at the top, with screenshots in `assets/` and the raw measured JSON
  in `data/`.

### Just want to read the method?
Open [Website Audit Suite - Handbook by Ananas Agency.md](Website%20Audit%20Suite%20-%20Handbook%20by%20Ananas%20Agency.md): every skill and reference in one document. No AI or installation required.

---

## Editing & repacking

The unpacked `<slug>/` folders are the single source of truth. The agent reads the `.skill` archive, so
**after editing you must rebuild the archives** (and, if you want, the handbook):

```bash
python scripts/repack-all-skills.py   # rezips every <slug>/ into its .skill
python scripts/build-handbook.py      # regenerates the compiled handbook
```

---

## License & attribution

Licensed under the **MIT License**; see [LICENSE](LICENSE). You may use, adapt, and share it, including
commercially. Keeping the copyright notice is all that's required; a visible credit is appreciated:

> "Ananas-Agency Website Audit Suite" by **Kostiantyn Ivanov** (Ananas-Agency, ananas-agency.com).
