# Goals & Discovery Rules — Detailed Reference

The owner's-voice intake. This skill runs a short, warm interview and produces a **Goals & Discovery
brief** (no grades, no findings). It pairs with the [Site Snapshot](../../../0%20Site%20Snapshot/site-snapshot/references/rules-snapshot.md)
and gives every analysis the human context a crawler can't see. This reference holds the question bank,
the satisfaction pulse, the reconciliation rule, and the output format.

## Run it in parallel (do this first)

The interview is **owner-paced** (it spends its time waiting on the person, not the machine), so overlap
it with the parts of the audit that *are* machine-bound:

- **Extended layer (tools available).** As soon as you have the URL and a Snapshot, launch the measured
  scans **in the background** so control returns to you immediately, then interview while they render:
  ```bash
  # launch each in the background (do not block on them), then start the interview
  python scripts/perf-a11y-scan.py https://example.com/ --out out &
  python scripts/mobile-audit.py   https://example.com/ --out out &
  python scripts/design-scan.py    https://example.com/ --out out &
  python scripts/seo-sweep.py      https://example.com/ --out out &
  ```
  (In an agent runtime, use its background-run mechanism rather than a literal shell `&`.) When the
  interview wraps, collect the outputs. They've been rendering the whole time.
- **Basic layer (no tools).** No background thread exists, so **interleave**: read a page, ask a question,
  read the next while the owner answers. Same feel, no wasted time.

The rule: **never make the owner watch a progress bar.** Talk to them while the machine works.

---

## The question bank (ask 6–9, in 1–2 passes, 2–3 at a time)

Warm and curious, not a form. Each question is tagged with its form:
- **[pick-1]**: single-select pickable (force one answer); always add an **"Other"** so a pick never traps them.
- **[pick-many]**: multi-select pickable ("pick all that apply"); use where more than one is usually true.
- **[open]**: free text, in the owner's own words; can't be pre-listed, and carries the richest material, so
  quote it verbatim.

Don't make it all multiple-choice: the **[open]** questions are where the value is.

### 1. Satisfaction today **[pick-1]**
- "How do you feel about your website right now?" Offer **very happy / it's okay / frustrated** (+ Other).
- **Optional pulse (1–5):** a quick self-rating so the brief has a shape. *This is the owner's view, not the
  audit's grade. Always label it that way.*

  | Area | Owner's 1–5 | In their words |
  |------|:-----------:|----------------|
  | Look & feel | | |
  | Message is clear | | |
  | Brings leads / sales | | |
  | Easy to update | | |

### 2. The one goal **[pick-1]**
- "Of everything the site could do, what's the **single most important** thing you want it to achieve?"
- Pickable: **more leads · more sales · more bookings/calls · sign-ups · look credible · fewer support
  requests · sell a specific product/service**.
- **Reconcile** with the Snapshot's primary conversion goal; see "Reconcile with the Snapshot" below.

### 3. What success looks like **[open]**
- "How would you *know* it's working? Is there a number you watch?" Chase a concrete metric: leads/month,
  sales, conversion %, booked calls, sign-ups, enquiries, average order value.
- If there genuinely isn't one, record **TBD**; never invent a target.

### 4. Biggest frustrations **[pick-many]**
- "What's the one or two things about the site that bug you most?" **Quote them verbatim** in the brief.

### 5. Audience, in their words **[open]**
- "Who is this really for, and what are they trying to do when they land?" Capture *their* framing even if
  the Snapshot already has an inferred audience; a gap between the two is itself useful signal.

### 6. References they admire **[open]**
- "Whose website do you look at and think 'I want that'? What do you like about it?" Note 1–3 sites + the *why*.

### 7. Appetite & constraints **[pick-1]** (appetite) + **[open]** (off-limits)
- "How much appetite do you have for changes right now?" Pickable: **a quick afternoon · a few days · a
  proper project/redesign**.
- "Anything off-limits?" Watch for: brand/logo locked, can't change platform, don't touch page X, redesign already
  underway, legal/compliance limits.

### 8. History & wishlist **[open]** *(optional, light)*
- "Changed anything on the site recently, or tried something that didn't work?"
- "If the site could do one new thing, what would it be?"

---

## Deeper questions (ask as far as the owner will go)

These sharpen the closing advice. Ask a couple at a time; stop when their energy dips; mark skipped ones
**TBD**. A quick brief covers the Core eight; a full brief works through most of these too.

### 9. Current results baseline **[open]**
- "Roughly how many enquiries/sales does the site bring you now, and how good is the quality?" Gives the
  target a starting point ("from ~3 a month to ~10").

### 10. Traffic sources **[pick-many]**
- "Where do visitors come from today: search, ads, referrals, social, word of mouth?" Even rough. Tells you
  which lever actually moves the goal (more traffic vs. better conversion).

### 11. Why clients really choose them **[open]**
- "When someone picks you over a competitor, what's the real reason?" The true differentiator in their words,
  not the tagline. This is gold for the messaging advice.

### 12. Biggest objection **[open]**
- "What's the doubt or question people raise most before they buy or commit?" Points straight at trust/proof
  advice.

### 13. Money pages **[open]**
- "Which pages, products, or services matter most commercially?" Focuses the effort where revenue is.

### 14. Marketing in flight **[pick-many]**
- "What's running right now that the site needs to support: ads, content/SEO, email, events, outbound?"

### 15. Brand & assets **[pick-many]**
- "Do you have brand guidelines, a logo, decent photography, or is a rebrand underway?" Sizes the design
  advice and respects locked brand.

### 16. Budget & timeline **[open]**
- "Roughly what budget band and timeline are you thinking? Any hard deadline: a launch, a campaign, a show?"

### 17. Who decides **[pick-1]**
- "Who signs off on changes: you, a marketing lead, a committee?" Shapes how the advice should be pitched.

### 18. The competitor to beat **[open]**
- "Is there one rival or example site you'd love to outclass? What do they do well?"

### 19. Anything we missed **[open]**
- "What haven't I asked that matters for this site?" Always end here. It's where owners volunteer the thing no fixed question would surface. Quote it verbatim.

---

## Building the diagnostic (the part that makes this worth reading)

A transcript of the answers is low value. The deliverable's centre of gravity is the **"Stated vs. observed"
reality-check**: each belief the owner holds, set against what the fetched page and the finished parallel
scans actually show, with **the gap** named. This is possible precisely because the interview runs while the
scans render. By the time the owner stops talking, the data is in.

### 1. "Stated vs. observed" reality-check
One row per belief: **you said → what we see → the gap.**
- **"You said"**: the owner's answer (goal, satisfaction, frustration, audience, appetite).
- **"What we see"**, grounded in fact: the fetched page (hero, copy, CTA, proof, structure) or a **real
  measured number** from a scan (LCP, security headers, axe violations, tokens, tracking). Never invent one.
- **"The gap"**: the insight the owner couldn't get from a form. Favour rows where belief and reality
  *disagree*; confirm the ones that agree, briefly.

Worked examples:
- *Goal "look credible"* → *scan: LCP 10.8 s, 6 MB, no security headers* → *your #1 credibility killer is
  technical, not visual: a 10-second load reads as amateur before the design is even seen.*
- *"The message isn't sharp"* → *H1 is a slogan; services all generic; portfolio anonymised* → *confirmed,
  and it's a copy fix: name what you do + who for, and name the clients.*
- *Satisfaction "okay"* → *the measured foundation grades poorly* → *the self-rating is generous.*

### 2. Tensions
List where the **goal, the constraints and the data conflict**, and resolve each. For example: *"you want 'wow' but
have only a few days and want to keep the design."* Often the constraint and the goal turn out compatible
(the credibility levers are all few-days fixes); say so, which is useful too.

### 3. "How to reach your goal" — prioritised advice
3–6 **opinionated, ordered** recommendations (highest leverage toward the stated goal first). Each: a short
imperative headline, one or two sentences of why/how tied to a belief + its gap (cite the real number where
one exists), and a `→` pointer to the analysis that will detail it. No letter grades, no IIF finding IDs, no
Impact/Effort scoring. That's the analyses and the Action Report; this orients them.

**Reconcile the goal with the Snapshot** as part of the reality-check: if the owner's stated goal differs
from the Snapshot's primary conversion, surface the mismatch, settle on the one commercial goal, and note
it (the Action Report backfills the Snapshot's open items later).

---

## Reconcile with the Snapshot

The audit is scored against **one** primary goal. If the owner's stated goal here differs from the primary
conversion captured in the Site Snapshot:

1. Surface the mismatch plainly ("the site pushes newsletter sign-ups, but you're telling me sales matter
   most, so which should the audit judge against?").
2. Settle on the single goal the owner cares about commercially.
3. Note the resolution in the brief, and treat that as the anchor the analyses use. If the Snapshot was
   already delivered, its open items are backfilled in the Action Report's reconciliation pass.

---

## Output file format

### File 1: `goals.md` (Markdown)

```markdown
# Goals & Discovery — [Site name]
*[One-line framing, e.g. "What the owner wants the site to achieve, in their words."]*
Date: [date]
Model: Ananas-Agency Website Audit intake
URL(s): [audited URLs]

## Owner brief (what they told us)
*Compressed — the answers, not the main event. The owner's own view, not the audit's grade.*
- **Satisfaction:** [very happy / okay / frustrated] — "[owner quote]"
- **The one goal:** [the single most important outcome] · **Success:** [how they'd know] — Target: [number or **TBD**]
- **Biggest frustration:** "[owner quote]"
- **Audience:** [who it's for, in their words]
- **Appetite & constraints:** [afternoon / few days / project] · off-limits: [brand / platform / none]
- **Deeper (as captured):** references [...] · differentiator [...] · objection [...] · competitor [...] *(or TBD)*

## Stated vs. observed (the reality-check)
*Each belief, held against the fetched page + the parallel scans — grounded in real numbers, never invented.*

| You said | What the page + scans show | The gap |
|----------|----------------------------|---------|
| Goal: [...] | [observed fact / measured number] | [the insight] |
| "[frustration]" | [what the page shows] | [confirm / pinpoint] |
| Satisfaction: [...] | [measured foundation] | [reality check] |
| Audience: [...] | [does the copy speak to them?] | [match / mismatch] |

## Tensions
- [goal vs. constraint vs. data conflict] → [resolution — often compatible, say so]

## How to reach your goal (prioritised)
*Ordered by leverage toward [the goal] — the analyses verify and quantify each.*
1. **[Imperative headline]** — [why/how tied to a gap; cite the real number]. → [Analysis]
2. **[Imperative headline]** — [...]. → [Analysis]
3. **[Imperative headline]** — [...]. → [Analysis]
[... 3–6, highest-leverage first ...]

## How this shapes the audit
- The analyses are read against **[the one goal]**; recommendations sized to **[appetite]**, respecting **[constraints]**.

## Next step
Run any of the five analyses (Messaging, Conversion, SEO, UX & Technical, Design & Visual) and paste this
brief with the Site Snapshot when asked about the site.
```

### File 2: `goals.html` (styled, share-ready)

A single **self-contained** `.html` file (all CSS inline in one `<style>` block, **no external assets and
no JavaScript**), so it opens in any browser, prints cleanly to PDF, and emails as one file. Render the
**same content** as the Markdown version. Keep the `<style>` block **identical to the shared design system**
(reproduced in full below). Every skill in this suite uses this exact block so all deliverables share one
look. Only these differ per skill: the `<title>`, the header, and the `utm_content=goals-discovery` in the
two brand links.

- Lead with the **diagnosis**, keep the answers compact. One `<section class="block">` per heading, in this
  order: **Owner brief** (compressed), **Stated vs. observed** (the reality-check), **Tensions**,
  **How to reach your goal** (prioritised advice), How this shapes the audit, Next step.
- **Owner brief:** a few `.row`s (satisfaction, goal + success, frustration, audience, appetite/constraints,
  deeper-as-captured). Compact; put owner quotes in `<blockquote>`. Label it "the owner's own view".
- **Stated vs. observed**, a `<table>` with three columns: **You said · What the page + scans show · The
  gap**. One row per belief; the "observed" cell cites a real measured number or a page fact. This is the
  visual centre of gravity; give it the most weight.
- **Tensions**, `.row`s: the conflict → its resolution.
- **How to reach your goal**, render **each advice item as an `article.card`**: a bold imperative headline in
  `.card h3`, one or two sentences of why/how in a `.row` (cite the real number), and a `→ [Analysis]`
  pointer linking that analysis's page. Order by leverage; number them.
- **No grade chip and no IIF finding cards:** this is the orienting diagnosis, not the graded analysis.

**Navigation & hints (required in every generated `.html`):**
- **Cross-link every reference to another deliverable** (see [report-format.md](../../../report-format.md) for
  canonical filenames: `site-snapshot.html`, `messaging.html`, `conversion.html`, `seo.html`,
  `ux-technical.html`, `design.html`, `action-report.html`). Any finding ID cited links to that dimension's
  page with a tooltip.
- **Hover hints on short terms, every occurrence, not just the first.** Give a `title` tooltip to every
  appearance of the shorthand set: **IIF, CRO, SEO, UX, CTA, the ID prefixes (MSG/CRO/SEO/UX/DSN), and the
  quadrant labels (quick win / big bet / fill-in / skip)**, e.g.
  `<abbr title="Issue · Impact · Fix — the finding format">IIF</abbr>`.
- **No Previous / Next buttons in this file.** Don't add a `pagenav` mid-session. End with the Print hint.
  The walk is wired only in the final pack (see report-format.md, "Final consistency pass").
- **Print hint (no JavaScript).** End the page with
  `<p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>`.

Full page (reproduce the shared `<style>` block verbatim; it is identical suite-wide; only the `<title>`,
header, and `utm_content` change):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Goals &amp; Discovery — [Site name]</title>
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
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=goals-discovery" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=goals-discovery" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>Goals &amp; Discovery — [Site name]</h1>
    <p class="tagline">What the owner wants — held against what the site actually shows.</p>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit intake &nbsp;·&nbsp; <b>URL:</b> [url]</div>
  </header>

  <section class="block">
    <h2 class="section">Owner brief</h2>
    <p class="verdict-common">The owner's own view (not the audit's grade) — compressed; the reality-check below is the main event.</p>
    <div class="row"><span class="k">Satisfaction</span>[very happy / okay / frustrated]</div>
    <div class="row"><span class="k">The one goal</span>[the single most important outcome] &nbsp;·&nbsp; <span class="k">Success</span>[how they'd know] — Target: [number or TBD]</div>
    <div class="row"><span class="k">Audience</span>[who it's for, in their words]</div>
    <div class="row"><span class="k">Appetite &amp; constraints</span>[afternoon / few days / project] · off-limits: [brand / platform / none]</div>
    <div class="row"><span class="k">Deeper (as captured)</span>differentiator [...] · objection [...] · references [...] · competitor [...] <i>(or TBD)</i></div>
    <blockquote>"[owner quote — the frustration, in their words]"</blockquote>
  </section>

  <section class="block">
    <h2 class="section">Stated vs. observed</h2>
    <p class="verdict-common">Each belief, held against the fetched page + the parallel scans — grounded in real numbers, never invented.</p>
    <div class="tablewrap"><table>
      <tr><th>You said</th><th>What the page + scans show</th><th>The gap</th></tr>
      <tr><td>Goal: [...]</td><td>[observed fact / measured number]</td><td>[the insight]</td></tr>
      <tr><td>"[frustration]"</td><td>[what the page shows]</td><td>[confirm / pinpoint]</td></tr>
      <tr><td>Satisfaction: [...]</td><td>[measured foundation]</td><td>[reality check]</td></tr>
      <tr><td>Audience: [...]</td><td>[does the copy speak to them?]</td><td>[match / mismatch]</td></tr>
    </table></div>
  </section>

  <section class="block">
    <h2 class="section">Tensions</h2>
    <div class="row">[goal vs. constraint vs. data conflict] → <b>[resolution — often compatible, say so]</b></div>
  </section>

  <section class="block">
    <h2 class="section">How to reach your goal</h2>
    <p class="verdict-common">Prioritised — highest leverage toward [the goal] first. The analyses verify and quantify each.</p>
    <article class="card">
      <h3>[Imperative headline]</h3>
      <div class="row">[Why/how, tied to a gap; cite the real number.] → <a href="ux-technical.html">UX &amp; Technical</a></div>
    </article>
    <!-- ...3–6 advice cards, highest-leverage first; each → the analysis that details it... -->
  </section>

  <section class="block">
    <h2 class="section">How this shapes the audit</h2>
    <div class="row">The analyses are read against <b>[the one goal]</b>; recommendations are sized to <b>[appetite]</b> and respect <b>[constraints]</b>.</div>
  </section>

  <section class="block">
    <h2 class="section">Next step</h2>
    <div class="row">Run any of the five analyses (<a href="messaging.html">Messaging</a>, <a href="conversion.html">Conversion</a>, <a href="seo.html">SEO</a>, <a href="ux-technical.html">UX &amp; Technical</a>, <a href="design.html">Design &amp; Visual</a>) and paste this brief with the <a href="site-snapshot.html">Site Snapshot</a> when asked about the site.</div>
  </section>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=goals-discovery" target="_blank" rel="noopener">
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
