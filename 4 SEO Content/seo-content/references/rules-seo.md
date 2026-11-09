# SEO & Content Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
adds the SEO-specific tests, the scoring rubric, and worked finding examples.

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
python scripts/seo-sweep.py <homepage-URL> --per-type 5 --out "audit-<slug>"
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

The builder renders the full table from `seo-sweep.json` (a `Site-wide SEO sweep` section) as the evidence
behind those findings; don't copy it into the JSON. If the tool can't run (no Python), spot-check 2–3 pages by hand and say the sweep was not run.

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

**SEO-03 — Meaningful images have no alt text** · Impact 3 · Effort 2 · **quick win**
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

## Output
Write the results to the run folder as described in [audit-data-format.md](../../../audit-data-format.md),
section "Dimension files", then build the page.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
