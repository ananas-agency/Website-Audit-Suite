# Messaging & Clarity Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
adds the messaging-specific tests, the scoring rubric, worked finding examples, and the HTML output format.

## The clarity tests

Run these fast before the full rubric. They surface the biggest issues quickly.

### The 5-second test
From the hero (the first screen, before scrolling) alone, could a first-time visitor answer:
1. **What is this?** (what's offered)
2. **Who is it for?**
3. **What can I do next?** (the primary action)

If any answer is missing or ambiguous, that's a high-impact finding.

### The "so what?" test
Read the headline. Does it promise a **benefit or outcome the visitor cares about**, or does it just name
the company/product or state a feature? "The invoicing app for freelancers who hate admin" passes;
"Welcome to Acme" or "Powerful. Flexible. Modern." fails.

### The "only you" test (differentiation)
Could a direct competitor paste their own name onto this exact copy and have it still fit? If yes, the
messaging says nothing distinctive: a differentiation finding.

### The jargon / customer-language test
Is the copy written in the **visitor's** words about **their** problem, or in the company's internal
language ("synergistic platform", "best-in-class solutions", "leverage our ecosystem")? Insider jargon
that the audience wouldn't use is a clarity finding.

---

## Scoring rubric (weights sum to 100)

Rate each criterion **Pass** (full weight), **Partial** (half), or **Fail** (0). Sum → 0–100 → letter
grade. Always show this table in the deliverable so the grade is explainable.

| # | Criterion | What "Pass" looks like | Weight |
|---|-----------|------------------------|:------:|
| 1 | **Above-the-fold clarity** | The 5-second test passes: what / who / next action are all obvious from the hero. | 15 |
| 2 | **Headline quality** | Specific and benefit-led; names the outcome or the audience, not just the brand. | 12 |
| 3 | **Supporting subhead** | One line under the headline that expands the promise and adds the "how/for whom". | 8 |
| 4 | **Primary CTA clarity** | One obvious, action-worded primary call to action, visible above the fold. | 10 |
| 5 | **Differentiation** | States why *this* over alternatives — passes the "only you" test. | 10 |
| 6 | **Proof / credibility** | Concrete proof near the claims: testimonials, client logos, numbers, guarantees, reviews. | 12 |
| 7 | **Customer language** | Speaks to the reader's problem in their words; no unexplained insider jargon. | 10 |
| 8 | **Benefit-led, scannable copy** | Benefits before features; skimmable headings/bullets, not walls of text. | 10 |
| 9 | **Cross-page consistency** | The hero promise is carried consistently across the key pages (no bait-and-switch). | 7 |
| 10 | **Objection handling** | Addresses the main hesitation (price, risk, effort, trust) somewhere on the path. | 6 |

> A criterion can generate **more than one finding** (e.g. two different jargon problems), but score the
> criterion once overall. Findings are the fix list; the rubric is the grade.

Grade bands (from report-format.md): A 90–100 · B 80–89 · C 70–79 · D 60–69 · F 0–59.

---

## Worked finding examples (Issue · Impact · Fix)

**MSG-01. Hero says nothing about what the site does** · Impact 5 · Effort 1 · **quick win**
- **Issue:** The homepage H1 reads *"Welcome — we're glad you're here."* Nothing on the first screen says
  what's sold or for whom.
- **Impact:** A first-time visitor fails the 5-second test and can't tell they're in the right place,
  the single biggest cause of bounce on the primary entry page.
- **Fix:** Replace with a benefit-led headline naming the offer and audience, e.g. *"Bookkeeping for
  tradespeople — your accounts sorted in an hour a week."* Add a one-line subhead on how it works.
- **Evidence:** `<h1>Welcome — we're glad you're here.</h1>`

**MSG-02. No differentiation; copy is interchangeable** · Impact 4 · Effort 3 · **big bet**
- **Issue:** Body copy is *"We deliver high-quality solutions with a customer-first approach."* Fails the
  "only you" test; any competitor could use it verbatim.
- **Impact:** Nothing tells the visitor why to pick this over the three other tabs they have open; the
  site competes on price by default.
- **Fix:** Replace generic claims with one concrete, ownable difference (a method, a guarantee, a niche
  focus, a number). Interview the owner for the real "why us" and lead with it.

**MSG-03. Feature dump, no benefits** · Impact 3 · Effort 2 · **fill-in**
- **Issue:** The product section lists *"OAuth 2.0, REST API, 99.9% uptime, multi-tenant architecture"*
  with no plain-language benefit.
- **Impact:** Non-technical buyers can't map features to what they *get*, so the value is lost on the
  people who sign the cheque.
- **Fix:** Pair each feature with its outcome, e.g. *"99.9% uptime — your store stays open even on Black
  Friday."*

**Strength worth noting** (not a finding, but record it): "Testimonials carry real names, companies, and a
specific result each — strong, credible proof."

### Anti-patterns to catch (each becomes a finding)
- **Generic hero:** "Welcome", "Your partner in X", "Solutions for a better tomorrow".
- **Brand-first headline:** leads with the company name instead of the visitor's outcome.
- **Adjective soup:** "innovative, dynamic, world-class" with nothing concrete.
- **Buried CTA:** no clear next action above the fold, or five competing CTAs of equal weight.
- **Claims without proof:** "trusted by thousands" with no logos, numbers, or testimonials.
- **We-we-we copy:** every sentence starts with "We…"; nothing about the reader.
- **Jargon wall:** insider terms the actual audience wouldn't use.
- **Inconsistent promise:** the ad/landing headline doesn't match what the page then talks about.

---

## Output file format

### File 1: `messaging.md` (Markdown)

```markdown
# Messaging & Clarity — [Site name]
Date: [date]
Model: Ananas-Agency Website Audit
Primary goal audited against: [the site's primary conversion]

## Grade: [A–F] ([score]/100)
[one-line verdict, e.g. "Fair — the offer is buried below the fold and the site reads like every competitor."]

### Scorecard
| # | Criterion | Pass/Partial/Fail | Weight | Points |
|---|-----------|-------------------|:------:|:------:|
| 1 | Above-the-fold clarity | Fail | 15 | 0 |
| ... | ... | ... | ... | ... |
| | **Total** | | **100** | **[score]** |

## Findings
### MSG-01. [short title] — Impact [1–5] · Effort [1–5] · [quick win/big bet/fill-in/skip]
- **Issue:** [I, with evidence]
- **Impact:** [what it costs]
- **Fix:** [F, concrete]
> "[quoted copy / element as evidence]"

[... further findings, impact order ...]

## What's working
- [1–3 genuine strengths]

## Summary
- Findings: [n] ([x] quick wins, [y] big bets, ...)
- Top priority: [MSG-ID — one line]
```

### File 2: `messaging.html` (styled, share-ready)

A single **self-contained** `.html` file (all CSS inline in one `<style>` block, **no external assets and
no JavaScript**). Use the **shared design system**: the exact `<style>` block and page frame from
[rules-snapshot.md](../../../0%20Site%20Snapshot/site-snapshot/references/rules-snapshot.md), reproduced
in full below so this skill is self-contained. Only these differ from the snapshot page: the `<title>`,
the header, the `utm_content=messaging-clarity` in the two brand links, and the section content.

Components:
- **A grade section first:** the letter grade in a `.grade` chip (class `a`/`b`/`c`/`d`/`f`), the score,
  a one-line verdict, and the **scorecard `<table>`** (criteria × pass/partial/fail × weight × points).
- **A Findings section:** one `.card` per finding. Card header: the `.id` chip (`MSG-01`), the short
  title, an **Impact meter** (`<span class="scorewrap"><span class="meter"><i style="width:NN%"></i></span><span class="scoreno">Impact X/5</span></span>`,
  width = Impact/5×100), and the **priority `.tag`** (`quickwin` / `bigbet` / `fillin` / `skip`). Body:
  Issue / Impact / Fix as `.row`s (append `· Effort X/5` in the Impact row via `<span class="effort">`),
  and the quoted evidence in a `<blockquote>`.
- **A "What's working" section:** `.row`s or `ul.clean` of strengths.
- **A Summary section:** findings count and the top priority (cited by ID).

**Navigation & hints (required):** cross-link other deliverables and tooltip every ID and shorthand term
(IIF, CRO, SEO, UX, CTA, MSG/CRO/SEO/UX, quadrant labels), every occurrence, per
[report-format.md](../../../report-format.md). **No `pagenav`** mid-session; end with the Print hint.

Finding card pattern:
```html
<article class="card">
  <h3><span class="id">MSG-01</span> Hero says nothing about what the site does
      <span class="scorewrap"><span class="meter"><i style="width:100%"></i></span><span class="scoreno">Impact 5/5</span></span>
      <span class="tag quickwin">quick win</span></h3>
  <div class="row"><span class="k">Issue</span>The homepage H1 reads "Welcome — we're glad you're here." Nothing says what's sold or for whom.</div>
  <div class="row"><span class="k">Impact</span>Visitors fail the 5-second test and bounce. <span class="effort">· Effort 1/5</span></div>
  <div class="row"><span class="k">Fix</span>Replace with a benefit-led headline naming the offer and audience, plus a one-line subhead.</div>
  <blockquote>"&lt;h1&gt;Welcome — we're glad you're here.&lt;/h1&gt;"</blockquote>
</article>
```

Full page (reproduce the shared `<style>` block verbatim; it is identical suite-wide):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Messaging &amp; Clarity — [Site name]</title>
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
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=messaging-clarity" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=messaging-clarity" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>Messaging &amp; Clarity — [Site name]</h1>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit &nbsp;·&nbsp; <b>Grade:</b> [A–F] ([score]/100)</div>
  </header>

  <section class="block">
    <h2 class="section"><span class="no">1</span> Grade &amp; scorecard</h2>
    <div class="row"><span class="grade c">C</span> <b>72/100</b> — [one-line verdict]</div>
    <div class="tablewrap"><table>
      <tr><th>#</th><th>Criterion</th><th>Result</th><th>Weight</th><th>Points</th></tr>
      <tr><td>1</td><td>Above-the-fold clarity</td><td>Fail</td><td>15</td><td>0</td></tr>
      <!-- one row per criterion -->
      <tr><td></td><td><b>Total</b></td><td></td><td><b>100</b></td><td><b>72</b></td></tr>
    </table></div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">2</span> Findings</h2>
    <!-- one .card per finding (see the finding card pattern above) -->
  </section>

  <section class="block">
    <h2 class="section"><span class="no">3</span> What's working</h2>
    <ul class="clean"><li>[genuine strength]</li></ul>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">4</span> Summary</h2>
    <div class="row"><span class="k">Findings</span>[n] ([x] quick wins, [y] big bets, …)</div>
    <div class="row"><span class="k">Top priority</span>[MSG-ID — one line]</div>
  </section>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=messaging-clarity" target="_blank" rel="noopener">
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
