# SEO & Content Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
adds the SEO-specific tests, the scoring rubric, worked finding examples, and the HTML output format.

> **Honesty rule (on-page only).** This skill analyses the **observable, on-page SEO** in the HTML you
> fetched: titles, meta tags, headings, alt text, URLs, links, schema, canonical, robots, viewport, plus
> the site-wide sweep + local structured-data validation from `seo-sweep.py`. Live search performance
> (rankings, search volume, backlinks, organic traffic, whether a page is actually indexed) is the owner's
> own search data and is **out of scope** for this suite: never state or estimate any of it. The grade is an
> expert judgement of on-page SEO, not a ranking measurement.

## The SEO tests

Run these fast before the full rubric; they surface the biggest issues quickly.

### The SERP-preview test
A **SERP** is a search engine results page: the list of blue links Google shows. Write the page's
`<title>` and `<meta name="description">` out exactly as they'd appear there:

> **Title line** (the blue clickable link, ~50–60 characters before Google truncates it)
> yoursite.com › page-url
> Grey description line (~150–160 characters before it's cut off)

Now judge it as a searcher would: is the title descriptive and specific, or is it "Home", blank, or the
same on every page? Does the description invite the click, or is it missing (so Google prints a random
sentence from the page)? If the preview reads badly or is duplicated across pages, that's a high-impact
finding: this is the site's advert on the results page.

### The search-intent match test
Take the term a page is trying to rank for (from its title, H1, and topic). If a real person from the
audience searched that term, what did they *want*: to buy, to compare, to learn how, to find a local
supplier? Does **this page** satisfy that intent, or is there a mismatch (a blog post ranking for a
"buy" query, a thin page ranking for a "how-to", a service the page never actually explains)? A page that
attracts the click but not the intent gets the bounce, an intent finding.

### The one-H1 test
The **H1** is the page's single main on-page heading (not the same as the browser-tab title). Check the
heading outline: is there **exactly one** H1, and does it state the page topic in the words the audience
uses? Zero H1s (common when the logo or a decorative banner is the top heading), several competing H1s,
or an H1 that says "Home" or a slogan with no keyword: each is a structure finding.

### The findability / indexability test
Can search engines reach and trust the page at all? Quick observable checks: is the URL `https://`; does
the `robots` meta or a visible `noindex` block it; is there a `<link rel="canonical">` pointing somewhere
sensible; is there a `viewport` meta (mobile-friendliness signal); does an XML sitemap appear to exist
(`/sitemap.xml`, or linked in `robots.txt`)? Anything blocking or missing here is a findability finding.
(Whether Google has *actually* indexed the page is the owner's search data, out of scope; judge the
on-page indexability signals only.)

---

## Site-wide quick SEO sweep (the secondary pages)

The homepage gets the full analysis above. For the **secondary pages** (services, products, case
studies, articles, about), run the bundled **static** crawler instead of hand-auditing each:

```
python scripts/seo-sweep.py <homepage-URL> --per-type 5 --out <folder>
```

It discovers URLs from the homepage nav and the sitemap (`sitemap_index.xml` / `sitemap.xml` /
`wp-sitemap.xml`), classifies them by URL path (services / products / case-studies / articles / about),
caps to `--per-type` per class (default 5), fetches each page **statically** (no browser), and writes a
compact `seo-sweep.md` table + `seo-sweep.json`. Pure standard library, no installs.

**What it records per page**, and the thresholds it flags on:

| Column | Flags when… |
|--------|-------------|
| Title (length) | missing, or outside **30–60 chars** |
| Meta description (length) | missing, or outside **70–160 chars** |
| H1 count | not exactly **1** |
| Canonical | missing `<link rel="canonical">` |
| Indexable | `noindex` present → **NOINDEX** (page hidden from Google) |
| Words | under **300** → thin content |
| Alt coverage | any `<img>` without `alt` |
| Open Graph | og:title missing or generic ("Home") |
| Schema | no JSON-LD block |
| H1/title alignment | the H1 and title share no keywords → "mismatch" |

It also rolls up **site-wide patterns**: duplicate titles across pages, how many pages miss a meta
description, which pages are thin, which lack a canonical.

**Turn it into findings, not noise.** Summarise the table into **a few site-wide `SEO-` findings**, one
per pattern, not one per page. Good sweep-driven findings read like:
- *"9 of 15 secondary pages have titles under 30 characters (e.g. `/case-studies/power-bi/` at 8 chars);
  they waste the strongest on-page ranking signal."* → Impact 3, Effort 3 (templated fix), big bet.
- *"The homepage title is duplicated on N pages, so Google can't tell them apart."* → Impact 3.
- *"`/case-studies/ms-fabric/` has an all-but-empty title (9 chars) and meta description (9 chars)."*

Keep the **full table in the deliverable** (a `Site-wide SEO sweep` section) as the evidence behind those
findings. If the tool can't run (no Python), spot-check 2–3 pages by hand and say the sweep was not run.

---

## Scoring rubric (weights sum to 100)

Rate each criterion **Pass** (full weight), **Partial** (half), or **Fail** (0). Sum → 0–100 → letter
grade. Always show this table in the deliverable so the grade is explainable.

| # | Criterion | What "Pass" looks like | Weight |
|---|-----------|------------------------|:------:|
| 1 | **Title tags** | Every page has a unique, descriptive `<title>` ~50–60 chars, leading with the topic/keyword, not "Home" or a duplicate. | 12 |
| 2 | **Meta descriptions** | Each key page has a present, compelling `<meta name="description">` ~150–160 chars that earns the click. | 8 |
| 3 | **Heading structure** | Exactly one H1 stating the page topic; a logical H2/H3 hierarchy; key terms used in headings. | 10 |
| 4 | **Keyword & search-intent match** | Pages target terms the audience actually searches, and the content matches the intent behind them. | 12 |
| 5 | **Content depth & usefulness** | Pages answer the visitor's real questions with substance; not thin, boilerplate, or duplicated. | 12 |
| 6 | **URL structure** | URLs are readable, descriptive, lowercase and hyphenated; not `?p=123` parameter soup. | 6 |
| 7 | **Image optimization** | Meaningful images carry descriptive `alt` text and sensible filenames; not decorative-only alt or huge files. | 8 |
| 8 | **Internal linking** | Key pages are linked from other pages with descriptive anchor text; no orphaned pages, no "click here". | 8 |
| 9 | **Structured data / schema** | Relevant schema is present (Organization, Product, FAQ, LocalBusiness, Article) so Google can show rich results. | 8 |
| 10 | **Indexability basics** | HTTPS; `robots` not blocking; an XML sitemap; sensible `canonical` tags; a mobile `viewport`. | 10 |
| 11 | **Content gaps** | The pages/topics the audience needs exist (FAQ, pricing, comparison, use-cases) — no obvious missing content. | 6 |

> A criterion can generate **more than one finding** (e.g. two different pages with missing meta
> descriptions), but score the criterion once overall. Findings are the fix list; the rubric is the grade.

Grade bands (from report-format.md): A 90–100 · B 80–89 · C 70–79 · D 60–69 · F 0–59.

---

## Worked finding examples (Issue · Impact · Fix)

**SEO-01 — Homepage `<title>` is just "Home"** · Impact 4 · Effort 1 · **quick win**
- **Issue:** The homepage title tag reads *"Home"*. The title is the blue clickable line on Google and
  the browser-tab label; this one says nothing about what the business does or for whom.
- **Impact:** On the results page (the SERP), a searcher sees "Home" and has no reason to click, so the
  site loses the click even when it ranks. It also throws away the single strongest on-page keyword signal.
- **Fix:** Write a unique, descriptive title ~50–60 characters leading with the offer and audience, e.g.
  *"Bookkeeping for tradespeople — Sorted in an hour a week"*. Give every page its own distinct title.
- **Evidence:** `<title>Home</title>`

**SEO-02 — Content doesn't match search intent** · Impact 4 · Effort 3 · **big bet**
- **Issue:** The page targeting *"emergency plumber Leeds"* is a 90-word "About our team" blurb with no
  service area, no call-out response time, and no booking path. The intent behind that search is "get help
  now"; the page answers a different question.
- **Impact:** Visitors who do land bounce straight back to Google (a "get help now" searcher won't read a
  team bio), and the mismatch tells Google the page is a weak answer for that query.
- **Fix:** Rebuild the page around the intent: 24/7 availability, the areas covered, typical response time,
  a phone CTA above the fold, and FAQ-style answers to what an emergency caller asks.

**SEO-03 — Meaningful images have no alt text** · Impact 3 · Effort 2 · **fill-in**
- **Issue:** All six product photos use empty or filename alt text, e.g. `alt=""` and
  `alt="IMG_4821.jpg"`. Alt text is the words search engines (and screen readers) read in place of an
  image.
- **Impact:** The site is invisible in Google Images for these products, and the page loses the extra
  keyword and accessibility signal the alt text would carry.
- **Fix:** Write descriptive alt for each meaningful image, e.g. `alt="Oak dining table seating six,
  natural finish"`; keep purely decorative images as `alt=""`. Rename files to describe the content
  (`oak-dining-table.jpg`).
- **Evidence:** `<img src="IMG_4821.jpg" alt="">`

**Strength worth noting** (not a finding, but record it): "Every service page carries valid LocalBusiness
schema with address, opening hours, and phone: a strong, correctly-implemented rich-result signal."

### Anti-patterns to catch (each becomes a finding)
- **Duplicate or blank titles:** the same `<title>` on every page, or missing titles.
- **"Home" / brand-only titles:** a title that names nothing the audience searches for.
- **Missing meta descriptions:** no `<meta name="description">`, so Google prints a random page snippet.
- **Multiple or zero H1s:** no clear main heading, or several competing ones.
- **Keyword stuffing:** the same term jammed unnaturally into titles, headings, and body copy.
- **Thin or duplicate content:** pages of a few boilerplate lines, or near-identical location/service pages.
- **"Click here" anchors:** links whose anchor text carries no meaning ("click here", "read more", "this").
- **No alt text:** meaningful images with empty or filename `alt`.
- **No structured data:** no schema at all where Product/FAQ/LocalBusiness/Article clearly applies.
- **Blocked by robots:** a `noindex` meta or robots rule keeping a page (that should rank) out of search.
- **Non-descriptive URLs:** `?p=123`, `/page-2`, uppercase or parameter-soup URLs instead of readable slugs.

---

## Output file format

### File 1: `seo.md` (Markdown)

```markdown
# SEO & Content — [Site name]
Date: [date]
Model: Ananas-Agency Website Audit
Audience searched for: [who searches, and the kind of terms they'd use]

## Grade: [A–F] ([score]/100)
[one-line verdict, e.g. "Weak — titles are duplicated, most pages have no meta description, and the service pages read as thin."]

### Scorecard
| # | Criterion | Pass/Partial/Fail | Weight | Points |
|---|-----------|-------------------|:------:|:------:|
| 1 | Title tags | Fail | 12 | 0 |
| ... | ... | ... | ... | ... |
| | **Total** | | **100** | **[score]** |

## Findings
### SEO-01. [short title] — Impact [1–5] · Effort [1–5] · [quick win/big bet/fill-in/skip]
- **Issue:** [I, with evidence]
- **Impact:** [what it costs]
- **Fix:** [F, concrete]
> "[quoted tag / heading / URL / copy as evidence]"

[... further findings, impact order ...]

## Site-wide SEO sweep (secondary pages)
[The `seo-sweep.py` table — one row per swept page — as evidence behind the site-wide findings above.]

| Page | Type | Title (len) | Desc (len) | H1 | Words | Alt | Schema | Flags |
|------|------|:-----------:|:----------:|:--:|:-----:|:---:|:------:|-------|
| /services/… | services | 39 | 160 | 1 | 714 | 12/12 | 2 | H1/title mismatch |
| ... | | | | | | | | |

*Homepage is audited in full above; this table is the quick per-page sweep of the sampled secondary pages.*

## What's working
- [1–3 genuine strengths]

## Out of scope (owner's search data)
- Live rankings, impressions, index status, search volume, backlinks, and organic traffic are the owner's
  own search data — not measured or estimated here. The bundled sweep samples ~5 pages/type; site-wide tags,
  duplicates, and **structured-data validity** are measured on that sample plus the homepage. (Broken links
  across the key pages are measured separately by `interaction-scan.py`.)

## Summary
- Findings: [n] ([x] quick wins, [y] big bets, ...)
- Top priority: [SEO-ID — one line]
```

### File 2: `seo.html` (styled, share-ready)

A single **self-contained** `.html` file (all CSS inline in one `<style>` block, **no external assets and
no JavaScript**). Use the **shared design system**: the exact `<style>` block and page frame from
[rules-snapshot.md](../../../0%20Site%20Snapshot/site-snapshot/references/rules-snapshot.md), reproduced
in full below so this skill is self-contained. Only these differ from the snapshot page: the `<title>`,
the header, the `utm_content=seo-content` in the two brand links, and the section content.

Components:
- **A grade section first:** the letter grade in a `.grade` chip (class `a`/`b`/`c`/`d`/`f`), the score,
  a one-line verdict, and the **scorecard `<table>`** (criteria × pass/partial/fail × weight × points).
- **A Findings section:** one `.card` per finding. Card header: the `.id` chip (`SEO-01`), the short
  title, an **Impact meter** (`<span class="scorewrap"><span class="meter"><i style="width:NN%"></i></span><span class="scoreno">Impact X/5</span></span>`,
  width = Impact/5×100), and the **priority `.tag`** (`quickwin` / `bigbet` / `fillin` / `skip`). Body:
  Issue / Impact / Fix as `.row`s (append `· Effort X/5` in the Impact row via `<span class="effort">`),
  and the quoted evidence in a `<blockquote>`.
- **A "Site-wide SEO sweep" section:** the `seo-sweep.py` per-page table as a `<table>` (Page, Type,
  Title len, Desc len, H1, Words, Alt, Schema, Flags), one row per swept page, above a one-line note that
  the homepage is audited in full and this is the quick sweep of the sampled secondary pages. Include the
  **structured-data validation** result (homepage + any per-page schema issues) beneath it.
- **A "What's working" section:** `.row`s or `ul.clean` of strengths.
- **An "Out of scope" note:** a one-line `ul.clean` that live rankings, traffic, and index status are the
  owner's own search data, not measured here (never invent rankings, traffic, or search-volume numbers, and
  name no third-party tool).
- **A Summary section:** findings count and the top priority (cited by ID).

**Navigation & hints (required):** cross-link other deliverables and tooltip every ID and shorthand term
(IIF, CRO, SEO, UX, CTA, MSG/CRO/SEO/UX, quadrant labels), every occurrence, per
[report-format.md](../../../report-format.md). **No `pagenav`** mid-session; end with the Print hint.

Finding card pattern:
```html
<article class="card">
  <h3><span class="id">SEO-01</span> Homepage title is just "Home"
      <span class="scorewrap"><span class="meter"><i style="width:80%"></i></span><span class="scoreno">Impact 4/5</span></span>
      <span class="tag quickwin">quick win</span></h3>
  <div class="row"><span class="k">Issue</span>The homepage title tag reads "Home" — it says nothing about what the business does or for whom.</div>
  <div class="row"><span class="k">Impact</span>On the results page a searcher has no reason to click, and the strongest on-page keyword signal is wasted. <span class="effort">· Effort 1/5</span></div>
  <div class="row"><span class="k">Fix</span>Write a unique, descriptive title ~50–60 characters leading with the offer and audience; give every page its own.</div>
  <blockquote>"&lt;title&gt;Home&lt;/title&gt;"</blockquote>
</article>
```

Full page (reproduce the shared `<style>` block verbatim; it is identical suite-wide):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SEO &amp; Content — [Site name]</title>
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
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=seo-content" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=seo-content" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>SEO &amp; Content — [Site name]</h1>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit &nbsp;·&nbsp; <b>Grade:</b> [A–F] ([score]/100)</div>
  </header>

  <section class="block">
    <h2 class="section"><span class="no">1</span> Grade &amp; scorecard</h2>
    <div class="row"><span class="grade d">D</span> <b>64/100</b> — [one-line verdict]</div>
    <div class="tablewrap"><table>
      <tr><th>#</th><th>Criterion</th><th>Result</th><th>Weight</th><th>Points</th></tr>
      <tr><td>1</td><td>Title tags</td><td>Fail</td><td>12</td><td>0</td></tr>
      <!-- one row per criterion -->
      <tr><td></td><td><b>Total</b></td><td></td><td><b>100</b></td><td><b>64</b></td></tr>
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
    <h2 class="section"><span class="no">4</span> Out of scope (owner's search data)</h2>
    <ul class="clean">
      <li>Live <b>rankings, impressions, index status, search volume, backlinks &amp; organic traffic</b> are the owner's own search data — not measured or estimated here.</li>
      <li><span class="verdict-common">On-page tags, duplicates &amp; structured-data validity are measured on the homepage + ~5 pages/type (see the Site-wide SEO sweep); broken links are measured by the interaction scan.</span></li>
    </ul>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">5</span> Summary</h2>
    <div class="row"><span class="k">Findings</span>[n] ([x] quick wins, [y] big bets, …)</div>
    <div class="row"><span class="k">Top priority</span>[SEO-ID — one line]</div>
  </section>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=seo-content" target="_blank" rel="noopener">
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
