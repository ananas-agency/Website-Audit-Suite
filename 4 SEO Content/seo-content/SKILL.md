---
name: seo-content
description: >
  Analyses a website's on-page SEO and content quality in the Ananas-Agency Website Audit Suite.
  Uses two-tier depth: the homepage gets a full in-depth analysis (title, meta, headings, keyword/intent,
  content, schema, indexability, gaps), and the secondary pages (services, products, case studies,
  articles, about) get a quick site-wide per-page SEO sweep — a cheap static crawl that tabulates each
  page's title/meta/H1/canonical/indexability/word-count/alt/schema and flags site-wide issues like
  duplicate or too-short titles and thin content. Produces graded findings in
  Issue · Impact · Fix format on an Impact × Effort priority scale, plus a 0–100 SEO grade. Use this
  skill when the user wants to: run an SEO audit, understand why their site isn't showing up on Google,
  check title tags / meta descriptions / headings, improve their rankings, or audit their content.
  Trigger: "SEO audit", "why isn't my site on Google", "meta tags", "improve my rankings", "title
  tags", "content audit", "keywords", "on-page SEO", "search engine optimization", "meta description".
---

# SEO & Content (Ananas-Agency — Website Audit)

## Goal

Judge how well the website can be **found in search and understood once found** (by both search engines
and the people typing queries), and turn every weakness into a prioritised, fixable **Finding**. Deliver
a graded SEO scorecard (0–100 → letter grade) and a list of `SEO-` findings in **Issue · Impact · Fix**
format, each rated on Impact and Effort so the user knows what to fix first.

This is **URL-first**: read the live pages and quote what's actually in them: the `<title>`, the meta
description, the headings, the alt text, the URLs, the schema. Written for **business owners and
marketers**, not SEO specialists, so explain the jargon in plain language (a *meta description* is the
grey summary line under a Google result; an *H1* is the page's main on-page heading; a *canonical* tells
Google which URL is the "real" one; *schema* is hidden code that helps Google show rich results), and tie
every finding to a real effect: fewer clicks, wrong page ranking, invisible to search.

## Inputs

- **Site Snapshot** (from Skill 0). Paste it if you have it; it anchors the analysis to the site's
  **audience** and **what they'd search for**, plus the page inventory. If it's missing, do a quick
  mini-snapshot first (fetch the homepage; establish name, what it does, audience, key pages) so your
  findings have an anchor, but don't run the full intake.
- **The URL(s)**: the homepage plus any key landing/product/content pages the user cares about.

## The core unit: a Finding (Issue · Impact · Fix)

Every observation is a Finding. See [report-format.md](../../report-format.md) for the full definition,
the Impact/Effort scales (1–5), and the priority quadrants (quick win / big bet / fill-in / skip). In
short:
- **Issue**: the specific SEO or content problem, with the **actual tag, heading, URL, or copy quoted**
  as evidence.
- **Impact**: what it costs (the page can't be found, loses the click on the results page, ranks for the
  wrong intent, reads as thin). Rated **Impact 1–5**.
- **Fix**: the concrete change, ideally with an example (the rewritten title, the H1 to use, the schema
  to add).
- **Effort 1–5** and a **priority quadrant** derived from Impact × Effort.

Give each finding an ID: `SEO-01`, `SEO-02`, … in impact order.

## Conversation flow

> **Two-tier depth (how deep to go where).** The **homepage** is the main page: give it the **full,
> in-depth** analysis below (every rubric criterion, quoted evidence, the full finding treatment). The
> **secondary pages** (services, products, case studies, articles, about) don't each need the full
> workup; they get a **quick per-page SEO sweep** (Step 2b) that tabulates the on-page SEO signals across
> them and surfaces site-wide patterns. This keeps coverage broad without auditing 25 pages by hand.

### Step 1: Load context and fetch the homepage (full depth)

Take the Site Snapshot (or build the mini one) and **fetch the homepage**. This is the page you analyse
in full. Read the raw HTML, not just the rendered text: the `<title>`, `<meta name="description">`, the
heading outline (H1/H2/H3), the image `alt` attributes, the on-page links and their anchor text, the URL,
any `<script type="application/ld+json">` schema, the `<link rel="canonical">`, `robots` meta, and the
viewport tag. Keep the site's **audience** in mind. SEO is always "findable *by whom, searching for
what*".

### Step 2: Run the SEO tests

Apply the fast diagnostic tests before the full rubric. Details and examples in
[references/rules-seo.md](references/rules-seo.md):
- **The SERP-preview test**: write the title + meta description out as they'd appear in a Google result.
  Do they read well and earn the click, or are they blank, truncated, or duplicated across pages?
- **The search-intent match test**: take the term this page is trying to rank for; if a real person
  searched it, would *this* page satisfy what they wanted, or would they bounce back to Google?
- **The one-H1 test**: is there exactly one clear H1 that states the page topic in the words the
  audience would use, or are there zero, several, or a decorative-logo H1?

### Step 2b: Site-wide quick SEO sweep (the secondary pages)

Don't hand-audit every page; **sweep them**. Run the bundled tool (pure Python, no browser needed):

```
python scripts/seo-sweep.py <homepage-URL> --per-type 5 --out <folder>
```

It discovers pages from the homepage nav and the sitemap, classifies them (services / products /
case-studies / articles / about), caps to ~5 per type, fetches each **statically**, and returns a compact
per-page table plus site-wide flags. Per page it checks: HTTP status, `<title>` (+ length), meta
description (+ length), canonical, `noindex`, H1 count, H2/H3 counts, word count (thin-content), image-alt
coverage, Open Graph, **structured data, which it validates locally (JSON parse + required-field checks per
type, e.g. Organization/Product/Article/FAQPage), including the homepage's schema**, internal-link count, and
whether the H1 and title share keywords. Full detail and thresholds:
[references/rules-seo.md](references/rules-seo.md), "Site-wide quick SEO sweep".

Turn the sweep into **a few site-wide `SEO-` findings** (not one per page): e.g. "9 of 15 pages have
titles under 30 chars", "the homepage title is duplicated on N pages", "2 pages carry no canonical",
"the homepage Product schema is missing required fields". Put the full table in the deliverable as reference.
If the tool can't run (no Python), fall back to spot-checking a couple of pages by hand, and say the sweep
was not run.

### Step 3: Work the rubric and generate findings

Go through the SEO rubric criteria (see the reference, "Scoring rubric"): title tags, meta descriptions,
heading structure, keyword/search-intent match, content depth, URL structure, image optimization,
internal linking, structured data, indexability basics, content gaps. For each weakness, write a Finding
(IIF) with quoted evidence, an Impact and Effort rating, and a quadrant. **Also note genuine strengths**,
so the report isn't only problems.

### Step 4: Score the dimension

Rate each rubric criterion Pass / Partial / Fail. **Each criterion's "Pass" is the 2026 standard from
[benchmarks-2026.md](../../benchmarks-2026.md)** (e.g. unique 50–60-char titles, one H1, schema, HTTPS +
sitemap + canonical), so cite the benchmark in findings. Apply the weights, and total to a **0–100
score**; map
to a **letter grade** (A–F, bands in [report-format.md](../../report-format.md)). Show the criteria table so
the grade is explainable. State plainly that the grade is an **expert judgement of on-page SEO**, not a
ranking report; it doesn't measure where the site actually ranks.

### Step 5: Deliver the files

Generate `seo.md` and a styled, self-contained `seo.html` and share them. Format, the finding card
component, and the scorecard layout: see the reference, "Output file format". End the HTML with the
Print hint; **no `pagenav`** mid-session.

### Step 6: Add to the Website Audit Report & hand off

Record the **SEO & Content** section (grade + criteria + findings) into the internal running **Website
Audit Report** (do not create/show a report file now; that's the Action Report skill's job at the end).
Format and section order: [report-format.md](../../report-format.md). Tell the user the next skill is any of
**Messaging & Clarity**, **Conversion (CRO)**, or **UX & Technical**, and that **Action Report** ties them
together at the end.

## Critical rules

1. **Evidence, always.** Every finding quotes the actual tag, heading, URL, alt text, or copy. No vague
   "SEO could be better".
2. **Anchor to the audience's search.** Judge findability toward the terms this audience actually types,
   not keywords in the abstract.
3. **Fixes are concrete.** Give the rewritten title, the H1 to use, or the schema type to add, not "improve
   SEO".
4. **Impact + Effort on every finding.** So the Action Report can place it on the matrix.
5. **Sweep the site's tags; never invent rankings or numbers.** Site-wide on-page signals (titles, metas,
   H1s, canonicals, thin content, duplicate titles) and **structured-data validity** **are measured** by the
   bundled `seo-sweep.py` across the homepage and the sampled secondary pages; quote its real numbers.
   Live search performance (rankings, impressions, search volume, backlinks, organic traffic, whether Google
   has indexed a page) is **out of scope** for this suite (it needs the owner's own search data). Never state
   or estimate any of it; judge on-page SEO only.
6. **Name strengths too.** Note what already works, so the grade and the report are balanced and credible.
7. **Plain language.** Business owners are the audience; explain every term (meta description, H1,
   canonical, schema, SERP, alt text, indexability) the first time it appears.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
