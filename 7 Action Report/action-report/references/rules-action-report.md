# Action Report Rules — Detailed Reference

This skill synthesises the whole audit. The Finding format, Impact/Effort scales, priority quadrants,
grade bands, ID scheme, the consolidated-report spec, cross-linking rules, the final consistency pass, and
the bundle all live in [report-format.md](../../../report-format.md). This reference adds the synthesis method,
the matrix and roadmap layout, the phased plan, the one CTA block, and the HTML output format for both the
Action Report page and the consolidated report.

## Computing the overall grade

- Take each **completed** dimension's 0–100 score (Messaging, Conversion, SEO, UX/Technical).
- **Overall score = the mean of the completed dimension scores**, rounded to the nearest whole number.
- Map to a letter with the shared bands (A 90–100 · B 80–89 · C 70–79 · D 60–69 · F 0–59).
- If not all five ran, average only what exists and state plainly which dimensions are missing (e.g.
  "Overall C (74), from Messaging and SEO only; Conversion and UX/Technical not run").
- The grade is an **expert judgement**, not a measurement; say so.

## Normalising across dimensions

Before building the matrix, sanity-check that Impact and Effort mean the same thing across the five
analyses. An "Impact 5" in Conversion (kills the primary conversion) should be as serious as an "Impact 5"
in SEO (blocks the whole site from being indexed). If an outlier is mis-rated, adjust it and note the change
in the Action Report so the roadmap ordering is trustworthy.

## The Impact × Effort matrix

Place **every** finding from every dimension into one quadrant, by its Impact (High = 4–5, Low = 1–3) and
Effort (Low = 1–2, High = 3–5):

| | Low effort (1–2) | High effort (3–5) |
|---|---|---|
| **High impact (4–5)** | **Quick Win** — do first | **Big Bet** — plan & schedule |
| **Low impact (1–3)** | **Fill-in** — do when convenient | **Skip** — backlog |

List findings in each quadrant by ID, highest impact first. Every finding must appear in exactly one cell.

## The prioritised roadmap

A single ordered list the user can work top-down:
1. **Quick Wins:** impact descending (these are the first-two-weeks list).
2. **Big Bets:** impact descending (schedule these).
3. **Fill-ins:** do alongside the above when convenient.
4. **Skip:** listed as backlog, explicitly deprioritised (don't hide them; just mark them low value).

Each roadmap row: ID (linked + tooltipped), the one-line issue, the fix in brief, Impact, Effort, and the
dimension it came from.

## The phased plan

- **Your first two weeks:** the Quick Wins, as a checklist. Each item links to the finding's dimension page.
- **Days 30–60:** kick off the top Big Bets; start measuring against the site's **primary conversion goal**
  (recommend the user watch the relevant analytics, e.g. GA4 conversions, form completions).
- **Days 60–90:** finish the Big Bets, action the worthwhile Fill-ins, then **re-run the audit** to see the
  grades move.

## The agency CTA block (exactly one, here)

The Action Report closing is the **one** place in the whole pack with a direct call to action (mirroring the
restraint of the rest of the suite). Render a single `.ctablock`:

```html
<div class="ctablock">
  <div class="ctahead">Fresh eyes turned your site into a to-do list?</div>
  <div class="ctasub">We turn audits like this one into websites that actually convert.</div>
  <a class="ctabtn" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=action-report-cta" target="_blank" rel="noopener">Let's Grow Together</a>
</div>
```

No email in the block; the footer already carries juicy@ananas-agency.com. Keep the CTA to this page only.

---

## Output file format — the Action Report

### File 1: `action-report.md`

```markdown
# Website Audit — Action Report — [Site name]
Date: [date]
Model: Ananas-Agency Website Audit
Primary goal: [the site's primary conversion]

## Overall grade: [A–F] ([score]/100)
| Dimension | Grade | Score |
|-----------|:-----:|:-----:|
| Messaging & Clarity | C | 72 |
| Conversion (CRO) | D | 64 |
| SEO & Content | B | 81 |
| UX & Technical | C | 70 |
| Design & Visual | B | 82 |
| **Overall** | **C** | **74** |

## Executive summary
- **Biggest opportunity:** [ID — one line]
- **Top 3 quick wins:** [ID, ID, ID]
- **What's working:** [1–2 strengths]

## Priority matrix (Impact × Effort)
- **Quick Wins:** [IDs]
- **Big Bets:** [IDs]
- **Fill-ins:** [IDs]
- **Skip:** [IDs]

## Roadmap
| # | ID | Issue | Fix (brief) | Impact | Effort | From |
|---|----|-------|-------------|:------:|:------:|------|
| 1 | CRO-01 | 11-field contact form | Cut to 3 fields | 4 | 2 | Conversion |
| ... | | | | | | |

## Plan
### Your first two weeks
- [ ] [quick win — ID]
### Days 30–60
- [big bets + start measuring]
### Days 60–90
- [finish big bets, re-audit]
```

### File 2: `action-report.html` (styled, share-ready)

Self-contained, using the **shared design system** (full `<style>` block + page frame reproduced below,
identical suite-wide; only the `<title>`, header, and `utm_content=action-report` differ). Sections:

1. **Overall scorecard:** the overall `.grade` chip + score, and a `<table>` of the five dimensions
   (Dimension, Grade chip, Score), with the Overall row bold.
2. **Executive summary:** biggest opportunity (ID, linked+tooltipped), top 3 quick wins (IDs), what's
   working.
3. **Priority matrix:** the `.matrix` grid of four `.quad` cells (`qw` / `bb` / `fi` / `sk`), each listing
   its findings by ID as `<li>`s.
4. **Roadmap:** a `<table>` (# / ID / Issue / Fix / Impact / Effort / From).
5. **Plan:** the three phases as `.row`s / `ul.clean` checklists.
6. **The single `.ctablock`** (above), then the Print hint. **No `pagenav`** mid-session (the final pass
   adds it).

Cross-link and tooltip **every** finding ID (link to its dimension page: `MSG-`→`messaging.html`,
`CRO-`→`conversion.html`, `SEO-`→`seo.html`, `UX-`→`ux-technical.html`, `DSN-`→`design.html`) and every shorthand term (IIF, CRO,
SEO, UX, CTA, quadrant labels), every occurrence. See [report-format.md](../../../report-format.md).

Matrix component:
```html
<div class="matrix">
  <div class="quad qw"><h4><span class="dot"></span>Quick Wins — do first</h4>
    <ul><li><a href="conversion.html" title="CRO-01 — 11-field contact form">CRO-01</a> — cut the form to 3 fields</li></ul></div>
  <div class="quad bb"><h4><span class="dot"></span>Big Bets — plan &amp; schedule</h4><ul><li>…</li></ul></div>
  <div class="quad fi"><h4><span class="dot"></span>Fill-ins — when convenient</h4><ul><li>…</li></ul></div>
  <div class="quad sk"><h4><span class="dot"></span>Skip — backlog</h4><ul><li>…</li></ul></div>
</div>
```

Full page (reproduce the shared `<style>` block verbatim):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Website Audit — Action Report — [Site name]</title>
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
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=action-report" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=action-report" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>Website Audit — Action Report — [Site name]</h1>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit &nbsp;·&nbsp; <b>Overall:</b> [A–F] ([score]/100)</div>
  </header>

  <section class="block">
    <h2 class="section"><span class="no">1</span> Overall scorecard</h2>
    <div class="row"><span class="grade c">C</span> <b>72/100</b> — [one-line overall verdict]</div>
    <div class="tablewrap"><table>
      <tr><th>Dimension</th><th>Grade</th><th>Score</th></tr>
      <tr><td>Messaging &amp; Clarity</td><td><span class="grade c">C</span></td><td>72</td></tr>
      <tr><td>Conversion (<abbr title="Conversion Rate Optimisation">CRO</abbr>)</td><td><span class="grade d">D</span></td><td>64</td></tr>
      <tr><td>SEO &amp; Content</td><td><span class="grade b">B</span></td><td>81</td></tr>
      <tr><td>UX &amp; Technical</td><td><span class="grade c">C</span></td><td>70</td></tr>
      <tr><td>Design &amp; Visual</td><td><span class="grade b">B</span></td><td>82</td></tr>
      <tr><td><b>Overall</b></td><td><b><span class="grade c">C</span></b></td><td><b>72</b></td></tr>
    </table></div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">2</span> Executive summary</h2>
    <div class="row"><span class="k">Biggest opportunity</span>[ID linked+tooltipped — one line]</div>
    <div class="row"><span class="k">Top 3 quick wins</span>[ID, ID, ID]</div>
    <div class="row"><span class="k">What's working</span>[1–2 strengths]</div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">3</span> Priority matrix</h2>
    <!-- .matrix with four .quad cells (see the matrix component above) -->
  </section>

  <section class="block">
    <h2 class="section"><span class="no">4</span> Roadmap</h2>
    <div class="tablewrap"><table>
      <tr><th>#</th><th>ID</th><th>Issue</th><th>Fix</th><th>Impact</th><th>Effort</th><th>From</th></tr>
      <!-- one row per finding, quick wins first -->
    </table></div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">5</span> Plan</h2>
    <div class="row"><span class="k">Your first two weeks</span></div>
    <ul class="clean"><li>[quick win — linked ID]</li></ul>
    <div class="row"><span class="k">Days 30–60</span>[big bets + start measuring]</div>
    <div class="row"><span class="k">Days 60–90</span>[finish big bets, then re-audit]</div>
  </section>

  <div class="ctablock">
    <div class="ctahead">Fresh eyes turned your site into a to-do list?</div>
    <div class="ctasub">We turn audits like this one into websites that actually convert.</div>
    <a class="ctabtn" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=action-report-cta" target="_blank" rel="noopener">Let's Grow Together</a>
  </div>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=action-report" target="_blank" rel="noopener">
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

## Output file format — the consolidated Website Audit Report

The merged entry document **`_[site]-website-audit-report`** (`.md` + `.html`): the full spec is in
[report-format.md](../../../report-format.md); the essentials:

- **Header:** the site's own logo if one is available (header logo / `og:image` / user-provided), embedded
  as a **data URI** so the file stays self-contained; otherwise the site **name** as styled text. Never
  invent a logo. Attribution: "Website audit of [site], built with the Website Audit Suite by Ananas
  Agency."
- **Executive summary first** (unnumbered): overall grade + the five dimension grades, biggest opportunity,
  top 3 quick wins, what's working.
- **Then every section in fixed order, full-width, with real substance (not teasers):**
  1. **Site Snapshot:** the snapshot facts.
  2. **Messaging & Clarity:** grade + scorecard table + full `MSG-` findings list.
  3. **Conversion (CRO):** grade + scorecard + full `CRO-` findings.
  4. **SEO & Content:** grade + scorecard + full `SEO-` findings.
  5. **UX & Technical:** grade + scorecard + full `UX-` findings.
  6. **Design & Visual:** grade + scorecard + design tokens (palette/fonts/button count) + the desktop &amp; mobile renders + full `DSN-` findings.
  7. **Action Plan:** the matrix + roadmap + phased plan.
- Each section heading carries an **"Open full document →"** `.openbtn` linking to that skill's `.html`.
- Render each section's digest **full-width**: tables as bare `<table style="width:100%">`, text as `.row`s
  directly in the section; do **not** wrap a section in `.tablewrap` or `.card`.
- Uses the same `<style>` block and frame; use `utm_content=website-audit-report` in its brand links.
- End with the single agency `.ctablock` (if not already on the Action Report page you link to) and the
  Print hint. The final pass makes this the **entry** file of the walk (sorts first; no Previous; Next →
  `site-snapshot.html`).

---

## Final consistency pass & bundle

Do these last, per [report-format.md](../../../report-format.md):
- **Regenerate every `.html`** in sequence order, adding the `pagenav` Previous/Next walk
  (`_[site]-website-audit-report` → `site-snapshot` → `messaging` → `conversion` → `seo` → `ux-technical`
  → `design` → `action-report`), tooltipping every ID, ensuring hover hints on every shorthand term, wiring all
  cross-links, and **reconciling the Site Snapshot's `TBD`s** (backfill only what the session actually
  answered; never invent).
- **Bundle** everything flat into **`[site]-website-audit.zip`** with code execution: the merged report
  first by name, then every per-skill `.md` + `.html`. Offer it as the primary download. For partial runs,
  bundle only what exists and name the gaps.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
