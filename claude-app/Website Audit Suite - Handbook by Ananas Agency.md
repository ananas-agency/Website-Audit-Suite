# Website Audit Suite - Handbook

_by Ananas Agency._ Every skill and its reference, compiled into one document. No stages - one suite.

================================================================================

# 0. Site Snapshot

**Skill ID:** `site-snapshot`

# Site Snapshot (Ananas-Agency — Website Audit intake)

## Goal

Fetch the user's website and produce a reusable **Site Snapshot**: the shared foundation for every
other Website Audit skill. Establish it once (what the site is, who it's for, and the one action it
most wants a visitor to take), then reuse it in each analysis instead of re-establishing the basics.

This suite is **URL-first**: you read the live page and pull the facts yourself; the user only
confirms them and fills the few things a page can't tell you (the real business goal, the audience,
who they see as competitors). Written for **business owners and marketers**, not developers. Keep
the language plain and explain any shorthand.

## Why a Site Snapshot

The Messaging, Conversion, SEO, and UX/Technical skills all need the same starting facts: the site's
purpose, its primary conversion, its audience, and which pages to look at. Capturing them once:

- removes repetition across skills,
- keeps every downstream finding anchored to the **same primary goal** (so recommendations pull in
  one direction),
- gives the user a single profile they can update as the site changes.

This skill is intake only. It does **not** grade or produce findings; it feeds the skills that do.

## What the snapshot captures

1. **Site & business:** the site/brand name and a one-line description of what it does; the
   category (e-commerce, SaaS, lead-gen / services, local business, content/media, other).
2. **Primary conversion goal:** the single most important action a visitor should take (buy, book a
   call, request a quote, sign up, subscribe, contact, download). Plus any secondary goals. *This is
   the anchor for the whole audit.*
3. **Audience:** who the site is for and what they're trying to do when they arrive.
4. **Page inventory:** the key pages and page *types* (home, services, products, case studies,
   articles, about, contact). Note which is the main entry page. This drives the suite's two-tier depth:
   the **homepage** gets the full in-depth audit, while the **secondary page types** get a quick site-wide
   SEO sweep (see [report-format.md](report-format.md), "Audit depth").
5. **Platform & signals:** the platform/CMS if detectable (WordPress, Shopify, Webflow, Wix, custom…),
   whether analytics/pixels are present, HTTPS, language/region (**only what's actually observable**).
6. **Competitors / references:** 1–3 sites the user compares themselves to (optional, user-supplied).
7. **Context:** the URL(s) audited, and any constraints (e.g. "don't judge the blog", "mobile
   matters most").

## Conversation flow

You do the reading; keep the user's part short. Aim for **one fetch + one confirmation pass** (roughly
3–5 questions, 2–3 at a time).

> **How to run this session: read before you start.**
> - **Fetch first, ask second.** As soon as you have the URL, fetch it and extract everything you can
>   (name, what it does, category, likely primary CTA, key pages from the nav, platform signals). Come
>   to the user with a *draft* snapshot to confirm, not a blank questionnaire.
> - **Only ask what the page can't tell you.** The real business goal, the true target audience, and
>   who they consider competitors are the three things you usually must ask. Everything else, propose
>   from what you read and let them correct it.
> - **Nail the primary goal.** If the page has several calls to action, ask the user which single
>   action matters most commercially; the whole audit is scored against it. Don't guess silently.
> - **Prefer pickable options.** For category (e-commerce / SaaS / lead-gen / local / content) and
>   primary goal (buy / book / quote / sign up / subscribe / contact / download), offer a short
>   pickable list rather than open prompts.
> - **Don't invent.** If you can't fetch the page (blocked, JS-only, paywalled), say so and ask the
>   user to paste the key pages' text or a screenshot. Anything genuinely unknown stays **TBD**, never
>   a guess; the later skills and the final reconciliation pass fill it in.

### Required inputs — capture before delivering
Check each off (or mark **TBD**) before Step 4 (Confirm & deliver):
- [ ] Site/brand name, one-line description, and the **URL(s)** audited
- [ ] Category (e-commerce / SaaS / lead-gen·services / local / content / other)
- [ ] **Primary conversion goal** (the single most important visitor action) + any secondary goals
- [ ] Audience: who it's for and their intent
- [ ] Page inventory: the key pages, and the main entry page
- [ ] Platform & signals: platform/CMS, analytics present?, HTTPS, language/region (observable only)
- [ ] Competitors / references (optional) and any constraints

### Step 1: Get the URL and fetch it

Ask for the website URL (and any specific pages the user cares about). The moment you have it, **fetch
the page(s)** and read them. From what you read, draft:
- the site name and a one-line description of what it does,
- the likely category,
- the calls to action you can see (to propose the primary goal),
- the key pages from the navigation,
- observable platform/tech signals (generator meta tag, script hosts, HTTPS, `lang`).

If the fetch fails or the page is essentially empty without JavaScript, tell the user plainly and ask
them to paste the homepage (and one or two key pages') text, or share a screenshot.

### Step 2: Confirm the draft, fill the gaps

Show the user your draft snapshot and ask them to confirm or correct it. Ask the 2–3 things the page
can't tell you:
- **Primary goal:** "Of everything on the site, what's the single most important thing you want a
  visitor to do?" (offer the pickable list).
- **Audience:** "Who is this really for, and what are they trying to do when they land?"
- **Competitors (optional):** "Whose sites do you compare yourself to?"

### Step 3: Note constraints & scope

Ask if there's anything specific to focus on or ignore (a page in progress, mobile-first, a specific
landing page for a campaign). Record it so the analysis skills respect it.

### Step 4: Confirm & deliver

Summarise the snapshot back and ask for a final confirm. Mark anything unknown as **TBD** rather than
guessing. Then deliver the files.

### Step 5: Hand off (and note the run layer)

Tell the user the snapshot is ready. The recommended next step is the **Goals & Discovery** interview. It
captures how they feel about the site and what they want it to achieve, and it runs *while* the site is
being read/measured (it's paced by the owner answering, so in the Extended layer you launch the background
scans first and interview during them). After that, any of the five analyses (**Messaging & Clarity**,
**Conversion**, **SEO**, **UX & Technical**, **Design & Visual**) can run; they're independent. From here
on, the user pastes this snapshot (and the Goals & Discovery brief) whenever a later skill asks about the site.

Also tell them which **layer** this audit will run in (both are free; see
[report-format.md](report-format.md), "Basic & Extended layers"):
- **Extended:** the measured tools can run here (you can execute `python`/Playwright), so the audit will
  include real Core Web Vitals, accessibility, mobile, design-token and tracking measurements.
- **Basic:** the tools can't run in this environment (e.g. the Claude web/desktop app), so those checks
  will be reported as *"not measured: available with the Extended layer"* and the audit is Claude's
  read-and-reason review. Everything else is identical.
Quietly test whether a tool can run (or infer from the environment) and say which mode they're getting.

## Output: deliver the snapshot as files

Generate TWO files (`site-snapshot.md` and a styled, self-contained `site-snapshot.html`) and share them
with the user. The `.html` must follow the shared navigation rules: cross-links to the other deliverables,
hover hints on short terms, and end with the Print hint (no `pagenav` mid-session). Format and the full
shared design system (CSS + page frame). See: [references/rules-snapshot.md](references/rules-snapshot.md),
section "Output file format".

Save both files and share them with the user for download.

## Add to the Website Audit Report

This suite is meant to run as one continuous session, start to finish. **Deliver only your own two files
now** (`.md` + `.html`). Keep the **Website Audit Report** as an **internal running document**. Do **not**
create, show, or hand over a report file mid-session; it is assembled and delivered only at the very end
(by the Action Report skill). As the first skill, start that internal record and add the **Site Snapshot**
section from what you just captured. Full format and section order:
[report-format.md](report-format.md).

## Critical rules

1. **URL-first.** Fetch and read the site before asking anything. Come with a draft, not a blank form.
2. **Intake, not analysis.** No grades, no findings here; that's the five analysis skills' job. Keep it
   to one short pass.
3. **Don't invent.** Report only observable signals; mark unknowns **TBD**. The Action Report's
   reconciliation pass backfills any TBDs answered later, so leave a genuine unknown as **TBD**, never a
   guess.
4. **One primary goal, anchored.** Pin down the single most important conversion and make the user
   confirm it; every later finding is judged against it.
5. **One snapshot, reused everywhere.** Remind the user to paste this into the other skills instead of
   re-establishing the site.
6. **Plain language.** The audience is business owners/marketers. Explain any shorthand; no unexplained
   jargon.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

---

## Skill reference materials: site-snapshot

### Reference: rules-snapshot.md

# Site Snapshot Rules — Detailed Reference

This reference also carries the **shared design system** (the full CSS + page frame) that every skill
in the Website Audit Suite reproduces identically in its `.html` output. If you need the style block,
it is reproduced in full at the bottom of this file.

## What to extract from the page (fetch-first checklist)

When you fetch the site, pull these before asking the user anything. Everything here is observable from
the HTML/rendered page. Do not infer beyond what's there.

### Identity & purpose
- Site / brand name: from `<title>`, the header logo `alt`, `og:site_name`, the footer.
- One-line description: from the hero H1/subhead, the `<meta name="description">`, or `og:description`.
- Category: infer from the content: e-commerce (cart, products, prices), SaaS (sign-up, pricing tiers,
  "start free trial"), lead-gen / services (contact/quote forms, "book a call"), local business
  (address, opening hours, map), content/media (articles, subscribe).

### Conversion signals
- Every visible call to action (button/link text: "Buy", "Add to cart", "Book a demo", "Get a quote",
  "Sign up", "Subscribe", "Contact us", "Download"). List them so you can propose the primary goal.
- Where they sit (above the fold? repeated? one clear one or many competing?).

### Structure
- Primary navigation items → the key pages to audit.
- Presence of: pricing page, about, contact, blog/resources, case studies/testimonials, FAQ.
- The main entry page (usually the homepage, unless the user names a campaign landing page).

### Platform & technical signals (observable only)
- Platform/CMS: `<meta name="generator">`, tell-tale asset paths (`/wp-content/` → WordPress,
  `cdn.shopify.com` → Shopify, `.webflow.io`/`assets.website-files.com` → Webflow, `wix` → Wix).
- Analytics / pixels present: Google Analytics/Tag Manager, Meta pixel, etc. (report presence, not data).
- HTTPS (is the URL `https://`?), `<html lang>`, apparent language/region.
- **Not captured at intake:** real load time, Core Web Vitals, true mobile rendering. Don't state these
  here; the **UX & Technical** skill *measures* them with the bundled tools. (Uptime and live traffic are
  out of scope for the suite.)

### Assets for the report header
- A usable logo for the consolidated report header: the header `<img>` logo, `og:image`, or one the user
  provides. Note the URL so the Action Report can embed it as a data URI. Never invent a logo.

---

## If the page can't be read

Some sites render nothing useful without JavaScript, block fetching, or sit behind a login. If so:
- Say plainly what happened ("I couldn't read the page directly; it looks JavaScript-rendered / blocked").
- Ask the user to paste the homepage (and 1–2 key pages') visible text, or share a screenshot.
- Work from what they provide; mark anything still unknown as **TBD**.

---

## Output file format

### File 1: `site-snapshot.md` (Markdown)

```markdown
# Site Snapshot — [Site name]
*[One-line description of what the site does]*
Date: [date]
Model: Ananas-Agency Website Audit intake
URL(s): [audited URLs]

## Site & business
- Category: [e-commerce / SaaS / lead-gen·services / local / content / other]
- What it does: [one or two sentences]

## Primary conversion goal
- **Primary:** [the single most important visitor action]
- Secondary: [any others]

## Audience
- Who it's for: [...]
- What they're trying to do: [...]

## Page inventory
- Main entry page: [URL]
- Key pages: [home, product/pricing, about, contact, key landing pages, blog — as found]

## Platform & signals (observable)
- Platform / CMS: [detected or TBD]
- Analytics / pixels present: [yes/no/which — presence only]
- HTTPS: [yes/no]  ·  Language/region: [...]

## Competitors / references (optional)
- [1–3 sites the user compares to]

## Scope & constraints
- [anything to focus on or ignore]

## Next step
Run the Messaging & Clarity skill (or any of the five analyses) and paste this snapshot when asked
about the site.
```

### File 2: `site-snapshot.html` (styled, share-ready)

A single **self-contained** `.html` file (all CSS inline in one `<style>` block, **no external assets
and no JavaScript**), so it opens in any browser, prints cleanly to PDF, and can be emailed as one file.
Render the **same content** as the Markdown version. Keep the `<style>` block **identical to the shared
design system** below. Every skill in this suite uses this exact block so all deliverables share one look.

- One `<section class="block">` per heading (Site & business, Primary conversion goal, Audience, Page
  inventory, Platform & signals, Competitors, Scope & constraints, Next step).
- Each fact is a `.row` (`<span class="k">label</span>value`).
- Render the page inventory and competitors as `.row`s or a small `<table>`.

**Navigation & hints (required in every generated `.html`):**
- **Cross-link every reference to another deliverable** (see [report-format.md](report-format.md)
  for canonical filenames: `messaging.html`, `conversion.html`, `seo.html`, `ux-technical.html`,
  `action-report.html`). Any finding ID cited links to that dimension's page with a tooltip.
- **Hover hints on short terms, every occurrence, not just the first.** Give a `title` tooltip to every
  appearance of the shorthand set: **IIF, CRO, SEO, UX, CTA, the ID prefixes (MSG/CRO/SEO/UX), and the
  quadrant labels (quick win / big bet / fill-in / skip)**, e.g.
  `<abbr title="Issue · Impact · Fix — the finding format">IIF</abbr>`.
- **No Previous / Next buttons in this file.** Don't add a `pagenav` mid-session. End with the Print
  hint. The walk is wired only in the final pack (see report-format.md, "Final consistency pass").
- **Print hint (no JavaScript).** End the page with
  `<p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>`.

---

## The shared design system (full style block + page frame)

Every skill in the suite reproduces this exact `<style>` block and page frame. Only these change per
skill: the `<title>`, the header `<h1>`/meta, the `utm_content` value in the two brand links (use the
skill's slug), and the section content. The palette, components, brand band, and footer stay identical.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Site Snapshot — [Site name]</title>
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
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=site-snapshot" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=site-snapshot" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>Site Snapshot — [Site name]</h1>
    <p class="tagline">[One-line description of what the site does]</p>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit intake &nbsp;·&nbsp; <b>URL:</b> [url]</div>
  </header>

  <section class="block">
    <h2 class="section">Site &amp; business</h2>
    <div class="row"><span class="k">Category</span>[e-commerce / SaaS / lead-gen·services / local / content / other]</div>
    <div class="row"><span class="k">What it does</span>[...]</div>
  </section>

  <section class="block">
    <h2 class="section">Primary conversion goal</h2>
    <div class="row"><span class="k">Primary</span>[the single most important visitor action]</div>
    <div class="row"><span class="k">Secondary</span>[...]</div>
  </section>

  <section class="block">
    <h2 class="section">Audience</h2>
    <!-- .row per fact: who it's for, what they're trying to do -->
  </section>

  <section class="block">
    <h2 class="section">Page inventory</h2>
    <!-- main entry page + key pages (.row list or small table) -->
  </section>

  <section class="block">
    <h2 class="section">Platform &amp; signals</h2>
    <!-- platform/CMS, analytics present?, HTTPS, language/region — observable only -->
  </section>

  <section class="block">
    <h2 class="section">Competitors &amp; scope</h2>
    <!-- optional competitor references, plus any focus/ignore constraints -->
  </section>

  <section class="block">
    <h2 class="section">Next step</h2>
    <div class="row">Run the Messaging &amp; Clarity skill (or any of the five analyses) and paste this snapshot when asked about the site.</div>
  </section>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=site-snapshot" target="_blank" rel="noopener">
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

================================================================================

# 1. Goals & Discovery

**Skill ID:** `goals-discovery`

# Goals & Discovery (Ananas-Agency — Website Audit intake)

## Goal

Capture the **owner's voice**, then **cross-examine it against the site**, and turn the gap into insight. A
transcript of the owner's answers is low value; the value is putting *what they believe* next to *what the
page and the measured scans actually show*, and surfacing where the two disagree.

So this skill produces a **diagnostic**, not a form:
1. a short **owner brief** (satisfaction, the one goal, success, frustrations, audience, appetite),
   compressed, not the bulk;
2. a **"Stated vs. observed" reality-check:** each belief the owner holds, set against what the fetch +
   the parallel scans reveal, with **the gap** called out (this is the centre of gravity);
3. the **tensions:** where the goal, the constraints and the data pull against each other;
4. a short, **prioritised "How to reach your goal":** opinionated direction, each item pointing to the
   analysis that will detail it.

This works *because* the interview runs while the scans render (below): by the time the owner finishes
answering, the measured data is already in, so you can immediately hold their answers against it. Where the
[Site Snapshot](../../0%20Site%20Snapshot/site-snapshot/SKILL.md) records what the *page* says and the owner
brief records what the *person* says, the reality-check is where you **add judgment neither could give alone**.
Written for **business owners and marketers**. Keep it a warm conversation, not a form; plain language, no jargon.

## Why a Goals & Discovery brief

The five analyses grade the site against the 2026 standard. But "good" only means something relative to a
goal. Two facts change how every finding should be read:

- **What the owner is trying to achieve:** more leads, more sales, fewer support calls, looking credible
  to investors. The same page is a success or a failure depending on which.
- **What they can and will change:** a beautiful redesign recommendation is useless if the brand is locked
  or the budget is an afternoon. Appetite and constraints keep the advice realistic.

Captured once, this brief travels with the [Site Snapshot](../../0%20Site%20Snapshot/site-snapshot/SKILL.md)
into every skill. It is **discovery + diagnosis + direction**. It produces **no graded findings** (the five
analyses do that, with IIF findings and letter grades), but it *does* hold the owner's answers against the
observed reality and close with **prioritised advice on how to reach their stated goals**, giving the
analyses and the [Action Report](../../7%20Action%20Report/action-report/SKILL.md) their bearings. The
reality-check and advice are directional, not the final plan; the analyses verify the specifics and the
Action Report ranks them.

## Runs *while* the site is being analysed

This interview is paced by the **owner answering**, so it costs almost no machine time, which makes it the
ideal thing to run **concurrently** with the parts of the audit that do:

- **Extended layer (tools can run, e.g. Claude Code):** as soon as you have the URL and a Site Snapshot,
  **launch the measured scans in the background** (`perf-a11y-scan.py`, `mobile-audit.py`, `design-scan.py`,
  `seo-sweep.py`, `tracking-scan.py`, `interaction-scan.py`; run them in the background so control returns
  to you), then **run this interview while they render**. When the interview wraps, the scan outputs are
  waiting. This hides the slowest part of the whole audit behind the conversation.
- **Basic layer (no tools, e.g. the Claude app):** there's no background thread, so simply **interleave**:
  read a page, ask a question, read the next while the owner types. It still feels concurrent and nothing
  is wasted.

Either way: **don't make the owner wait for a scan bar.** Talk to them while the machine works.

## What the brief captures

**Core, always capture (the fast interview):**
1. **Satisfaction today:** how happy they are with the site overall, and (optional) a quick 1–5
   self-rating across a few areas: look & feel, message clarity, getting leads/sales, ease of updating.
   *This is the owner's own view, clearly labelled, not the audit's grade.*
2. **The one goal:** the single most important thing they want the site to achieve. Reconcile this with
   the Snapshot's **primary conversion goal** (they should agree; if not, resolve it here).
3. **What success looks like:** how they'd know it's working, with a **number if they have one** (e.g.
   "20 qualified leads a month", "a 2% checkout rate", "10 booked calls a week"). Mark **TBD** if none.
4. **Biggest frustrations:** the one or two things that bother them most, in their own words.
5. **Audience, in their words:** who they think the site is really for and what those people come to do.
6. **References they admire:** sites they look at and want to emulate, and *what* they like about each.
7. **Appetite & constraints:** how much time/budget they have for change, and anything off-limits (brand
   locked, can't change platform, don't touch page X, a redesign already underway).
8. **History & wishlist** *(light)*: anything they've changed or tried recently, and the one new thing
   they wish the site could do.

**Deeper, capture when there's time, or for a fuller brief** (these sharpen the advice at the end):
9. **Current results baseline:** roughly how many enquiries/sales the site brings now, and how good the
   quality is. Gives the target a starting point ("from ~3 to ~10 a month").
10. **Traffic sources:** where visitors come from today (search, ads, referrals, social, word of mouth),
    even roughly. Tells you which lever moves the goal.
11. **Why clients really choose them:** the true differentiator, in the owner's words (not the tagline).
12. **Biggest objection:** the doubt or question prospects raise most before they buy/commit.
13. **Money pages:** the pages/products/services that matter most commercially (where to focus effort).
14. **Marketing in flight:** what's running now (ads, content/SEO, email, events, outbound) that the site
    should support.
15. **Brand & assets:** do they have brand guidelines / a logo / photography, or is a rebrand underway?
16. **Budget & timeline:** a rough band and any deadline (a launch, a campaign, a trade show).
17. **Who decides:** who signs off on changes (owner alone, a marketing lead, a committee).
18. **The competitor to beat:** one rival or example site they want to outclass, and why.
19. **Anything we missed** *(open catch-all)*: "What haven't I asked that matters for this site?" Always
    end on this; it's where owners volunteer the thing no fixed question would surface.

**Ask each in the right form:**
- **Single-select pickable** (force one answer): satisfaction · the **one** goal · appetite. The point is
  a priority; don't let these be multi.
- **Multi-select pickable** (pick all that apply): traffic sources · frustrations · audiences ·
  marketing-in-flight · brand assets. More than one is usually true.
- **Open (their own words)**: what success/"wow" looks like · why clients really choose them · the biggest
  objection · references they admire · the wishlist · the competitor to beat · the catch-all above. These
  can't be pre-listed, and they carry the richest material; quote them verbatim.
- Every pickable question still offers an **"Other"** so a pick never traps them.

Scale to the session: the **Core** eight are enough for a quick brief; add as many **Deeper** questions as
the owner has patience for. The more of the Deeper set you capture, the more specific the closing advice
can be.

## What it produces (diagnosis, not a transcript)

The output leads with the **judgment**, not the answers. In order:

**1. Owner brief (compressed).** The answers in a few tight rows: satisfaction, the one goal, success (+ a
number or **TBD**), top frustration, audience, appetite & constraints. Keep it short; it's context, not the
main event.

**2. "Stated vs. observed" reality-check, the centre of the deliverable.** For each belief the owner holds,
set it beside what the **fetched page and the parallel scans** actually show, and name **the gap**. Examples:
- Owner's goal is *"look credible"* → the scan measured **LCP 10.8s / 6 MB / no security headers** → *the
  #1 credibility killer is technical, not visual: a 10-second load reads as amateur before design is seen.*
- Owner says *"the message isn't sharp"* → the H1 is a slogan, services are generic, the portfolio is
  anonymised → *confirmed, and it's a copy fix: name what you do + who for, and name the clients.*
- Owner's satisfaction is *"okay"* → the measured foundation grades poorly → *the self-rating is generous.*

Each row is **you said → what we see → the gap**. This is what the owner can't get from a form, and it's the
reason the interview runs while the scans render; the data is ready to hold their answers against.

**3. Tensions.** Where the goal, the constraints and the data pull against each other, e.g. *"you want 'wow'
but have only a few days and want to keep the design"* → then resolve it (often the constraint and goal turn
out compatible, which is itself worth saying).

**4. "How to reach your goal": prioritised advice.** 3–6 opinionated, plain recommendations, **ordered by
leverage toward the stated goal**, each tied to an answer + the reality-check and pointing to the analysis
that details it. Sharp and short, not a hedge.

Rules that keep it honest:
- **Cross-examine, don't just record:** a row that only restates an answer adds nothing; every row must
  carry an observation or a gap.
- **Ground the "observed" side in fact:** the fetched page, or the measured scans (cite the real number).
  Don't invent metrics; the real-world numbers only analytics can show stay owner-reported.
- **No grades or IIF findings:** that's the five analyses and the Action Report. This is the orienting
  diagnosis, not the graded plan.

## Conversation flow

Keep it human and warm: **2–3 questions at a time**, in a few short passes. Always cover the **Core** eight;
then go as deep into the **Deeper** set as the owner has patience for (a quick brief is ~8 questions; a full
one is ~14–18). Come curious, not clipboard-in-hand, and let the depth follow their energy, not a checklist.

> **How to run this session: read before you start.**
> - **Kick off the machine work first (if you can), then talk.** In the Extended layer, launch the
>   background scans before you ask question one, so they render while you interview (see "Runs while the
>   site is being analysed"). Never leave the owner watching a progress bar.
> - **Mix pickable and open questions, don't make it all multiple-choice.** Use a short **pickable list**
>   for quick categorical answers (satisfaction: very happy / okay / frustrated; the goal: more leads /
>   sales / bookings / sign-ups / credibility / fewer support calls; appetite: an afternoon / a few days / a
>   project), always with an **"Other"** escape so they can type their own. But ask a genuine **open
>   question** wherever the answer needs their own words and can't be pre-listed: *what "success" actually
>   looks like, why clients really choose them, the sites they admire and why, the one thing they wish the
>   site did, and "what am I missing?"*. The open answers are where the richest material comes from; quote
>   them verbatim.
> - **Let pickable questions take more than one answer where more than one is true.** Traffic sources,
>   frustrations, audiences, and marketing-in-flight are rarely a single item, so offer these as
>   **multi-select** (pick all that apply) rather than forcing one choice. Satisfaction, the *one* goal, and
>   appetite stay single-select (the whole point is to force a priority).
> - **Nail the one goal and a number.** Push gently for the single most important goal and, if it exists,
>   a target number; it's what makes "is the site working?" answerable. If there's genuinely no number,
>   record **TBD**, don't invent one.
> - **Reconcile with the Snapshot.** If the owner's stated goal differs from the primary conversion in the
>   Site Snapshot, surface the mismatch and settle it; the analyses are scored against one goal.
> - **Their words are evidence.** Quote the owner directly in the brief (e.g. *"it looks dated and I'm
>   embarrassed to send the link"*). Don't paraphrase their frustration into blandness.
> - **Cross-examine, don't transcribe.** A brief that only echoes the answers is low value. Once you've
>   captured enough, hold each belief against the page + the finished scans and write the **"Stated vs.
>   observed"** reality-check (you said → what we see → the gap), then the **tensions**, then prioritised
>   advice. No grades or IIF findings (that's the analyses), but real judgment, grounded in what you saw.

### Required inputs — capture before delivering
Check each off (or mark **TBD**) before you deliver:
- [ ] **Core:** Satisfaction today (overall; optional per-area 1–5 self-rating)
- [ ] **Core:** The **one goal** (reconciled with the Snapshot's primary conversion)
- [ ] **Core:** What success looks like (+ a target number if they have one, else **TBD**)
- [ ] **Core:** Biggest frustration(s), in their words
- [ ] **Core:** Audience in their words
- [ ] **Core:** References they admire (optional) and what they like
- [ ] **Core:** Appetite & constraints (time/budget; anything off-limits)
- [ ] **Core:** History & wishlist (optional)
- [ ] **Core:** "Anything we missed?", the open catch-all (always ask last)
- [ ] **Deeper (as captured):** results baseline · traffic sources · true differentiator · biggest objection ·
      money pages · marketing in flight · brand & assets · budget & timeline · who decides · competitor to beat
- [ ] **Reality-check:** a **"Stated vs. observed"** row per belief (you said → what we see → the gap)
- [ ] **Tensions:** goal vs. constraints vs. data conflicts, each resolved
- [ ] **Advice:** the prioritised **"How to reach your goal"** recommendations, each tied to a gap and an analysis

### Step 1: Set up the parallel work, then open the conversation
If you have the URL and a Snapshot and can run tools, **start the background scans now**. Then open warmly:
*"Before I dig into the site, how do you feel about it today, and what do you most want it to do for you?"*

### Step 2: Satisfaction & the one goal
Ask how happy they are (offer very happy / okay / frustrated) and, optionally, a quick 1–5 on look & feel,
message clarity, getting leads/sales, and ease of updating. Then pin the **single most important goal**
(pickable list) and reconcile it with the Snapshot's primary conversion.

### Step 3: Success, frustrations & audience
Ask what success looks like (chase a number), the one or two things that frustrate them most, and who they
think the site is really for. Quote them.

### Step 4: References, appetite & constraints
Ask which sites they admire and why, how much appetite/budget they have for change, and what's off-limits.
Optionally: anything they've changed recently, and the one thing they wish the site could do.

### Step 5: Deeper context (as far as they'll go)
If the owner has patience, go into the **Deeper** set, a couple of questions at a time: current results
baseline and traffic sources, why clients really choose them and the biggest objection, the money pages and
marketing in flight, brand/assets, budget & timeline, who decides, and the competitor to beat. Stop whenever
their energy dips; every extra answer just makes the closing advice sharper. Mark anything skipped **TBD**.

### Step 6: Cross-examine — build the "Stated vs. observed" reality-check
This is the step that makes the deliverable worth reading. By now the parallel scans have finished, so hold
each of the owner's beliefs against what you can actually see:
- Read the fetched page yourself (hero, copy, CTA, proof, structure) and pull the measured numbers from the
  scans (perf/CWV, security headers, axe/keyboard, mobile, design tokens, tracking/consent, links).
- For each belief (the goal, the satisfaction rating, the frustration, the audience) write one row:
  **you said → what we see → the gap**. Prefer rows where the two *disagree* (that's the insight); confirm
  the ones where they agree, briefly.
- Then list the **tensions**: where the goal, the constraints and the data conflict, and resolve each
  (often the constraint and the goal are compatible, which is worth stating).
Ground every "observed" claim in the page or a real measured number; never invent one.

### Step 7: Write the prioritised "How to reach your goal" advice
Turn the reality-check into 3–6 **opinionated, ordered** recommendations, highest leverage toward the
stated goal first. Anchor each to a belief + its gap, make it concrete and plain, cite the real number where
one exists, and point it to the analysis that will detail it. No grades, no IIF findings; the analyses and
Action Report produce the graded, prioritised plan.

### Step 8: Confirm & deliver
Summarise the reality-check and the top advice back in a few lines and get a quick confirm. Mark genuine
unknowns **TBD** (the Action Report's reconciliation pass backfills any answered later). Then deliver the files.

### Step 9: Hand off
Tell the owner the brief is ready and travels with the Site Snapshot; they paste both whenever a later
skill asks about the site. Point them to the analyses (**Messaging**, **Conversion**, **SEO**,
**UX & Technical**, **Design & Visual**), any of which can run next, and note that by now the background
scans (if you launched them) are likely done.

## Output: deliver the brief as files

Generate TWO files (`goals.md` and a styled, self-contained `goals.html`) and share them. The `.html` uses
the **shared design system** and follows the shared navigation rules: cross-links to the other deliverables,
hover hints on short terms, and the Print hint at the end (no `pagenav` mid-session). Format and the full
shared page frame. See [references/rules-goals-discovery.md](references/rules-goals-discovery.md),
section "Output file format".

Save both files and share them with the user for download.

## Add to the Website Audit Report

This suite runs as one continuous session. **Deliver only your own two files now** (`.md` + `.html`). Keep
the **Website Audit Report** as an **internal running document**. Do **not** create, show, or hand over a
report file mid-session; the [Action Report](../../7%20Action%20Report/action-report/SKILL.md) assembles and
delivers it at the very end. Record the **Goals & Discovery** section (the compressed owner brief, the
**"Stated vs. observed"** reality-check, the tensions, and the prioritised **"How to reach your goal"**
advice) into that internal record, in its fixed slot right after Site Snapshot. Full format and section
order: [report-format.md](report-format.md).

## Critical rules

1. **Run it in parallel.** It's owner-paced: launch the background scans first (Extended) or interleave
   (Basic), so the interview and the machine work overlap. Never make the owner wait on a scan.
2. **Cross-examine, don't transcribe.** The value is the gap between what the owner *believes* and what the
   page + scans *show*. Lead with the **"Stated vs. observed"** reality-check and tensions, then prioritised
   advice. No letter grades and no IIF findings (that's the five analyses), but every row must carry an
   observation or a gap, grounded in the page or a real measured number, never invented.
3. **One goal, reconciled.** Pin the single most important goal and make it agree with the Snapshot's
   primary conversion; every later finding is judged against it.
4. **Chase a number.** Push gently for a target metric; if there genuinely isn't one, record **TBD**, never
   invent a figure.
5. **Quote the owner.** Their own words are the evidence in this brief; don't sand them down.
6. **Don't invent.** Anything unknown stays **TBD**; the reconciliation pass backfills what's answered later.
7. **Plain language, warm tone.** Business owners are the audience: a conversation, not a questionnaire.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

---

## Skill reference materials: goals-discovery

### Reference: rules-goals-discovery.md

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
- **Cross-link every reference to another deliverable** (see [report-format.md](report-format.md) for
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

================================================================================

# 2. Messaging & Clarity

**Skill ID:** `messaging-clarity`

# Messaging & Clarity (Ananas-Agency — Website Audit)

## Goal

Judge how clearly the website communicates **what it offers, who it's for, and why to choose it**, and
turn every weakness into a prioritised, fixable **Finding**. Deliver a graded messaging scorecard
(0–100 → letter grade) and a list of `MSG-` findings in **Issue · Impact · Fix** format, each rated on
Impact and Effort so the user knows what to fix first.

This is **URL-first**: read the live pages and quote what's actually on them. Written for **business
owners and marketers**. Plain language, no unexplained jargon, and every finding tied to a real effect
on their visitors.

## Inputs

- **Site Snapshot** (from Skill 0): paste it if you have it; it anchors the analysis to the site's
  **primary conversion goal** and audience. If it's missing, do a quick mini-snapshot first (fetch the
  homepage; establish name, what it does, primary goal, audience) so your findings have an anchor,
  but don't run the full intake.
- **The URL(s):** the homepage plus any key landing/product pages the user cares about.

## The core unit: a Finding (Issue · Impact · Fix)

Every observation is a Finding. See [report-format.md](report-format.md) for the full definition,
the Impact/Effort scales (1–5), and the priority quadrants (quick win / big bet / fill-in / skip). In
short:
- **Issue:** the specific clarity problem, with the **actual copy or element quoted** as evidence.
- **Impact:** what it costs (visitors bounce, don't grasp the offer, don't act). Rated **Impact 1–5**.
- **Fix:** the concrete rewrite or change, ideally with an example.
- **Effort 1–5** and a **priority quadrant** derived from Impact × Effort.

Give each finding an ID: `MSG-01`, `MSG-02`, … in impact order.

## Conversation flow

### Step 1: Load context and fetch the pages

Take the Site Snapshot (or build the mini one) and **fetch the homepage and key pages**. Read the hero,
the section headings, the CTAs, the body copy, the proof elements. Keep the site's **primary goal** in
mind; clarity is always "clear *toward what action*".

### Step 2: Run the clarity tests

Apply the fast diagnostic tests before the full rubric; details and examples in
[references/rules-messaging-clarity.md](references/rules-messaging-clarity.md):
- **The 5-second test:** from the hero alone, can a first-time visitor say *what this is, who it's for,
  and what they can do next*?
- **The "so what?" test:** does the headline promise a benefit, or just name the company/product?
- **The "only you" test:** could a competitor put their name on this exact copy? If yes, there's no
  differentiation.

### Step 2b: Check the message across the key pages (not just the homepage)

Interior pages (top services/products, case studies, about, contact) are common entry points from
search and ads, so **fetch the key pages too** and, for each, pull the **H1**, the **primary CTA**, and
the hero line. Compare them:
- **Clarity:** does each page pass the 5-second test on arrival, or does it lead with a bare product/
  category label (e.g. an H1 of just "Power BI" or "About") instead of a benefit or outcome?
- **Consistency:** is the value proposition and CTA consistent with the homepage (no bait-and-switch),
  or does the message drift page to page?
- **Case studies especially:** does the H1 tease the *result* ("How X cut reporting time 80%"), or waste
  it on a bare label?

You already have most of this data if the SEO sweep (Skill 4, `seo-sweep.py`) and the interaction scan
(Skill 3, `interaction-scan.py`) ran; reuse their per-page H1s and CTAs. Turn a systemic weakness into
one cross-page `MSG-` finding (e.g. "every interior page leads with a product-label H1, not a benefit"),
not one finding per page. This feeds the **Cross-page consistency** rubric criterion.

### Step 3: Work the rubric and generate findings

Go through the messaging rubric criteria (see the reference, "Scoring rubric"): above-the-fold clarity,
headline, subhead, primary CTA, differentiation, proof, customer language, scannable benefit-led copy,
cross-page consistency, objection handling. For each weakness, write a Finding (IIF) with quoted evidence,
an Impact and Effort rating, and a quadrant. **Also note genuine strengths**; the report shouldn't be
only problems.

### Step 4: Score the dimension

Rate each rubric criterion Pass / Partial / Fail: **each criterion's "Pass" is the 2026 standard from
[benchmarks-2026.md](benchmarks-2026.md)**, so cite the benchmark in findings ("the standard is X,
you're at Y"), then apply the weights, and total to a **0–100 score**; map
to a **letter grade** (A–F, bands in [report-format.md](report-format.md)). Show the criteria table so
the grade is explainable. State plainly that the grade is an **expert judgement**, not a lab measurement.

### Step 5: Deliver the files

Generate `messaging.md` and a styled, self-contained `messaging.html` and share them. Format, the finding
card component, and the scorecard layout. See the reference, "Output file format". End the HTML with the
Print hint; **no `pagenav`** mid-session.

### Step 6: Add to the Website Audit Report & hand off

Record the **Messaging & Clarity** section (grade + criteria + findings) into the internal running
**Website Audit Report** (do not create/show a report file now; that's the Action Report skill's job at
the end). Format and section order: [report-format.md](report-format.md). Tell the user the next skill
is any of **Conversion (CRO)**, **SEO & Content**, or **UX & Technical**, and that **Action Report** ties
them together at the end.

## Critical rules

1. **Evidence, always.** Every finding quotes the actual copy or names the exact element. No vague
   "messaging could be stronger".
2. **Anchor to the primary goal.** Judge clarity toward the site's one main conversion, not in the
   abstract.
3. **Fixes are concrete.** Give the rewrite or a worked example, not "make it clearer".
4. **Impact + Effort on every finding.** So the Action Report can place it on the matrix.
5. **Don't invent.** Judge only what's on the page. If you couldn't read a page, say so and ask for the
   text/screenshot; never assume copy you didn't see.
6. **Name strengths too.** Note what already works, so the grade and the report are balanced and credible.
7. **Plain language.** Business owners are the audience; explain any shorthand (CTA, above the fold, …).


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

---

## Skill reference materials: messaging-clarity

### Reference: rules-messaging-clarity.md

# Messaging & Clarity Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](report-format.md). This reference
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
[report-format.md](report-format.md). **No `pagenav`** mid-session; end with the Print hint.

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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

================================================================================

# 3. Conversion (CRO)

**Skill ID:** `conversion-cro`

# Conversion (CRO) (Ananas-Agency — Website Audit)

## Goal

Judge how well the website **removes friction and moves visitors toward its one primary conversion**, and
turn every weakness into a prioritised, fixable **Finding**. Deliver a graded conversion scorecard
(0–100 → letter grade) and a list of `CRO-` findings in **Issue · Impact · Fix** format, each rated on
Impact and Effort so the user knows what to fix first.

**CRO** means Conversion Rate Optimisation: making it easier and more compelling for a visitor to take
the action you want (buy, enquire, book, sign up). A **CTA** is a call to action: the button or link that
asks for that step ("Get a quote", "Add to cart").

This is **URL-first**: read the live pages and quote what's actually on them. Written for **business
owners and marketers**. Plain language, no unexplained jargon, and every finding tied to a real effect
on their visitors' likelihood to convert.

## Inputs

- **Site Snapshot** (from Skill 0): paste it if you have it; it anchors the analysis to the site's
  **primary conversion goal** and audience. If it's missing, do a quick mini-snapshot first (fetch the
  homepage; establish name, what it does, primary goal, audience) so your findings have an anchor,
  but don't run the full intake.
- **The URL(s):** the homepage plus any key pages on the conversion path (product/pricing, the landing
  page, the contact/quote/booking/checkout page the user cares about).

## The core unit: a Finding (Issue · Impact · Fix)

Every observation is a Finding. See [report-format.md](report-format.md) for the full definition,
the Impact/Effort scales (1–5), and the priority quadrants (quick win / big bet / fill-in / skip). In
short:
- **Issue:** the specific conversion problem, with the **actual copy, element, or form field quoted** as
  evidence.
- **Impact:** what it costs (visitors hesitate, abandon the form, leave the path, don't act). Rated
  **Impact 1–5**.
- **Fix:** the concrete change or rewrite, ideally with an example.
- **Effort 1–5** and a **priority quadrant** derived from Impact × Effort.

Give each finding an ID: `CRO-01`, `CRO-02`, … in impact order.

## Conversation flow

### Step 1: Load context and fetch the pages

Take the Site Snapshot (or build the mini one) and **fetch the homepage and the pages on the conversion
path**. Read the hero and its primary CTA, every CTA on the page (text, position, prominence, repetition),
the form(s) and their fields and labels, the trust signals (testimonials, reviews, logos, guarantees,
badges) and where they sit relative to the ask, the pricing (or the path to it), and anything that competes
for the click. Keep the site's **primary goal** firmly in mind; every judgement is "does this move the
visitor toward *that action*".

### Step 2: Run the fast conversion tests

Apply the fast diagnostic tests before the full rubric; details and examples in
[references/rules-conversion.md](references/rules-conversion.md):
- **The one-action test:** on each key page, is there ONE obvious next step, or do several CTAs of equal
  weight compete for the click?
- **The form-field test:** is every field on the form justified? Each extra field costs conversions;
  anything not strictly needed to act is friction.
- **The trust-at-the-ask test:** is proof or reassurance (a testimonial, guarantee, review, security
  note) right where the visitor commits (beside the button or form), not only stranded at the top of the
  page?

### Step 2b: Measure measurement-readiness (can they even track the outcome?)

The whole audit tells the user to "improve the conversion", so **check they can measure it.** If a
headless browser is available, run the bundled tool:

```
python scripts/tracking-scan.py <URL> --out <folder>
```

It renders the page on a fresh load and reports: the **analytics stack** (GA4 / GTM / measurement IDs),
**marketing pixels**, whether there's **conversion/event tracking** (dataLayer events beyond page views)
or just page views, the **Consent Management Platform** and whether **trackers fire before consent**
(a GDPR risk) with **Google Consent Mode** present or not, and the cookies set. Full method:
[references/rules-conversion.md](references/rules-conversion.md), "Measurement-readiness (measured)".

Turn gaps into `CRO-` findings; the highest-value one is usually *"analytics is installed but there's no
conversion tracking, so the primary goal can't actually be measured"* (which undercuts the entire
improvement plan), plus any *"trackers fire before consent"* privacy issue. If the tool can't run, say so
and check the analytics tags by hand from the markup.

### Step 3: Work the rubric and generate findings

Go through the conversion rubric criteria (see the reference, "Scoring rubric"): single clear path, CTA
prominence & repetition, CTA copy, form friction, trust at the ask, value reinforcement at decision points,
pricing clarity, friction & distraction (leaks), urgency/relevance, and the mobile path. For each weakness,
write a Finding (IIF) with quoted evidence, an Impact and Effort rating, and a quadrant. **Also note
genuine strengths**; the report shouldn't be only problems.

### Step 4: Score the dimension

Rate each rubric criterion Pass / Partial / Fail: **each criterion's "Pass" is the 2026 standard from
[benchmarks-2026.md](benchmarks-2026.md)**, so cite the benchmark in findings ("the standard is X,
you're at Y"), then apply the weights, and total to a **0–100 score**; map
to a **letter grade** (A–F, bands in [report-format.md](report-format.md)). Show the criteria table so
the grade is explainable. State plainly that the grade is an **expert judgement**, not a lab measurement,
and that real conversion behaviour needs the user's own analytics (see the honesty rule below).

### Step 5: Deliver the files

Generate `conversion.md` and a styled, self-contained `conversion.html` and share them. Format, the finding
card component, and the scorecard layout. See the reference, "Output file format". End the HTML with the
Print hint; **no `pagenav`** mid-session.

### Step 6: Add to the Website Audit Report & hand off

Record the **Conversion (CRO)** section (grade + criteria + findings) into the internal running **Website
Audit Report** (do not create/show a report file now; that's the Action Report skill's job at the end).
Format and section order: [report-format.md](report-format.md). Tell the user the remaining skills are
any of **Messaging & Clarity**, **SEO & Content**, or **UX & Technical**, and that **Action Report** ties
them together at the end.

## Critical rules

1. **Evidence, always.** Every finding quotes the actual CTA copy, names the form field, or points to the
   exact element. No vague "the conversion path could be tighter".
2. **Anchor to the primary goal.** Judge every element by whether it moves the visitor toward the site's
   one main conversion, not conversion in the abstract.
3. **Fixes are concrete.** Give the rewrite, the fields to cut, or the trust element to add, not "improve
   the form".
4. **Impact + Effort on every finding.** So the Action Report can place it on the matrix.
5. **Report only what's observable; never invent numbers.** Judge the copy, elements, forms, links, and
   structure you can actually see (and the measured interaction/tracking scans). **Real funnel behaviour**
   (drop-off rates, form completion, where visitors abandon) is the owner's private analytics data; no tool
   in this suite can see it, so treat it as **owner-reported**: use whatever the owner told you in the
   **Goals & Discovery** brief (current enquiry volume/quality, the goal, the frustration) as context, and
   otherwise leave it out. Never invent a conversion rate or an abandonment figure.
6. **Name strengths too.** Note what already works, so the grade and the report are balanced and credible.
7. **Plain language.** Business owners are the audience; explain any shorthand (CTA, above the fold, friction,
   leak, …).


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

---

## Skill reference materials: conversion-cro

### Reference: rules-conversion.md

# Conversion (CRO) Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](report-format.md). This reference
adds the conversion-specific tests, the scoring rubric, worked finding examples, and the HTML output format.

Everything here anchors to the site's **primary conversion goal** (from the Site Snapshot). "Good" always
means "moves the visitor toward *that one action* with the least friction". **CRO** = Conversion Rate
Optimisation; a **CTA** = call to action (the button/link that asks for the step).

## The fast conversion tests

Run these fast before the full rubric. They surface the biggest leaks quickly.

### The one-action test
On each key page, is there **ONE obvious next step**? Look at the CTAs above the fold and down the page.
If several buttons of equal visual weight compete ("Buy now", "Learn more", "Contact", "Download the
brochure", "Join our newsletter" all shouting at once), the visitor has to choose instead of act, and a
confused visitor does nothing. One clear primary action per page passes; a wall of equal choices fails.

### The form-field test
Look at every form on the conversion path and ask of **each field**: is this strictly needed to take the
action? Every extra field costs conversions. A quote form that demands phone, company, budget, and "how did
you hear about us" before giving anything back is friction the visitor didn't agree to. Only-what's-needed,
with the rest optional or asked later, passes; a long form of "nice to have" required fields fails.

### The trust-at-the-ask test
Is proof or reassurance **right where the visitor commits** (beside the button, under the form, at the
price), not stranded at the top of the page? People hesitate at the moment of action: a testimonial,
a star rating, a "no card required", a money-back guarantee, or a security note *at the ask* removes that
last doubt. Trust placed only in a far-away section, or missing entirely at the decision point, fails.

---

## Scoring rubric (weights sum to 100)

Rate each criterion **Pass** (full weight), **Partial** (half), or **Fail** (0). Sum → 0–100 → letter
grade. Always show this table in the deliverable so the grade is explainable.

| # | Criterion | What "Pass" looks like | Weight |
|---|-----------|------------------------|:------:|
| 1 | **Single clear conversion path** | One primary action per page; competing choices are minimised and visually subordinate. | 12 |
| 2 | **CTA prominence & repetition** | The primary CTA is above the fold, high-contrast, and repeated on long pages so it's always in reach. | 10 |
| 3 | **CTA copy** | Buttons say the action *and* the value ("Get my free quote"), not a bare "Submit" / "Click here". | 8 |
| 4 | **Form friction** | Only necessary fields; no needless required fields; clear labels and sensible input types. | 10 |
| 5 | **Trust signals at the ask** | Testimonials, reviews, client logos, guarantees, or security badges sit *near* the action, not only far above. | 12 |
| 6 | **Value reinforcement at decision points** | Benefits/reassurance sit beside CTAs and forms, restating "what I get" at the moment of choice. | 8 |
| 7 | **Pricing clarity** | Pricing is visible and understandable, or there's a clear, honest path to it (no dead "Contact us for pricing" wall). | 10 |
| 8 | **Friction & distraction (leaks)** | No dead ends, competing links, or unnecessary steps pulling visitors *off* the path. | 8 |
| 9 | **Urgency / relevance** | Appropriate, honest urgency or proof of demand (real stock, real deadlines, genuine social proof) — no dark patterns. | 6 |
| 10 | **Mobile conversion path** | CTA reachable and forms usable on small screens (confirmed by the measured mobile render). | 8 |
| 11 | **Measurement & tracking readiness** *(measured — tracking-scan.py)* | Analytics installed **and** conversion/event tracking configured (not just page views), with compliant consent (a real CMP / Google Consent Mode, trackers gated until opt-in). | 8 |

> A criterion can generate **more than one finding** (e.g. two separate leaks), but score the criterion
> once overall. Findings are the fix list; the rubric is the grade.

### Measurement-readiness (measured — the check that validates the whole plan)

The audit's roadmap says "improve the conversion" and "measure bookings in GA4". So **verify they can.**
Run the bundled tool (needs Playwright: `pip install playwright && playwright install chromium`; read-only, no clicks/submits):

```
python scripts/tracking-scan.py <URL> --out <folder>
```

It renders the page on a fresh load and reports:
- **Analytics stack:** GA4 / Universal Analytics / Google Tag Manager, and the measurement IDs.
- **Conversion tracking:** are there **events/conversions** (dataLayer events, gtag/fbq `track`) or **only
  page views**? Analytics with no conversion tracking means the primary goal **can't be measured**, the
  single most important gap, because it undercuts the entire improvement plan.
- **Marketing pixels:** Meta, LinkedIn, Google Ads, TikTok, etc.
- **Consent:** a real **CMP** (Cookiebot / OneTrust / Usercentrics / Complianz…) vs. a cosmetic cookie
  bar, whether **Google Consent Mode** is present, and whether **analytics/marketing trackers fire before
  consent** (a GDPR risk).
- **Cookies** set on first load (count, analytics vs marketing, first vs third party).

**Findings it produces (CRO-):**
- *"GA4 is installed but no conversion tracking is configured; the primary goal (bookings) can't be
  measured yet"* → high impact (blocks the whole 30–60–90 measurement plan), low effort (define one
  conversion event), quick win.
- *"Trackers fire before consent with no real CMP / Consent Mode"* → a privacy/GDPR finding (bigger effort:
  add a proper consent layer).

If the tool can't run, inspect the `<head>`/scripts by hand for `gtag`/`GTM-`/pixel snippets and say
conversion tracking is "not verified".

### Interaction + multi-page (does the conversion actually work, beyond the homepage?)

The analyses above focus on the homepage; the **conversion** happens across pages. Run the companion tool:

```
python scripts/interaction-scan.py <homepage-URL> --pages <home,contact,top-service> --out <folder>
```

It drives a headless browser across the key pages and checks:
- **CTA reachability:** does the primary CTA point to a real destination (a page / an on-page target),
  or a dead `#` / empty link? For buttons it clicks and observes navigation.
- **Form validation:** the main form's fields, required count, input types, and whether the browser would
  **block an empty submit** (client-side validation present), via `checkValidity()`.

**Ethics, read this:** the tool may **follow a navigation CTA** (that's just browsing) but it **never
submits a form**. Submitting sends real data to the business. Never auto-submit a live production form;
if you need to test submission, do it on staging or with the owner's permission.

Findings it surfaces (CRO-): a CTA that only scrolls to a buried widget, a **contact page with no form**
(mailto-only), a form with no validation, or a dead CTA. These are conversion-path defects a homepage,
markup-only pass can't see.

Grade bands (from report-format.md): A 90–100 · B 80–89 · C 70–79 · D 60–69 · F 0–59.

> **Honesty rule (conversion-specific).** Report only what's observable from the fetched page (the copy,
> the CTAs, the form fields, the links, the layout, what renders), plus the measured interaction/tracking
> scans. Real funnel data (drop-off, form-completion, cart-abandonment, where visitors leave) is the owner's
> private analytics and **no tool in this suite can see it**. Treat it as **owner-reported**: use what the
> owner said in the **Goals & Discovery** brief as context, and otherwise leave it out. **Never invent a
> conversion rate or an abandonment number.** A grade is an expert judgement, not a lab measurement. Say so.

---

## Worked finding examples (Issue · Impact · Fix)

**CRO-01. 11-field contact form on the main conversion page** · Impact 4 · Effort 2 · **quick win**
- **Issue:** The "Request a quote" form requires eleven fields (name, company, phone, email, budget range,
  timeframe, job title, industry, company size, "how did you hear about us", and a message), all marked
  required before the visitor gets anything.
- **Impact:** Every extra required field costs completions; a first-touch enquiry form this long turns away
  ready-to-buy visitors who'd happily give a name and email. This is the primary conversion, so the leak is
  costly. (Real completion rate is the owner's analytics data, owner-reported via Goals & Discovery, not
  tool-measured.)
- **Fix:** Cut to the two or three fields you truly need to respond (name, email, one-line message); make
  the rest optional or ask them after first contact. Add a reassurance line under the button.
- **Evidence:** `<label>Budget range *</label> … <label>Company size *</label> … <label>How did you hear about us? *</label>`

**CRO-02. "Submit" button with no value or reassurance** · Impact 4 · Effort 1 · **quick win**
- **Issue:** The primary CTA on the enquiry form reads *"Submit"*, with no statement of what happens next
  and no trust signal beside it.
- **Impact:** "Submit" describes the visitor's effort, not their reward, and at the exact moment of
  commitment there's nothing answering "is this safe / what do I get / how fast will they reply?". That is
  hesitation right at the ask.
- **Fix:** Rewrite to action + value, e.g. *"Get my free quote"*, and add a one-line reassurance beneath it
  ("No obligation — we reply within one working day"). Consider a small testimonial or star rating next to
  the button.
- **Evidence:** `<button type="submit">Submit</button>`

**CRO-03. Five competing CTAs above the fold; no single path** · Impact 4 · Effort 3 · **big bet**
- **Issue:** The hero shows five buttons of equal weight (*"Buy now", "Book a demo", "Download brochure",
  "Watch video", "Join newsletter"*), with none visually dominant.
- **Impact:** The one-action test fails: the visitor must choose instead of act, and competing choices dilute
  every click away from the primary goal (which the Snapshot names as booking a demo).
- **Fix:** Pick one primary action, make it the loud, high-contrast button, and demote the rest to quieter
  secondary links lower down. One page, one job.
- **Evidence:** `<a class="btn">Buy now</a> <a class="btn">Book a demo</a> <a class="btn">Download brochure</a> …`

**CRO-04. Pricing hidden behind "Contact us"** · Impact 3 · Effort 3 · **fill-in**
- **Issue:** The pricing page carries no numbers, only *"Contact us for a custom quote"* with a form.
- **Impact:** Visitors who can't gauge fit or affordability leave to compare a competitor who shows a range;
  the "talk to sales" wall filters out self-serve buyers who were ready.
- **Fix:** Show at least a starting price, a "from £X" band, or three example packages; even indicative
  numbers let visitors self-qualify and keep them on the path.

**Strength worth noting** (not a finding, but record it): "The checkout shows trust badges, a money-back
guarantee, and 'no card details stored' right beside the Pay button: proof exactly at the ask."

### Anti-patterns to catch (each becomes a finding)
- **"Submit" / "Click here" CTAs:** button copy that names the effort, not the reward.
- **Over-long forms:** asking phone, company, budget, job title before giving any value.
- **No trust at the ask:** testimonials and guarantees stranded far from the button or form.
- **Competing CTAs:** several equal-weight buttons; no single obvious next step.
- **Hidden pricing:** "Contact us for pricing" with no number or range anywhere.
- **Auto-playing distractions:** carousels, video, pop-ups, or chat nags that pull focus off the action.
- **Leaks off the path:** the checkout/enquiry page still carries full nav, footer links, and outbound
  links that invite the visitor away.
- **Multi-step where one step would do:** a three-screen flow (or a mandatory account) for what a single
  short form could capture.
- **Dark-pattern urgency:** fake countdowns, invented "only 2 left", pre-ticked upsells. Honest urgency
  only.
- **CTA below the fold on mobile:** the primary action pushed off-screen behind a wall of hero text
  (flag as observable; the measured mobile render, `mobile-audit.py` via UX & Technical, confirms the
  small-screen placement).

---

## Output file format

### File 1: `conversion.md` (Markdown)

```markdown
# Conversion (CRO) — [Site name]
Date: [date]
Model: Ananas-Agency Website Audit
Primary goal audited against: [the site's primary conversion]

## Grade: [A–F] ([score]/100)
[one-line verdict, e.g. "Weak — the offer is strong but an 11-field form and five competing CTAs leak the click."]

### Scorecard
| # | Criterion | Pass/Partial/Fail | Weight | Points |
|---|-----------|-------------------|:------:|:------:|
| 1 | Single clear conversion path | Fail | 14 | 0 |
| ... | ... | ... | ... | ... |
| | **Total** | | **100** | **[score]** |

## Findings
### CRO-01. [short title] — Impact [1–5] · Effort [1–5] · [quick win/big bet/fill-in/skip]
- **Issue:** [I, with evidence]
- **Impact:** [what it costs; real funnel numbers are owner-reported (Goals & Discovery), not tool-measured]
- **Fix:** [F, concrete]
> "[quoted copy / element / form field as evidence]"

[... further findings, impact order ...]

## What's working
- [1–3 genuine strengths]

## Summary
- Findings: [n] ([x] quick wins, [y] big bets, ...)
- Top priority: [CRO-ID — one line]
```

### File 2: `conversion.html` (styled, share-ready)

A single **self-contained** `.html` file (all CSS inline in one `<style>` block, **no external assets and
no JavaScript**). Use the **shared design system**: the exact `<style>` block and page frame from
[rules-snapshot.md](../../../0%20Site%20Snapshot/site-snapshot/references/rules-snapshot.md), reproduced
in full below so this skill is self-contained. Only these differ from the snapshot page: the `<title>`,
the header, the `utm_content=conversion-cro` in the two brand links, and the section content.

Components:
- **A grade section first:** the letter grade in a `.grade` chip (class `a`/`b`/`c`/`d`/`f`), the score,
  a one-line verdict, and the **scorecard `<table>`** (criteria × pass/partial/fail × weight × points).
- **A Findings section:** one `.card` per finding. Card header: the `.id` chip (`CRO-01`), the short
  title, an **Impact meter** (`<span class="scorewrap"><span class="meter"><i style="width:NN%"></i></span><span class="scoreno">Impact X/5</span></span>`,
  width = Impact/5×100), and the **priority `.tag`** (`quickwin` / `bigbet` / `fillin` / `skip`). Body:
  Issue / Impact / Fix as `.row`s (append `· Effort X/5` in the Impact row via `<span class="effort">`),
  and the quoted evidence in a `<blockquote>`.
- **A "What's working" section:** `.row`s or `ul.clean` of strengths.
- **A Summary section:** findings count and the top priority (cited by ID).

**Navigation & hints (required):** cross-link other deliverables and tooltip every ID and shorthand term
(IIF, CRO, SEO, UX, CTA, MSG/CRO/SEO/UX, quadrant labels), every occurrence, per
[report-format.md](report-format.md). **No `pagenav`** mid-session; end with the Print hint.

Finding card pattern:
```html
<article class="card">
  <h3><span class="id">CRO-01</span> 11-field contact form on the main conversion page
      <span class="scorewrap"><span class="meter"><i style="width:80%"></i></span><span class="scoreno">Impact 4/5</span></span>
      <span class="tag quickwin">quick win</span></h3>
  <div class="row"><span class="k">Issue</span>The "Request a quote" form requires eleven fields, all marked required before the visitor gets anything.</div>
  <div class="row"><span class="k">Impact</span>Every extra required field costs completions on the primary conversion; real drop-off is <span class="term" title="Owner's analytics data — owner-reported via Goals &amp; Discovery, not tool-measured">owner-reported</span>. <span class="effort">· Effort 2/5</span></div>
  <div class="row"><span class="k">Fix</span>Cut to the two or three fields you truly need; make the rest optional; add a reassurance line under the button.</div>
  <blockquote>"&lt;label&gt;Budget range *&lt;/label&gt; … &lt;label&gt;How did you hear about us? *&lt;/label&gt;"</blockquote>
</article>
```

Full page (reproduce the shared `<style>` block verbatim; it is identical suite-wide):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Conversion (CRO) — [Site name]</title>
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
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=conversion-cro" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=conversion-cro" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>Conversion (CRO) — [Site name]</h1>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit &nbsp;·&nbsp; <b>Grade:</b> [A–F] ([score]/100)</div>
  </header>

  <section class="block">
    <h2 class="section"><span class="no">1</span> Grade &amp; scorecard</h2>
    <div class="row"><span class="grade d">D</span> <b>64/100</b> — [one-line verdict]</div>
    <div class="tablewrap"><table>
      <tr><th>#</th><th>Criterion</th><th>Result</th><th>Weight</th><th>Points</th></tr>
      <tr><td>1</td><td>Single clear conversion path</td><td>Fail</td><td>14</td><td>0</td></tr>
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
    <h2 class="section"><span class="no">4</span> Summary</h2>
    <div class="row"><span class="k">Findings</span>[n] ([x] quick wins, [y] big bets, …)</div>
    <div class="row"><span class="k">Top priority</span>[CRO-ID — one line]</div>
  </section>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=conversion-cro" target="_blank" rel="noopener">
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

================================================================================

# 4. SEO & Content

**Skill ID:** `seo-content`

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

Every observation is a Finding. See [report-format.md](report-format.md) for the full definition,
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
[benchmarks-2026.md](benchmarks-2026.md)** (e.g. unique 50–60-char titles, one H1, schema, HTTPS +
sitemap + canonical), so cite the benchmark in findings. Apply the weights, and total to a **0–100
score**; map
to a **letter grade** (A–F, bands in [report-format.md](report-format.md)). Show the criteria table so
the grade is explainable. State plainly that the grade is an **expert judgement of on-page SEO**, not a
ranking report; it doesn't measure where the site actually ranks.

### Step 5: Deliver the files

Generate `seo.md` and a styled, self-contained `seo.html` and share them. Format, the finding card
component, and the scorecard layout: see the reference, "Output file format". End the HTML with the
Print hint; **no `pagenav`** mid-session.

### Step 6: Add to the Website Audit Report & hand off

Record the **SEO & Content** section (grade + criteria + findings) into the internal running **Website
Audit Report** (do not create/show a report file now; that's the Action Report skill's job at the end).
Format and section order: [report-format.md](report-format.md). Tell the user the next skill is any of
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

---

## Skill reference materials: seo-content

### Reference: rules-seo.md

# SEO & Content Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](report-format.md). This reference
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
[report-format.md](report-format.md). **No `pagenav`** mid-session; end with the Print hint.

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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

================================================================================

# 5. UX & Technical

**Skill ID:** `ux-technical`

# UX & Technical (Ananas-Agency — Website Audit)

## Goal

Judge how **usable and technically sound** the website is (can visitors find their way, read the
page, use it on a phone, trust it, and complete a form without friction), and turn every weakness
into a prioritised, fixable **Finding**. Deliver a graded UX & Technical scorecard (0–100 → letter
grade) and a list of `UX-` findings in **Issue · Impact · Fix** format, each rated on Impact and
Effort so the user knows what to fix first.

This is **URL-first**: inspect the live pages and quote what's actually in the markup and on screen.
Written for **business owners and marketers**: plain language, and every piece of jargon explained
(viewport, alt text, contrast ratio, render-blocking, Core Web Vitals) with each finding tied to a
real effect on their visitors.

## Inputs

- **Site Snapshot** (from Skill 0). Paste it if you have it; it anchors the analysis to the site's
  **primary conversion goal**, audience, page inventory, and the observable platform/HTTPS signals
  already captured. If it's missing, do a quick mini-snapshot first (fetch the homepage; establish
  name, what it does, primary goal, key pages, HTTPS) so your findings have an anchor, but don't run
  the full intake.
- **The URL(s)**: the homepage plus any key pages the user cares about (a product/pricing page, the
  contact/booking page with the main form, a deep content page).

## The core unit: a Finding (Issue · Impact · Fix)

Every observation is a Finding. See [report-format.md](report-format.md) for the full definition,
the Impact/Effort scales (1–5), and the priority quadrants (quick win / big bet / fill-in / skip). In
short:
- **Issue**: the specific usability or technical problem, with the **actual element, attribute, or
  page quoted** as evidence (the missing viewport tag, the unlabeled input, the 404 link).
- **Impact**: what it costs (visitors can't navigate, bounce on mobile, can't submit the form, lose
  trust). Rated **Impact 1–5**.
- **Fix**: the concrete change, ideally with the exact markup or attribute to add.
- **Effort 1–5** and a **priority quadrant** derived from Impact × Effort.

Give each finding an ID: `UX-01`, `UX-02`, … in impact order.

## Conversation flow

### Step 1: Load context and fetch the pages

Take the Site Snapshot (or build the mini one) and **fetch the homepage and key pages**. Read the
markup, not just the rendered text: the `<head>` (viewport meta, `<html lang>`, HTTPS on asset URLs),
the navigation, the heading order (`<h1>`…`<h6>`), image `alt` attributes, form `<label>`s and input
types, link `href`s, and the weight/dimensions of hero images. Keep the site's **primary goal** in
mind. Usability is always "usable *toward completing that action*".

### Step 2: Run the UX/technical fast tests

Apply the fast diagnostic tests before the full rubric. Details and examples in
[references/rules-ux-technical.md](references/rules-ux-technical.md):
- **The three-click test**: can a visitor reach any key page (product, pricing, contact) in about
  three clicks from the homepage, or do they hit dead ends?
- **The squint test**: blur or squint at the page: does the visual hierarchy pull the eye to the one
  main action, or does everything shout equally (or nothing stands out)?
- **The mobile-viewport test**: is there a `<meta name="viewport">` tag, and (confirmed by the
  measured render in Step 2b) do the text size and tap targets survive a narrow phone-width screen
  without a horizontal scrollbar?

### Step 2b: Measure mobile-friendliness (headless render — the correct way)

Don't guess mobile behaviour from the markup; **render the page and measure it**. If Playwright is
available (`pip install playwright && playwright install chromium`, which bundles its own Chromium,
cross-platform), run the bundled tool:

```
python scripts/mobile-audit.py <URL> --out <folder> --widths 320,390,414
```

It renders the page with real mobile emulation at each phone width and reports, per width
(full detail and thresholds in [references/rules-ux-technical.md](references/rules-ux-technical.md),
"Measured mobile-friendliness test"):
- **Fits the screen?** Document scroll width vs viewport width (any horizontal scroll = fail).
- **Elements too big**: every element whose box extends past the screen edge (real overflow), kept
  separate from content merely clipped inside a carousel/`overflow` container.
- **Images wider than the screen.**
- **Tap targets under 44×44px**: buttons/links too small to tap reliably (Apple HIG / WCAG 2.5.5).
- **Text under 12px**: too small to read on a phone.
- A **full-page screenshot per width**: open them and eyeball the layout for anything the numbers miss.

Turn each measured problem into a `UX-` finding with the real numbers as evidence (e.g. "44 tap
targets below 44×44px at 390px: pagination, language switch, carousel controls"). If **no headless
browser is available** (Basic layer), say so and fall back to marking these "not measured", then describe the
observable signals but never assume the result.

### Step 2c: Measure performance, accessibility & security (headless — the correct way)

Don't guess "is it fast?", "is it accessible?", or "is it secure?"; **measure them**. If Playwright is available (bundled Chromium, cross-platform),
run the bundled scanner:

```
python scripts/perf-a11y-scan.py <URL> --out <folder>
```

It renders the page (mobile-emulated, as Google measures) and returns, all locally with no API keys:
**lab Core Web Vitals** (LCP, CLS, FCP, TTFB) **+ a lab INP proxy (Total Blocking Time)**, page weight + the
heaviest resources; **real WCAG violations** via **axe-core** (critical / serious / moderate / minor) **plus a
keyboard focus-order pass**; and a **security** read (HTTPS, TLS version, HSTS/CSP & security headers present
vs. missing, redirect chain, mixed content). Thresholds and full method:
[references/rules-ux-technical.md](references/rules-ux-technical.md), "Measured performance, accessibility & security".
Turn each into a `UX-` finding with the numbers as evidence. **Honesty:** this is a **lab** run. The INP
figure is the standard lab proxy (TBT), not the real-world field percentile; and full **screen-reader**
testing is manual and out of scope. Say so. If the scanner can't run (Basic layer), fall back to "not measured".

### Step 3: Work the rubric and generate findings

Go through the UX & Technical rubric criteria (see the reference, "Scoring rubric"): navigation & IA,
visual hierarchy & readability, mobile responsiveness, page-speed signals, accessibility, links &
errors, security & trust basics, forms usability, UI consistency, layout & whitespace, responsive
robustness. For each weakness, write a Finding (IIF) with quoted evidence, an Impact and Effort
rating, and a quadrant. **Also note genuine strengths**, so the report isn't only problems.

**Readability of the content templates is measured.** The Design & Visual scan (`design-scan.py --pages`)
renders representative interior templates (an article, a service page, a case study) and measures each one's
**body text-alignment** and **characters-per-line**. Use `design-pages.json` for the readability criterion:
centred body copy, or lines well outside ~45-75 characters, on an article or service template is a real
`UX-` readability finding even when the homepage reads fine. Cite the measured value.

### Step 4: Score the dimension

Rate each rubric criterion Pass / Partial / Fail. **Each criterion's "Pass" is the 2026 standard from
[benchmarks-2026.md](benchmarks-2026.md)** (Core Web Vitals ≤ 2.5s/200ms/0.1, tap targets ≥ 44px,
WCAG 2.2 AA, HTTPS + HSTS, and the **UI/UX & usability** bars: Nielsen's heuristics, clear IA in ~1–3
clicks, one focal point, ≥ 16px / 45–75-char / 1.5 text, consistency, visible feedback under 1s), so cite
the benchmark in findings. Apply the weights, and total to a **0–100 score**;
map to a **letter grade** (A–F, bands in [report-format.md](report-format.md)). Show the criteria
table so the grade is explainable. State plainly that the grade is an **expert judgement**, informed by the
measured numbers where the bundled tools ran (speed, mobile fit, accessibility, security, links), and by
observable markup signals where they didn't (Basic layer).

### Step 5: Deliver the files

Generate `ux-technical.md` and a styled, self-contained `ux-technical.html` and share them. Format,
the finding card component, and the scorecard layout: see the reference, "Output file format". End
the HTML with the Print hint; **no `pagenav`** mid-session.

### Step 6: Add to the Website Audit Report & hand off

Record the **UX & Technical** section (grade + criteria + findings) into the internal running
**Website Audit Report** (do not create/show a report file now; that's the Action Report skill's job
at the end). Format and section order: [report-format.md](report-format.md). Tell the user the
remaining analyses are any of **Messaging & Clarity**, **Conversion (CRO)**, or **SEO & Content**, and
that **Action Report** ties them together at the end.

## Critical rules

1. **Evidence, always.** Every finding quotes the actual element, attribute, or page: the missing
   `<meta name="viewport">`, the `<img>` with no `alt`, the link returning 404. No vague "the UX
   could be better".
2. **Measure what you can; be honest about the rest.** With a headless browser, these are now
   **measured, not guessed**, all locally with no API keys: **mobile-friendliness** (`mobile-audit.py`,
   Step 2b); **lab Core Web Vitals + a lab INP proxy (TBT) + page weight**, **WCAG violations via axe-core
   + a keyboard focus pass**, and **security** (HTTPS/TLS/headers/redirects/mixed content)
   (`perf-a11y-scan.py`, Step 2c); and **broken-link HTTP status** across the key pages
   (`interaction-scan.py`). Base those findings on the real numbers and quote them. The only thing a local
   run genuinely can't produce is the real-world **field percentile** (LCP/INP/CLS across many real users).
   Measure the lab equivalents and don't claim a field number; full **screen-reader** testing stays
   manual and out of scope. Never invent a load time, a CWV score, or a violation you didn't measure. In the
   **Basic layer** (no browser), these fall back to "not measured"; describe observable signals, don't name
   a third-party tool.
3. **Anchor to the primary goal.** Judge usability toward the site's one main conversion; friction
   on the path to the main action outranks cosmetic issues.
4. **Fixes are concrete.** Give the exact attribute, tag, or change (e.g. "add
   `<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">` to the `<head>`"), not
   "make it responsive".
5. **Impact + Effort on every finding.** So the Action Report can place it on the matrix.
6. **Don't invent.** Judge only what you can observe. If a page couldn't be read or rendered, say so
   and ask for the markup/screenshot; never assume behaviour you didn't see.
7. **Name strengths too.** Note what already works, so the grade and the report are balanced and
   credible.
8. **Plain language.** Business owners are the audience; explain every technical term the first time
   (viewport = the visible screen area; alt text = the text description of an image; contrast ratio =
   how readable text is against its background; render-blocking = scripts that delay the page
   appearing; Core Web Vitals = Google's set of real-world speed/stability scores).


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

---

## Skill reference materials: ux-technical

### Reference: rules-ux-technical.md

# UX & Technical Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](report-format.md). This reference
adds the UX/technical-specific fast tests, the scoring rubric, worked finding examples, and the HTML
output format.

## What you can and cannot check (read this first)

This dimension is where the **honesty rule** bites hardest, because the questions users ask ("is it
fast?", "is it accessible?") often need tools you don't have. Be scrupulous about the line:

**You CAN verify from the page you fetched:** the `<head>` tags (`<meta name="viewport">`,
`<html lang>`), whether URLs and assets are served over **HTTPS** and whether any asset is loaded over
plain `http://` on an `https://` page (**mixed content**), the navigation and whether key pages are
reachable, the **heading order** (`<h1>`…`<h6>`), image **alt** attributes, form `<label>`s and input
`type`s, link `href`s (and whether they resolve), the number and apparent weight of scripts and
images, and obvious layout/UI-consistency issues in what renders.

**You CAN now MEASURE** three things a static read couldn't, all via bundled headless-Chrome tools:
1. **Mobile-friendliness** via `scripts/mobile-audit.py`: fit-to-screen, oversized elements/images, tap
   targets ≥44×44px, text ≥12px (see "Measured mobile-friendliness test" below).
2. **Performance (lab Core Web Vitals)** via `scripts/perf-a11y-scan.py`: LCP, CLS, FCP, TTFB, load time,
   total transferred weight, request count, third-party count, and the heaviest resources.
3. **Accessibility (WCAG):** the same `scripts/perf-a11y-scan.py` injects **axe-core** and returns real
   violations grouped by impact (critical / serious / moderate / minor).
Quote the **real measured numbers** as evidence; these are no longer "observed from markup only" (see
"Measured performance & accessibility" below).

**Measured here, locally, no API keys.** The bundled tools render/inspect the page and return real
numbers; quote them as evidence. The only thing a local run genuinely can't produce is the **real-world
field percentile** (LCP/INP/CLS across many real users). That needs live user data, so this suite measures
the **lab** equivalents instead and never claims field numbers.

| Measured here (bundled tool) | What you get |
|------------------------------|--------------|
| Mobile fit / tap targets / text size (`mobile-audit.py`) | measured (or "not measured" only if no browser is present) |
| Lab Core Web Vitals — LCP/CLS/FCP/TTFB + page weight (`perf-a11y-scan.py`) | measured (lab) |
| INP — lab proxy via **Total Blocking Time** + long-tasks (`perf-a11y-scan.py`) | measured (lab proxy) |
| Accessibility — WCAG violations via axe-core **+ a keyboard focus-order pass** (`perf-a11y-scan.py`) | measured |
| Security — HTTPS, TLS version, HSTS/CSP & headers, redirect chain, mixed content (`perf-a11y-scan.py`) | measured |
| Broken links — HTTP status of every link across the key pages (`interaction-scan.py`) | measured |

Only in the **Basic layer** (no headless browser available) do these fall back to "not measured"; there you
still flag the *signals* (a 4 MB hero image, ten render-blocking scripts, missing alt) but never fabricate a
score. Full **screen-reader** testing remains manual and is out of scope: say so plainly; don't point at a
third-party tool.

---

## The UX/technical fast tests

Run these fast before the full rubric; they surface the biggest issues quickly.

### The three-click test
Starting from the homepage, can a visitor reach any **key page** (the main product/service, pricing,
and the contact/booking page) in roughly **three clicks**, following clearly labelled links? If a key
page is buried, orphaned, or only reachable via the footer, or the trail leads to a dead end, that's a
navigation finding.

### The squint test
Blur your eyes (or mentally squint) at the first screen. Does one element, the primary action, stand
out by size, colour, or position, so the eye lands on it first? If everything competes at the same
visual weight (or nothing draws the eye), the **visual hierarchy** isn't guiding the visitor to the
main action. This is the visual analogue of the messaging 5-second test.

### The mobile-viewport test
Two parts. First, is there a `<meta name="viewport" content="width=device-width, initial-scale=1">`
tag in the `<head>`? Without it, phones render the desktop layout zoomed out and the site is not
mobile-responsive. Second, and this is now **measured, not eyeballed** (see "Measured mobile-friendliness
test" below), when rendered at phone width, does the **text stay legible** (≥12px), do the **tap targets
stay big enough** (≥44×44px), and does the content **fit without a horizontal scrollbar**? Failing either
part is a high-impact mobile finding; remember most traffic is mobile.

### The jargon check (for the reader, not the site)
Every technical term you use in a finding gets a plain-language gloss on first use: *viewport* (the
visible screen area), *alt text* (an image's text description, read by screen readers and shown if the
image fails), *contrast ratio* (how readable text is against its background), *render-blocking* (a
script that delays the page appearing), *Core Web Vitals* (Google's real-world speed/stability scores).

---

## Measured mobile-friendliness test (the correct way to check "does it fit the phone?")

Static HTML can only tell you the viewport tag is present; it cannot tell you whether things actually
**fit** or are **too big**, because that depends on CSS, images, and JavaScript at a real screen width.
So render the page and measure it.

**Run it** (needs Playwright: `pip install playwright && playwright install chromium`; it bundles its own Chromium, no browser to install):
```
python scripts/mobile-audit.py <URL> --out <folder> --widths 320,390,414
```
320px = small phone, 390px = iPhone-class, 414px = large phone. The tool uses real mobile emulation
(device metrics, touch, 2× density), then per width reports and saves a full-page screenshot.

**What it measures, and the pass/fail thresholds:**

| Check | Question | Pass |
|-------|----------|------|
| **Fits the screen** | Is the page's scroll width ≤ the viewport width? | no horizontal scroll (≤ +2px) |
| **Elements too big** | Does any element's box stick out past the screen edge? | zero *real* overflowers (the tool separates these from content merely clipped inside a carousel/`overflow` container, which is usually fine) |
| **Images too big** | Is any image wider than the screen? | zero |
| **Tap targets** | Are buttons/links ≥ 44×44 CSS px? | count of sub-44px targets → the fewer the better (Apple HIG / WCAG 2.5.5 target size) |
| **Legible text** | Is body text ≥ 12px? | zero elements under 12px |

**Turn results into findings.** Each failed check becomes a `UX-` finding with the real numbers as
evidence, e.g.:
- *"At 390px the page fits with no horizontal scroll and no oversized images; mobile layout is sound."*
  (a **strength**, recorded, not a finding)
- *"44 tap targets render below 44×44px at 390px (pagination 32×32, language switch 40×40, carousel
  arrows 30×32); fiddly to tap on a phone."* → Impact 3, Effort 2, quick win.
- *"A hero container is 131px wider than the 390px screen and forces sideways scroll."* → Impact 4+.

**Also open the screenshots.** The numbers catch overflow and sizing; your eyes catch things they can't:
overlapping elements, a menu that covers content, text crammed against the edge, an image that's
technically in-bounds but visually dominating. Note those as findings too.

**If there's no headless browser** (Basic layer), say so and fall back to "not measured"; describe the
observable signals (viewport meta present? fixed-width containers? tiny tap targets in the markup?) but do
**not** assert whether the page actually fits.

---

## Measured performance, accessibility & security (the flags a static read leaves open)

Run the bundled scanner (needs Playwright: `pip install playwright && playwright install chromium`; axe-core
is loaded from a CDN at run time, everything else is local, no API keys):

```
python scripts/perf-a11y-scan.py <URL> --out <folder>
```

It renders the page **mobile-emulated** (as Google measures) and returns four things:

**Performance: lab Core Web Vitals + weight + a lab INP proxy**, with the 2026 thresholds:

| Metric | Good | Needs work | Poor |
|--------|------|-----------|------|
| **LCP** (largest content paints) | ≤ 2.5s | 2.5–4s | > 4s |
| **CLS** (layout shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 |
| **FCP** (first paint) | ≤ 1.8s | 1.8–3s | > 3s |
| **TTFB** (server response) | ≤ 0.8s | 0.8–1.8s | > 1.8s |
| **INP proxy — Total Blocking Time** | ≤ 200ms | 200–600ms | > 600ms |

Plus total transferred KB, request count, third-party host count, and the **heaviest resources** (a
multi-MB hero image/video is the usual culprit). **Honesty:** this is a **lab** run (one emulated load); the
INP figure is the standard **lab proxy (Total Blocking Time)**, not the real-world field percentile (which
needs many real users); measure the lab number and don't claim a field number.

**Accessibility: real WCAG violations via axe-core** (Deque, MIT), grouped by impact (**critical / serious /
moderate / minor**) with the rule id, the WCAG tags, and element counts, **plus a keyboard focus-order pass**
(how many tab stops reached, how many with no visible focus indicator, and positive-`tabindex` anti-patterns).
A **critical** (e.g. a button with no accessible name) or **serious** (e.g. colour-contrast) is a genuine
WCAG 2.2 AA failure and, under the EU Accessibility Act, a compliance risk. **Honesty:** axe + the keyboard
pass catch the automatable share of WCAG; full **screen-reader** testing is manual and out of scope; say so.

**Security, measured from the response:** HTTPS, TLS version, which security headers are present vs. missing
(HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy), the redirect chain,
and any **mixed content** (http assets on an https page).

Turn each into a `UX-` finding with the real numbers as evidence (e.g. "TTFB 1.3s and a 2 MB hero video",
"axe-core: 1 critical (button-name), 18 contrast failures", "TBT 274ms", "HSTS and CSP both missing"). In the
**Basic layer** (no browser), fall back to "not measured"; never invent a score.

---

## Scoring rubric (weights sum to 100)

Rate each criterion **Pass** (full weight), **Partial** (half), or **Fail** (0). Sum → 0–100 → letter
grade. Always show this table in the deliverable so the grade is explainable. Criteria marked
**(observable-only)** are judged from the markup and what renders, not from a measurement tool; note
that limitation in the finding.

| # | Criterion | What "Pass" looks like | Weight |
|---|-----------|------------------------|:------:|
| 1 | **Navigation & information architecture** | Intuitive, labelled nav; key pages findable in 1–2 clicks; no dead ends or orphan pages. | 12 |
| 2 | **Visual hierarchy & readability** *(interior templates measured — design-scan.py)* | Clear hierarchy; legible type size; **line length ~45-75 chars** and **body text left/justified, not centred**, on content templates (articles, service pages), not just the homepage; adequate text contrast. | 10 |
| 3 | **Mobile responsiveness** *(measured — mobile-audit.py)* | `<meta name="viewport">` present; page fits the screen at 320/390/414px with no horizontal scroll; no oversized elements/images; text ≥12px; tap targets ≥44×44px. | 12 |
| 4 | **Performance** *(measured — perf-a11y-scan.py)* | Lab Core Web Vitals in the green: LCP ≤ 2.5s, CLS ≤ 0.1, FCP ≤ 1.8s, TTFB ≤ 0.8s, TBT ≤ 200ms; page weight reasonable, no multi-MB hero asset. *(INP measured as a lab proxy — TBT; only real-world field percentiles need live users.)* | 10 |
| 5 | **Accessibility** *(measured — perf-a11y-scan.py: axe-core + keyboard pass)* | axe-core finds no critical/serious WCAG violations; images have alt, fields have labels, contrast ≥4.5:1, one H1, logical order, `<html lang>` set; keyboard focus order reaches controls with a visible focus indicator. | 12 |
| 6 | **Links & errors** *(measured — interaction-scan.py)* | No broken links (HTTP status of every link checked); anchors point where they say; forms actually work. | 8 |
| 7 | **Security & trust basics** *(measured — perf-a11y-scan.py)* | Served over HTTPS with a modern TLS version; no mixed content (`http://` assets on an `https://` page); sensible security headers (HSTS/CSP present); clean redirect chain. | 8 |
| 8 | **Forms usability** | Appropriate input types (email/tel/etc.); inline validation; clear error and success messaging. | 8 |
| 9 | **UI consistency** | Consistent buttons, spacing, colours, and components across pages. | 6 |
| 10 | **Layout & whitespace** | Uncluttered and scannable, not overwhelming; sensible content width and breathing room. | 8 |
| 11 | **Responsive robustness** *(measured — mobile-audit.py + screenshots)* | No layout breakage, horizontal scroll, or overlapping/clipped elements at 320/390/414px, confirmed in the rendered screenshots. | 6 |

> A criterion can generate **more than one finding** (e.g. two separate accessibility gaps), but score
> the criterion once overall. Findings are the fix list; the rubric is the grade.

Grade bands (from report-format.md): A 90–100 · B 80–89 · C 70–79 · D 60–69 · F 0–59.

---

## Worked finding examples (Issue · Impact · Fix)

**UX-01 — No viewport meta tag; site not mobile-responsive** · Impact 5 · Effort 2 · **quick win**
- **Issue:** The homepage `<head>` has no `<meta name="viewport">` tag. Without it, phones render the
  full desktop layout zoomed out to a tiny, unreadable width. *(Viewport = the visible screen area the
  browser lays the page into.)*
- **Impact:** The majority of visitors are on phones; a zoomed-out, pinch-to-read page is the single
  biggest cause of mobile bounce and blocks the primary conversion for most of the audience.
- **Fix:** Add `<meta name="viewport" content="width=device-width, initial-scale=1">` to the `<head>`,
  then verify the layout in the browser's responsive/device mode. **True mobile rendering not
  measured here; check it in device mode after the change.**
- **Evidence:** `<head>` contains `<title>`, `<meta charset>` and stylesheet links, but no
  `<meta name="viewport" …>`.

**UX-02 — Images have no alt text; content invisible to screen readers** · Impact 4 · Effort 2 · **quick win**
- **Issue:** All 14 content images, including the hero and the three product thumbnails, are
  `<img src="…">` with no `alt` attribute. *(Alt text = the text description of an image, read aloud by
  screen readers and shown if the image fails to load.)*
- **Impact:** Visitors using screen readers get nothing where the images are (key product visuals are
  effectively blank), and it's a common accessibility/legal exposure. Search engines also lose the
  image context. **Full accessibility not measured here; this is a markup check only.**
- **Fix:** Add a concise, descriptive `alt` to each meaningful image (e.g.
  `alt="Blue insulated water bottle, 750ml"`); use `alt=""` for purely decorative images. The bundled
  `perf-a11y-scan.py` (axe-core + keyboard pass) confirms the fix and the rest of the WCAG scan.
- **Evidence:** `<img src="/img/hero.jpg">`, with no `alt` on this or any of the 14 images.

**UX-03 — Oversized hero image with no lazy-loading** · Impact 4 · Effort 2 · **quick win**
- **Issue:** The homepage hero is a single **4.2 MB** JPEG (`hero-full.jpg`) served at full resolution
  with no `loading="lazy"` on below-the-fold images. *(Render-blocking/heavy assets delay the page
  appearing.)*
- **Impact:** A multi-megabyte hero is a strong signal of slow first load, especially on mobile data,
  which loses impatient visitors before they see anything. **In a Basic run this is an asset-weight signal,
  not a score; the bundled `perf-a11y-scan.py` measures the real load impact (LCP/TTFB/weight).**
- **Fix:** Export the hero as a compressed, correctly sized image (target well under 300 KB; serve
  WebP/AVIF and a smaller mobile variant), and add `loading="lazy"` to below-the-fold images. Then
  **re-run `perf-a11y-scan.py`** to confirm the improvement.
- **Evidence:** `hero-full.jpg`: 4.2 MB, 4000×2500px, displayed at ~1200px wide.

**UX-04 — Contact form fields have no labels** · Impact 4 · Effort 2 · **quick win**
- **Issue:** On the contact page every input relies on placeholder text only (e.g.
  `<input type="text" placeholder="Your name">`) with no associated `<label>`, and the message field
  uses `type="text"` instead of a `<textarea>`.
- **Impact:** Placeholders vanish once the user types (they lose track of what a field is for),
  screen readers may not announce the field, and the wrong input type worsens the mobile keyboard,
  all adding friction on the page that drives the primary conversion.
- **Fix:** Give every field a real `<label for="…">`, use correct types (`type="email"`,
  `type="tel"`), switch the message to `<textarea>`, and add inline validation with clear error and
  success messages.
- **Evidence:** `<input type="text" placeholder="Your name">`, with no `<label>` anywhere in the form.

**Strength worth noting** (not a finding, but record it): "Every page is served over HTTPS with no
mixed content, the primary nav is consistent across all pages, and `<html lang=\"en\">` is set: solid
trust and consistency basics."

### Anti-patterns to catch (each becomes a finding)
- **Missing viewport meta:** no `<meta name="viewport">`; phones get the zoomed-out desktop layout.
- **Tiny or low-contrast text:** body copy below ~14px or pale grey on white that's hard to read.
- **Images without alt:** meaningful `<img>` with no `alt` attribute.
- **Unlabeled form fields:** inputs with only placeholders, no `<label>`.
- **Mystery-meat navigation:** icon-only or vague nav ("Solutions", "More") that hides where links go.
- **Broken links:** nav or in-body links returning 404, or anchors pointing to the wrong page.
- **Mixed content over HTTPS:** an `https://` page loading images/scripts over plain `http://`.
- **No HTTPS:** the site (or the form-submit endpoint) served over plain `http://`.
- **Layout shift / overlap on mobile:** elements overlapping, clipped, or causing horizontal scroll
  at narrow widths.
- **Giant unoptimised hero images:** multi-megabyte, full-resolution images signalling slow load.
- **Inconsistent buttons/components:** different button styles, spacings, or colours page to page.

---

## Output file format

### File 1: `ux-technical.md` (Markdown)

```markdown
# UX & Technical — [Site name]
Date: [date]
Model: Ananas-Agency Website Audit
Primary goal audited against: [the site's primary conversion]

## Grade: [A–F] ([score]/100)
[one-line verdict, e.g. "Weak — no viewport tag and unlabeled forms make the site hard to use on the phones most visitors are on."]

### Scorecard
| # | Criterion | Pass/Partial/Fail | Weight | Points |
|---|-----------|-------------------|:------:|:------:|
| 1 | Navigation & information architecture | Pass | 12 | 12 |
| ... | ... | ... | ... | ... |
| | **Total** | | **100** | **[score]** |

## Findings
### UX-01. [short title] — Impact [1–5] · Effort [1–5] · [quick win/big bet/fill-in/skip]
- **Issue:** [I, with evidence]
- **Impact:** [what it costs] [+ "not measured" note only if the scan couldn't run (Basic layer)]
- **Fix:** [F, concrete — the exact tag/attribute/change, and how the bundled scan verifies it]
> "[quoted element / attribute / page as evidence]"

[... further findings, impact order ...]

## What's working
- [1–3 genuine strengths]

## Summary
- Findings: [n] ([x] quick wins, [y] big bets, ...)
- Mobile (measured — mobile-audit.py): [fits 320/390/414 · N tap targets <44px · N oversized · N text <12px]
- Perf/a11y/security (measured — perf-a11y-scan.py): [LCP/CLS/FCP/TTFB/TBT · axe WCAG · keyboard focus · HTTPS/TLS/headers/mixed-content]
- Links (measured — interaction-scan.py): [N checked · N broken]
- Top priority: [UX-ID — one line]
```

### File 2: `ux-technical.html` (styled, share-ready)

A single **self-contained** `.html` file (all CSS inline in one `<style>` block, **no external assets
and no JavaScript**). Use the **shared design system**: the exact `<style>` block and page frame from
[rules-snapshot.md](../../../0%20Site%20Snapshot/site-snapshot/references/rules-snapshot.md), reproduced
in full below so this skill is self-contained. Only these differ from the snapshot page: the `<title>`,
the header, the `utm_content=ux-technical` in the two brand links, and the section content.

Components:
- **A grade section first:** the letter grade in a `.grade` chip (class `a`/`b`/`c`/`d`/`f`), the score,
  a one-line verdict, and the **scorecard `<table>`** (criteria × pass/partial/fail × weight × points).
- **A Findings section:** one `.card` per finding. Card header: the `.id` chip (`UX-01`), the short
  title, an **Impact meter** (`<span class="scorewrap"><span class="meter"><i style="width:NN%"></i></span><span class="scoreno">Impact X/5</span></span>`,
  width = Impact/5×100), and the **priority `.tag`** (`quickwin` / `bigbet` / `fillin` / `skip`). Body:
  Issue / Impact / Fix as `.row`s (append `· Effort X/5` in the Impact row via `<span class="effort">`),
  and the quoted evidence in a `<blockquote>`. If a scan couldn't run (Basic layer), say **"not measured"**
  in the row; don't name a third-party tool.
- **A "What's working" section:** `.row`s or `ul.clean` of strengths.
- **A Summary section:** findings count, a one-line measured-tools summary (or a Basic-layer "not measured"
  note if the scans couldn't run), and the top priority (cited by ID).

**Navigation & hints (required):** cross-link other deliverables and tooltip every ID and shorthand term
(IIF, CRO, SEO, UX, CTA, MSG/CRO/SEO/UX, quadrant labels), every occurrence, per
[report-format.md](report-format.md). **No `pagenav`** mid-session; end with the Print hint.

Finding card pattern:
```html
<article class="card">
  <h3><span class="id">UX-01</span> No viewport meta tag; site not mobile-responsive
      <span class="scorewrap"><span class="meter"><i style="width:100%"></i></span><span class="scoreno">Impact 5/5</span></span>
      <span class="tag quickwin">quick win</span></h3>
  <div class="row"><span class="k">Issue</span>The homepage &lt;head&gt; has no &lt;meta name="viewport"&gt; tag, so phones render the desktop layout zoomed out.</div>
  <div class="row"><span class="k">Impact</span>Most visitors are on phones and get a pinch-to-read page — the biggest cause of mobile bounce. <span class="effort">· Effort 2/5</span></div>
  <div class="row"><span class="k">Fix</span>Add &lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt; to the &lt;head&gt;; the bundled mobile-audit.py confirms the fit at 320/390/414.</div>
  <blockquote>"&lt;head&gt; has &lt;title&gt; and stylesheet links but no &lt;meta name=&quot;viewport&quot;&gt;"</blockquote>
</article>
```

Full page (reproduce the shared `<style>` block verbatim; it is identical suite-wide):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UX &amp; Technical — [Site name]</title>
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
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=ux-technical" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=ux-technical" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>UX &amp; Technical — [Site name]</h1>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit &nbsp;·&nbsp; <b>Grade:</b> [A–F] ([score]/100)</div>
  </header>

  <section class="block">
    <h2 class="section"><span class="no">1</span> Grade &amp; scorecard</h2>
    <div class="row"><span class="grade d">D</span> <b>64/100</b> — [one-line verdict]</div>
    <div class="tablewrap"><table>
      <tr><th>#</th><th>Criterion</th><th>Result</th><th>Weight</th><th>Points</th></tr>
      <tr><td>1</td><td>Navigation &amp; information architecture</td><td>Pass</td><td>12</td><td>12</td></tr>
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
    <h2 class="section"><span class="no">4</span> Summary</h2>
    <div class="row"><span class="k">Findings</span>[n] ([x] quick wins, [y] big bets, …)</div>
    <div class="row"><span class="k">Mobile (measured)</span>fits 320/390/414px · [N] tap targets &lt;44px · [N] oversized · [N] text &lt;12px</div>
    <div class="row"><span class="k">Perf / a11y / security (measured)</span>LCP/CLS/FCP/TTFB/TBT · axe WCAG · keyboard focus · HTTPS/TLS/headers/mixed-content</div>
    <div class="row"><span class="k">Links (measured)</span>[N] checked · [N] broken</div>
    <div class="row"><span class="k">Top priority</span>[UX-ID — one line]</div>
  </section>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=ux-technical" target="_blank" rel="noopener">
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

================================================================================

# 6. Design & Visual

**Skill ID:** `design-visual`

# Design & Visual (Ananas-Agency — Website Audit)

## Goal

Judge how the website **actually looks** (whether the rendered design leads the eye to the main action,
feels coherent and current, and reads as professional and trustworthy), and turn every weakness into a
prioritised, fixable **Finding**. Deliver a graded Design & Visual scorecard (0–100 → letter grade) and a
list of `DSN-` findings in **Issue · Impact · Fix** format, each rated on Impact and Effort so the user
knows what to fix first.

This is the one dimension a **static-HTML read can't do**: you have to see the page. So it works from two
inputs: the **measured design tokens** (objective counts, from the bundled `scripts/design-scan.py`) and a
**visual read** of the rendered desktop + mobile screenshots (expert judgement). Written for **business
owners and marketers**: plain language, no unexplained jargon, and every finding tied to a real effect on
their visitors.

## Inputs

- **Site Snapshot** (from Skill 0). Paste it if you have it; it anchors the analysis to the site's
  **primary conversion goal** and audience. If it's missing, do a quick mini-snapshot first (fetch the
  homepage; establish name, what it does, primary goal, audience) so your findings have an anchor, but
  don't run the full intake.
- **The URL**: the homepage (the main page gets the full visual audit); optionally a key landing/product
  page the user cares about.
- **Brand guidelines** (optional): the company's real colours, fonts, and logo. **Needed for a true
  "off-brand" call.** Without them, judge general design quality and internal consistency only, and ask
  the user for their brand guidelines if they want brand-*fit* assessed (see Critical rules).

## The core unit: a Finding (Issue · Impact · Fix)

Every observation is a Finding. See [report-format.md](report-format.md) for the full definition,
the Impact/Effort scales (1–5), and the priority quadrants (quick win / big bet / fill-in / skip). In
short:
- **Issue**: the specific design problem, with **evidence**: a measured token ("design-scan: 11 distinct
  button styles") and/or the visual observation ("the hero uses a 2012-era glossy gradient and a drop
  shadow on every card").
- **Impact**: what it costs (visitors don't know where to look, the site reads as dated or amateur, trust
  erodes via the aesthetic-usability effect). Rated **Impact 1–5**.
- **Fix**: the concrete design change, ideally with the target ("collapse to two button styles, one
  primary, one secondary").
- **Effort 1–5** and a **priority quadrant** derived from Impact × Effort.

Give each finding an ID: `DSN-01`, `DSN-02`, … in impact order.

## Conversation flow

### Step 1: Load context and identify the page

Take the Site Snapshot (or build the mini one) and confirm the URL to render (the homepage, plus any key
page the user names). Keep the site's **primary goal** and **audience** in mind. Good design is design
that leads the eye *toward the main action* and fits *who the site is for*.

### Step 2: Run the design scan (headless render — the correct way)

Don't guess how the page looks from the markup; **render it and measure it**. If Playwright is available
(`pip install playwright && playwright install chromium`, which bundles its own Chromium, cross-platform), run the bundled tool:

```
python scripts/design-scan.py <URL> --pages <one-article,one-service-page,one-case-study> --out <folder>
```

Pass `--pages` with **one representative page per key interior template**: an **article/blog post**, a
**service/offering page**, and a **case study** (pick them from the Snapshot's page inventory or the SEO
sweep's page types). A site's biggest design and readability problems usually live on these template pages,
not the homepage, so the tool renders each one, **screenshots it** (`page-<slug>.png`), compares tokens for
**cross-page consistency** (same typeface/palette/button system, or drift?), and **measures readability** per
page: body **text-alignment**, approximate **characters-per-line** (the 45-75 target), and **words-per-visual**
(a wall-of-text signal). This is what lets you judge the interior templates, not just the homepage.

It renders in headless Chrome at desktop (1440px) and mobile (390px) and produces (full detail and thresholds
in [references/rules-design-visual.md](references/rules-design-visual.md), "The design scan"):
- **`design-tokens.json` / `design-scan.md`**: the MEASURED tokens: the **typeface(s)**, the **count of
  distinct font sizes** (and weights), the **colour palette** (distinct text colours + backgrounds), and the
  **count of distinct BUTTON STYLES** (a coherence signal, fewer is more consistent). These counts are objective.
- **`design-desktop.png`** and **`design-mobile.png`**: full-page homepage screenshots for the visual read.
- With `--pages`: **`page-<slug>.png`** per interior template, plus `design-pages.json` with the cross-page
  token consistency and the **per-page readability** (alignment, chars-per-line, words-per-visual).

### Step 2b: Do the visual read — actually LOOK at the screenshots

Open `design-desktop.png` and `design-mobile.png` and **look at them**. This is the expert-judgement half:
grounded in the **benchmarks-2026.md §4 UI/UX principles** (Nielsen's heuristics, visual hierarchy,
consistency/Jakob's Law, aesthetic-usability, Stanford Web Credibility), judge visual hierarchy, whitespace,
typography, imagery quality, modern-vs-dated, colour harmony, brand coherence, and the trust/polish the
design conveys, on both desktop and the phone. Cross-reference the measured tokens (e.g. a "cluttered,
no focal point" observation next to "design-scan: 9 distinct font sizes, 11 button styles"). Run the three
fast tests first (Step 3).

**If no headless browser is available**, say so and fall back to a **user-provided screenshot** of the page.
If none is available either, mark the visual read **"not assessed"** and ask for a screenshot; never invent
what the page looks like. The measured token counts also require the render, so without either they're
unavailable too.

### Step 2c: Read the interior templates (not just the homepage)

Open each `page-<slug>.png` from the `--pages` render and read the interior templates the way you read the
homepage. This is where the biggest design problems on real sites hide. For each template, judge:
- **Layout & structure:** is the page designed (sections, cards, a clear structure), or is it a long
  undifferentiated column that reads like a pasted document?
- **Text density & visual variety:** does it mix text with graphics, diagrams, and varied section layouts,
  or is it a wall of text? The measured **words-per-visual** is the signal (a service or article page with
  hundreds of words and almost no visuals is text-heavy). This is the common offering-page failure.
- **What the page delivers:** a service/offering page should look like it answers *"what the client gets"*,
  not read like an essay on the technology or the process.
- **Readability (measured):** cross-check the numbers. **Centred body text**, or **chars-per-line well
  outside 45-75** (benchmarks-2026.md §4), makes a page hard to read regardless of how it looks. Quote the
  measured value in the finding.

Turn each template-level problem into a `DSN-` finding with the screenshot and the measured readability
value as evidence (e.g. *"the article template centres its body text at ~120 chars/line, which is hard to
read"*, or *"the service page is a wall of text: ~140 words per visual, no diagrams or section variety"*).
These are page-**template** findings, so one finding per template pattern, not one per page. If a readability
problem is really about legibility and line length, note that **UX & Technical** covers it too and align the
two.

### Step 3: Run the design fast tests

Apply the fast diagnostic tests before the full rubric. Details and examples in
[references/rules-design-visual.md](references/rules-design-visual.md):
- **The squint test**: blur the page (or squint): does **one clear focal point** emerge and lead the eye
  to the primary action, and is the layout balanced, or does everything compete (or nothing stands out)?
- **The 5-second impression**: glance for five seconds: does it look **modern, professional and
  trustworthy**, or dated, generic, or amateur?
- **The consistency count**: from the scan, how many **button styles / font sizes / colours**? A tight
  set signals a coherent design system; a sprawling one signals an ad-hoc, inconsistent build.

### Step 4: Work the rubric and generate findings

Go through the Design & Visual rubric criteria (see the reference, "Scoring rubric"): visual hierarchy,
design-system consistency, typography, colour & palette, layout/grid/alignment, whitespace & density,
imagery & media quality, modern-vs-dated, brand coherence & credibility, and mobile visual quality. For
each weakness, write a Finding (IIF): **cite the measured number as evidence where it applies AND the
visual observation**, with an Impact and Effort rating and a quadrant. **Also note genuine strengths**, so
the report isn't only problems.

### Step 5: Score the dimension

Rate each rubric criterion Pass / Partial / Fail. **Each criterion's "Pass" is the 2026 standard from
[benchmarks-2026.md](benchmarks-2026.md)** (§4 UI/UX & usability: one focal point, visual hierarchy,
consistency/Jakob's Law, ≥16px / 45–75-char / 1.5 readable type, aesthetic-minimalist design, and the
aesthetic-usability effect on trust), so cite the benchmark in findings. Apply the weights, and total to a
**0–100 score**; map to a **letter grade** (A–F, bands in [report-format.md](report-format.md)). Show the
criteria table so the grade is explainable. State plainly that the **token counts are measured** but the
**visual judgement is expert-subjective**, grounded in the §4 UI/UX principles, not a lab metric.

### Step 6: Deliver the files

Generate `design.md` and a styled, self-contained `design.html` (embedding the two rendered screenshots and
the measured tokens) and share them. Format, the finding card component, the design-tokens block, and the
scorecard layout: see the reference, "Output file format". End the HTML with the Print hint; **no
`pagenav`** mid-session.

### Step 7: Add to the Website Audit Report & hand off

Record the **Design & Visual** section (grade + criteria + findings) into the internal running **Website
Audit Report** (do not create/show a report file now; that's the Action Report skill's job at the end).
Format and section order: [report-format.md](report-format.md). Tell the user the remaining analyses are
any of **Messaging & Clarity**, **Conversion (CRO)**, **SEO & Content**, or **UX & Technical**, and that
**Action Report** ties them together at the end.

## Critical rules

1. **Measured vs. expert-subjective: say which is which.** The design-token **counts** (button styles,
   font sizes, colours, typefaces) are **objective and measured** by `design-scan.py`. The **visual
   judgement** (hierarchy, whitespace, modern-vs-dated, imagery, polish) is **expert-subjective**,
   grounded in the **benchmarks-2026.md §4 UI/UX** principles (Nielsen's heuristics, visual hierarchy,
   consistency, aesthetic-usability), **not a lab metric**. Label it as expert judgement; never dress an
   opinion up as a measurement.
2. **A true "off-brand" call needs brand guidelines.** Judging that a design is *off-brand* requires the
   company's real **colours, fonts, and logo**. Without them, judge **general design quality + internal
   consistency** only (does it hold together with itself?), and **ask the user for brand guidelines** if
   they want brand-fit assessed. Never assert a colour or font is "wrong for the brand" with no reference.
3. **Look, don't guess.** Base the visual read on the **rendered screenshots** (or a user-supplied one).
   If no headless browser and no screenshot are available, mark the visual read **"not assessed"** and ask
   for one; **never invent what the page looks like**.
4. **Evidence, always: the number and the eye.** Every finding cites the measured token where relevant
   ("design-scan: 11 button styles") **and/or** the concrete visual observation ("the hero is a glossy
   2012-era gradient"). No vague "the design could be better".
5. **Anchor to the primary goal and audience.** Judge the design toward the site's one main conversion and
   who it's for: a focal point that leads to the main action, and an aesthetic that fits the audience.
6. **Fixes are concrete.** Give the specific change and target (e.g. "collapse to two button styles",
   "cut to one display + one body typeface", "replace the generic stock photo with a real product shot"),
   not "make it look nicer".
7. **Impact + Effort on every finding.** So the Action Report can place it on the matrix.
8. **Name strengths too.** Note what already works visually, so the grade and the report are balanced and
   credible.
9. **Plain language.** Business owners are the audience; explain any shorthand (visual hierarchy = what the
   eye is led to first; design system = a consistent set of colours/type/buttons; focal point = the one
   thing that stands out; whitespace = the empty breathing room around elements).


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

---

## Skill reference materials: design-visual

### Reference: rules-design-visual.md

# Design & Visual Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](report-format.md). This reference
adds the design-specific fast tests, the design scan, the scoring rubric, worked finding examples, and the
HTML output format.

## What is measured vs. what is expert judgement (read this first)

This dimension mixes two very different kinds of evidence, and the **honesty rule** requires you keep them
apart:

**MEASURED, objective, from `scripts/design-scan.py`.** The token **counts** are computed from the
rendered page's real styles, so quote them as facts:
- the **typeface(s)** actually in use (top font families),
- the **count of distinct font sizes** (and the weights present),
- the **colour palette**: the count of distinct text colours and backgrounds, plus the top ones,
- the **count of distinct button styles**: a design-system coherence signal (fewer is more consistent).

**EXPERT-SUBJECTIVE: the visual read, from looking at the screenshots.** Whether the hierarchy leads the
eye, whether the layout is balanced, whether the imagery is quality, whether it looks modern or dated, and
whether it reads as trustworthy, these are **expert judgements grounded in the benchmarks-2026.md §4
UI/UX principles** (Nielsen's 10 heuristics, visual hierarchy, consistency/Jakob's Law, aesthetic &
minimalist design, the aesthetic-usability effect, Stanford Web Credibility), **not lab metrics**. Label
them as judgement, never as measurement.

**A true "off-brand" call needs brand guidelines.** Deciding a colour or font is *off-brand* requires the
company's real **colours, fonts, and logo**. Without them, judge **general design quality + internal
consistency** only, and **ask the user for their brand guidelines** if they want brand-fit assessed.

**If there's no headless browser**, fall back to a **user-provided screenshot**; if none, mark the visual
read **"not assessed"** and ask for one; never invent what the page looks like.

| To assess… | How | In the report, mark |
|------------|-----|---------------------|
| Design tokens (colours, fonts, sizes, button styles) | **`scripts/design-scan.py`** (bundled) | **measured** (or "not available" if no browser/screenshot) |
| Visual hierarchy, whitespace, imagery, modern-vs-dated, polish | **Look at the rendered screenshots** | **expert judgement** (benchmarks §4 UI/UX) |
| Brand-fit / "off-brand" | Needs the company's **brand guidelines** | "not assessed — brand guidelines needed" |

---

## The design scan (the correct way to check "how does it look?")

Static HTML tells you nothing about how a page actually looks; that depends on CSS, images, and layout at a
real screen width. So render the page and both measure its tokens and capture it for the eye.

**Run it** (needs Playwright: `pip install playwright && playwright install chromium`; it bundles its own Chromium, no browser to install):
```
python scripts/design-scan.py <URL> --pages <one-article,one-service-page,one-case-study> --out <folder>
```
It renders the homepage at desktop (1440px) and mobile (390px, 2× density), extracts the design tokens from
computed styles, and saves full-page screenshots. With `--pages`, it also renders **one representative page
per key interior template** (an article, a service/offering page, a case study), screenshots each, and
measures their readability. Interior templates are where most real design problems live, so always pass them.

**What it produces:**

| Artefact | What it gives you |
|----------|-------------------|
| **`design-tokens.json`** | The full measured homepage tokens (raw counts + top colours/fonts/sizes/button styles). |
| **`design-scan.md`** | A readable summary: typeface(s), # distinct font sizes + weights, # distinct colours, # distinct button styles, plus the interior-template readability table. |
| **`design-desktop.png`** / **`design-mobile.png`** | Full-page homepage renders for the visual read. |
| **`page-<slug>.png`** (with `--pages`) | Full-page render of each interior template for the visual read. |
| **`design-pages.json`** (with `--pages`) | Cross-page token consistency + **per-page readability** (alignment, chars-per-line, words-per-visual). |

**Interior-template readability thresholds** (from `design-pages.json`; benchmarks-2026.md §4):

| Signal | Good | Flag it |
|--------|------|---------|
| **Body text-alignment** | `left` (or `justify` with care) | `center` on long body copy: hard to read (a `DSN-`/`UX-` finding) |
| **Characters per line** | ~45-75 | > 75 (lines too long) or < 40 (too narrow) |
| **Words per visual** | mixed (text + graphics) | very high (e.g. 100+): a wall of text with no diagrams or section variety |

**The consistency signals to read off the tokens** (fewer is more coherent; these are guides, not hard
thresholds):

| Token | Coherent | Getting noisy | Ad-hoc |
|-------|----------|---------------|--------|
| **Button styles** | 1–3 (primary/secondary/tertiary) | 4–6 | 7+ (no design system) |
| **Distinct font sizes** | ~4–8 (a type scale) | 9–12 | 13+ (no scale) |
| **Typefaces** | 1–2 (or a deliberate pair) | 3 | 4+ |
| **Core palette** | a controlled set (a few brand + neutrals) | drifting | dozens of unrelated colours |

**Then LOOK.** Open both screenshots and judge the things the counts can't: does one focal point emerge,
is the composition aligned and balanced, is there breathing room or is it crammed, is the imagery custom
and sharp or generic/low-res, does it look current or dated, is the colour harmonious, and does the whole
read as professional and trustworthy, on desktop **and** on the phone. Turn each problem into a `DSN-`
finding that pairs the number with the observation.

---

## The design fast tests

Run these fast before the full rubric; they surface the biggest issues quickly.

### The squint test
Blur your eyes (or mentally squint) at the rendered page. Does **one element, the primary action,
emerge as the clear focal point**, so the eye lands on it first, and does the overall layout feel
**balanced** (weight distributed, not lopsided or crammed to one side)? If everything competes at the same
visual weight, nothing stands out, or the composition is unbalanced, the **visual hierarchy** isn't guiding
the visitor. This is the visual analogue of the messaging 5-second test.

### The 5-second impression
Glance at the page for five seconds, as a first-time visitor would. Does it look **modern, professional,
and trustworthy**, or dated, generic, or amateur? First impressions form in well under a second and drive
credibility (the *aesthetic-usability effect*: a cleaner, more current design is also **trusted** more;
Stanford Web Credibility). Note the gut reaction and what drives it (dated gradients, clip-art, clutter, a
tidy modern grid).

### The consistency count
From the scan, count the **button styles**, the **distinct font sizes**, and the **distinct colours**. A
tight set (a few buttons, a real type scale, a controlled palette) signals a coherent **design system**; a
sprawling set (a dozen button styles, fifteen font sizes, colours everywhere) signals an ad-hoc build that
will read as inconsistent and unpolished. Quote the numbers.

---

## Scoring rubric (weights sum to 100)

Rate each criterion **Pass** (full weight), **Partial** (half), or **Fail** (0). Sum → 0–100 → letter
grade. Always show this table in the deliverable so the grade is explainable. Criteria marked
**(measured)** are anchored to a `design-scan.py` token count; the rest are **expert judgement** from the
rendered screenshots (benchmarks §4 UI/UX); note that in the finding.

**Judge each criterion across the homepage AND the sampled interior templates** (see "Read the interior
templates" in the SKILL). A template-level problem counts against the relevant criterion, e.g. a wall-of-text
service page hits **Visual hierarchy** and **Whitespace & density**; centred body copy or over-long lines on
an article hit **Typography**. Don't let a polished homepage hide broken interior templates.

| # | Criterion | What "Pass" looks like | Weight |
|---|-----------|------------------------|:------:|
| 1 | **Visual hierarchy** | One clear focal point; the eye is led to the primary action; size, colour, and spacing rank importance. | 12 |
| 2 | **Design-system consistency** *(measured — # button styles)* | Buttons, components, and spacing are consistent; a tight, reused set (few button styles), not ad-hoc. | 12 |
| 3 | **Typography** *(measured — # font families / # font sizes)* | A coherent typeface (or a deliberate pair) and a tight type scale; legible size and line length. | 12 |
| 4 | **Colour & palette** *(measured — # distinct colours)* | A controlled, harmonious, on-brand palette with sufficient contrast; not a scatter of unrelated colours. | 10 |
| 5 | **Layout, grid & alignment** | Structured, aligned, balanced composition; elements sit on a grid, edges line up. | 10 |
| 6 | **Whitespace & density** | Uncluttered, with breathing room; content isn't crammed or overwhelming. | 10 |
| 7 | **Imagery & media quality** | High-quality, relevant, consistent imagery — custom over generic stock, sharp resolution, no distortion. | 8 |
| 8 | **Modern vs dated** | Follows current design conventions; doesn't look visibly old (no 2010-era gradients/bevels/clip-art). | 8 |
| 9 | **Brand coherence & credibility** | Professional, trustworthy, a consistent identity — the aesthetic-usability effect: good design is trusted more. | 10 |
| 10 | **Mobile visual quality** *(measured — mobile render)* | The design itself (not just the responsive layout) holds up and looks good on a phone. | 8 |

> A criterion can generate **more than one finding** (e.g. two separate imagery problems), but score the
> criterion once overall. Findings are the fix list; the rubric is the grade.

Grade bands (from report-format.md): A 90–100 · B 80–89 · C 70–79 · D 60–69 · F 0–59.

---

## Worked finding examples (Issue · Impact · Fix)

**DSN-01 — 11 distinct button styles; no coherent design system** · Impact 3 · Effort 3 · **big bet**
- **Issue:** `design-scan.py` measured **11 distinct button styles** on the homepage (different fills,
  border radii, and padding), and the screenshots confirm it: the hero CTA, the nav button, and the card
  buttons all look different. *(Design system = a consistent, reused set of colours, type, and buttons.)*
- **Impact:** An ad-hoc button set reads as unpolished and makes the primary action harder to spot; every
  button competing dilutes the one that matters, and inconsistency quietly erodes trust (aesthetic-usability
  effect).
- **Fix:** Collapse to **two button styles**, one primary (the main CTA) and one secondary, with a single
  shared radius, padding, and colour rule, applied site-wide. Define them once as reusable components.
- **Evidence:** design-scan: 11 distinct button styles; buttonRadii include 0px, 4px, 8px, 24px, 999px.

**DSN-02 — Dated hero: glossy gradient, bevels, and a 2012-era look** · Impact 4 · Effort 3 · **big bet**
- **Issue:** The hero (desktop screenshot) uses a glossy top-to-bottom gradient, beveled buttons with
  drop shadows, and a skeuomorphic badge: visual conventions that read as roughly a decade old.
- **Impact:** The 5-second impression is "dated", which via the aesthetic-usability effect lowers perceived
  quality and trust before the visitor reads a word, costly on the primary entry page. *(Expert judgement
  against benchmarks §4 UI/UX, not a lab metric.)*
- **Fix:** Modernise the hero to current conventions: flat or subtly-layered colour, a clean sans type
  scale, generous whitespace, a single high-contrast primary button, and a sharp real photograph or a
  simple custom graphic instead of the badge.
- **Evidence:** `design-desktop.png`: glossy gradient hero + beveled/drop-shadowed buttons.

**DSN-03 — Cluttered layout with no clear focal point** · Impact 4 · Effort 3 · **big bet**
- **Issue:** The squint test fails: on the blurred desktop screenshot nothing stands out; the first screen
  packs a headline, two promo banners, a carousel, and six equal-weight cards with almost no whitespace.
  The scan backs this up: **9 distinct font sizes**, so text weight doesn't rank anything.
- **Impact:** With no focal point the eye has nowhere to land and the primary action gets lost in the
  noise; visitors don't know where to look or what to do next, hurting the main conversion.
- **Fix:** Establish one focal point: give the hero and its single primary CTA room and dominant weight,
  demote the promos below the fold, add generous whitespace, and cut the type scale to ~5 sizes so size
  signals importance.
- **Evidence:** design-scan: 9 distinct font sizes; `design-desktop.png`: dense first screen, no
  dominant element.

**DSN-04 — Low-quality generic stock imagery** · Impact 3 · Effort 2 · **fill-in**
- **Issue:** The three "team"/"service" images are recognisable generic stock photos (a posed handshake, a
  smiling headset agent), one visibly stretched out of its aspect ratio.
- **Impact:** Generic stock reads as impersonal and less credible than real imagery, and the distortion
  looks careless; both weaken the professional, trustworthy impression the page needs to make.
- **Fix:** Replace with real, on-brand photography (the actual team, product, or work) at correct aspect
  ratio and resolution; if stock is unavoidable, choose authentic, non-cliché shots and keep them
  consistent in tone.
- **Evidence:** `design-desktop.png`: posed-handshake stock image, ~third image stretched horizontally.

**Strength worth noting** (not a finding, but record it): "The palette is controlled (design-scan shows a
tight core of a brand navy, one warm accent, and neutral greys), and the type is a single clean sans on a
consistent scale; the base design system is coherent."

### Anti-patterns to catch (each becomes a finding)
- **Too many fonts / sizes:** 3+ typefaces or a sprawling, scale-less set of font sizes (measured).
- **Too many colours:** a scatter of unrelated colours with no controlled core palette (measured).
- **Inconsistent buttons:** many different button styles, radii, and sizes; no reusable component set
  (measured).
- **Generic stock photos:** cliché, impersonal, or distorted imagery instead of real, on-brand visuals.
- **Cluttered / dense layout:** everything crammed together, no whitespace, overwhelming first screen.
- **Poor alignment:** elements off-grid, ragged edges, nothing lining up.
- **Dated gradients / shadows / bevels:** glossy gradients, heavy drop shadows, skeuomorphic or clip-art
  styling that reads as a decade old.
- **No clear focal point:** everything the same visual weight; the eye has nowhere to land.
- **Low-contrast decoration over text:** decorative imagery or busy backgrounds behind copy that hurt
  legibility (ties to §3 Accessibility contrast).

---

## Output file format

### File 1: `design.md` (Markdown)

```markdown
# Design & Visual — [Site name]
Date: [date]
Model: Ananas-Agency Website Audit
Graded against: benchmarks-2026.md (§4 UI/UX)
Primary goal audited against: [the site's primary conversion]

## Grade: [A–F] ([score]/100)
[one-line verdict, e.g. "Fair — a coherent palette undermined by a dated hero, a cluttered first screen, and 11 different button styles."]

### Scorecard
| # | Criterion | Pass/Partial/Fail | Weight | Points |
|---|-----------|-------------------|:------:|:------:|
| 1 | Visual hierarchy | Fail | 12 | 0 |
| ... | ... | ... | ... | ... |
| | **Total** | | **100** | **[score]** |

### Design tokens (measured — design-scan.py)
- **Typeface(s):** [e.g. Inter (body), Poppins (headings)]
- **Distinct font sizes:** [n]  ·  weights: [list]
- **Palette:** [n] text colours · [n] backgrounds — core: [top few hex/rgb]
- **Distinct button styles:** [n]  (fewer is more consistent)

## Findings
### DSN-01. [short title] — Impact [1–5] · Effort [1–5] · [quick win/big bet/fill-in/skip]
- **Issue:** [I — the measured number and/or the visual observation]
- **Impact:** [what it costs] [+ "expert judgement" note where it's a visual call]
- **Fix:** [F, concrete — the specific design change and target]
> [evidence — e.g. "design-scan: 11 button styles" / "design-desktop.png — glossy gradient hero"]

[... further findings, impact order ...]

## What's working
- [1–3 genuine strengths]

## Summary
- Findings: [n] ([x] quick wins, [y] big bets, ...)
- Design tokens (measured): [typeface(s) · N font sizes · N colours · N button styles]
- Visual read: [expert judgement — benchmarks §4 UI/UX; or "not assessed — no render/screenshot"]
- Top priority: [DSN-ID — one line]
```

### File 2: `design.html` (styled, share-ready)

A single **self-contained** `.html` file (all CSS inline in one `<style>` block, **no external assets and
no JavaScript**, except the two rendered screenshots referenced by relative `src`, which ship in the same
folder/ZIP). Use the **shared design system**: the exact `<style>` block and page frame from
[rules-messaging-clarity.md](../../../2%20Messaging%20Clarity/messaging-clarity/references/rules-messaging-clarity.md),
reproduced in full below so this skill is self-contained. Only these differ: the `<title>`, the header, the
`utm_content=design-visual` in the two brand links, and the section content.

Components:
- **A grade section first:** the letter grade in a `.grade` chip (class `a`/`b`/`c`/`d`/`f`), the score,
  a one-line verdict, and the **scorecard `<table>`** (criteria × pass/partial/fail × weight × points).
- **A "Design tokens (measured)" section:** the palette rendered as small inline **swatches** (inline
  styles), the **typeface(s)**, the **# of distinct font sizes**, and the **# of distinct button styles**.
- **A "Rendered screenshots" section:** the desktop and mobile full-page renders embedded as `<img>` in a
  flex row, each with its `<figcaption>` label **above** the image (caption first in the `<figure>`, then the
  `<img>`). Mid-session use the flat path `<img src="design-desktop.png">` (the PNG
  sits beside this file). In the **final bundle** the screenshots move to `assets/`, so the Action Report's
  regeneration repoints them to `assets/design-desktop.png` / `assets/design-mobile.png` (see
  [report-format.md](report-format.md), "Deliverables bundle").
- **A Findings section:** one `.card` per finding. Card header: the `.id` chip (`DSN-01`), the short
  title, an **Impact meter** (`<span class="scorewrap"><span class="meter"><i style="width:NN%"></i></span><span class="scoreno">Impact X/5</span></span>`,
  width = Impact/5×100), and the **priority `.tag`** (`quickwin` / `bigbet` / `fillin` / `skip`). Body:
  Issue / Impact / Fix as `.row`s (append `· Effort X/5` in the Impact row via `<span class="effort">`),
  and the evidence in a `<blockquote>` (the measured number and/or the screenshot reference). Where a claim
  is a visual call, say **"expert judgement"** in the row.
- **A "What's working" section:** `.row`s or `ul.clean` of strengths.
- **A Summary section:** findings count, the measured tokens in one line, a "visual read" note, and the
  top priority (cited by ID).

**Navigation & hints (required):** cross-link other deliverables and tooltip every ID and shorthand term
(IIF, CRO, SEO, UX, **DSN**, CTA, MSG/CRO/SEO/UX/DSN, quadrant labels), every occurrence, per
[report-format.md](report-format.md). **No `pagenav`** mid-session; end with the Print hint.

Design-tokens block pattern (inline swatches):
```html
<div class="row"><span class="k">Palette</span>
  <span style="display:inline-block;width:14px;height:14px;background:#0a2147;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #0a2147 &nbsp;
  <span style="display:inline-block;width:14px;height:14px;background:#d99a2b;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #d99a2b &nbsp;
  <span style="display:inline-block;width:14px;height:14px;background:#f5f5f7;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #f5f5f7
</div>
<div class="row"><span class="k">Typeface(s)</span>Inter (body) · Poppins (headings)</div>
<div class="row"><span class="k">Distinct font sizes</span>9</div>
<div class="row"><span class="k">Distinct button styles</span>11 <span class="effort">· fewer is more consistent</span></div>
```

Rendered-screenshots block pattern:
```html
<div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px">
  <figure style="margin:0;flex:1 1 380px">
    <figcaption class="verdict-common" style="margin-bottom:6px">Desktop (1440px)</figcaption>
    <img src="design-desktop.png" alt="Full-page desktop render" style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:2px">
  </figure>
  <figure style="margin:0;flex:0 1 220px">
    <figcaption class="verdict-common" style="margin-bottom:6px">Mobile (390px)</figcaption>
    <img src="design-mobile.png" alt="Full-page mobile render" style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:2px">
  </figure>
</div>
```

Finding card pattern:
```html
<article class="card">
  <h3><span class="id">DSN-01</span> 11 distinct button styles; no coherent design system
      <span class="scorewrap"><span class="meter"><i style="width:60%"></i></span><span class="scoreno">Impact 3/5</span></span>
      <span class="tag bigbet">big bet</span></h3>
  <div class="row"><span class="k">Issue</span>design-scan measured 11 distinct button styles; the screenshots confirm the hero, nav, and card buttons all look different.</div>
  <div class="row"><span class="k">Impact</span>An ad-hoc button set reads as unpolished and makes the primary action harder to spot. <span class="effort">· Effort 3/5</span></div>
  <div class="row"><span class="k">Fix</span>Collapse to two button styles — one primary, one secondary — with a shared radius, padding, and colour, applied site-wide.</div>
  <blockquote>design-scan: 11 distinct button styles; radii 0/4/8/24/999px</blockquote>
</article>
```

Full page (reproduce the shared `<style>` block verbatim; it is identical suite-wide):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Design &amp; Visual — [Site name]</title>
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
    <a class="pkgname" href="https://website-audit-suite.ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=design-visual" target="_blank" rel="noopener">Website Audit Suite</a>
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=design-visual" target="_blank" rel="noopener">
      <span class="byline">by</span>
      <img class="brandlogo" src="https://ananas-agency.com/wp-content/uploads/2025/05/ananas-agency-logo-no-background-for-black.png" alt="Ananas Agency">
    </a>
  </div>
</div>

<div class="wrap">
  <header class="doc">
    <h1>Design &amp; Visual — [Site name]</h1>
    <div class="meta"><b>Date:</b> [date] &nbsp;·&nbsp; <b>Model:</b> Ananas-Agency Website Audit &nbsp;·&nbsp; <b>Grade:</b> [A–F] ([score]/100) &nbsp;·&nbsp; <b>Graded against:</b> benchmarks-2026.md (§4 UI/UX)</div>
  </header>

  <section class="block">
    <h2 class="section"><span class="no">1</span> Grade &amp; scorecard</h2>
    <div class="row"><span class="grade c">C</span> <b>72/100</b> — [one-line verdict]</div>
    <div class="tablewrap"><table>
      <tr><th>#</th><th>Criterion</th><th>Result</th><th>Weight</th><th>Points</th></tr>
      <tr><td>1</td><td>Visual hierarchy</td><td>Fail</td><td>12</td><td>0</td></tr>
      <!-- one row per criterion -->
      <tr><td></td><td><b>Total</b></td><td></td><td><b>100</b></td><td><b>72</b></td></tr>
    </table></div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">2</span> Design tokens (measured)</h2>
    <div class="row"><span class="k">Palette</span>
      <span style="display:inline-block;width:14px;height:14px;background:#0a2147;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #0a2147 &nbsp;
      <span style="display:inline-block;width:14px;height:14px;background:#d99a2b;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #d99a2b &nbsp;
      <span style="display:inline-block;width:14px;height:14px;background:#f5f5f7;border:1px solid #ccc;border-radius:2px;vertical-align:middle"></span> #f5f5f7
    </div>
    <div class="row"><span class="k">Typeface(s)</span>[e.g. Inter (body) · Poppins (headings)]</div>
    <div class="row"><span class="k">Distinct font sizes</span>[n]</div>
    <div class="row"><span class="k">Distinct button styles</span>[n] <span class="effort">· fewer is more consistent</span></div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">3</span> Rendered screenshots</h2>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:10px">
      <figure style="margin:0;flex:1 1 380px">
        <figcaption class="verdict-common" style="margin-bottom:6px">Desktop (1440px)</figcaption>
        <img src="design-desktop.png" alt="Full-page desktop render" style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:2px">
      </figure>
      <figure style="margin:0;flex:0 1 220px">
        <figcaption class="verdict-common" style="margin-bottom:6px">Mobile (390px)</figcaption>
        <img src="design-mobile.png" alt="Full-page mobile render" style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:2px">
      </figure>
    </div>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">4</span> Findings</h2>
    <!-- one .card per finding (see the finding card pattern above) -->
  </section>

  <section class="block">
    <h2 class="section"><span class="no">5</span> What's working</h2>
    <ul class="clean"><li>[genuine strength]</li></ul>
  </section>

  <section class="block">
    <h2 class="section"><span class="no">6</span> Summary</h2>
    <div class="row"><span class="k">Findings</span>[n] ([x] quick wins, [y] big bets, …)</div>
    <div class="row"><span class="k">Design tokens (measured)</span>[typeface(s)] · [N] font sizes · [N] colours · [N] button styles</div>
    <div class="row"><span class="k">Visual read</span>expert judgement — benchmarks §4 UI/UX [or "not assessed — no render/screenshot"]</div>
    <div class="row"><span class="k">Top priority</span>[DSN-ID — one line]</div>
  </section>
  <p class="printhint">🖨 Print / Save as PDF — press <kbd>Ctrl</kbd>+<kbd>P</kbd> (<kbd>⌘</kbd>+<kbd>P</kbd> on Mac)</p>
</div>

<footer class="doc">
  <div class="fwrap">
    <a class="brandlink" href="https://ananas-agency.com/?utm_source=ananas-website-skills&amp;utm_medium=deliverable&amp;utm_campaign=website-audit-suite&amp;utm_content=design-visual" target="_blank" rel="noopener">
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

================================================================================

# 7. Action Report

**Skill ID:** `action-report`

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

> **Precondition — check before you assemble anything.** The report's section 2 cites `goals.md` as its
> source, so that file must exist. If **Goals & Discovery never ran**, stop and run it now (it's a short
> interview; the scans are already done, so it costs only the owner's answers) — then assemble. Do not
> paper over it by writing section 2 from the scans: an owner brief you inferred yourself is fabrication,
> and every grade in the report is supposed to be judged against a goal *the owner stated*. Only if the
> owner is genuinely unavailable do you proceed, with section 2 marked **NOT CAPTURED** and a line in the
> executive summary saying the audit is ungrounded.

## What it produces

1. **Overall scorecard**: the completed dimension grades side by side, plus an **overall grade** (average
   of the completed dimension scores, mapped to the same A–F bands). See
   [report-format.md](report-format.md).
1b. **"2026 standard vs your site" scorecard**: a compact table of the key benchmarks from
   [benchmarks-2026.md](benchmarks-2026.md) (Core Web Vitals, mobile/tap targets, WCAG 2.2 AA, title
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
plus the Site Snapshot. Note which analyses are missing. **Check the Goals & Discovery brief is actually
there** (see the precondition under "Inputs") — if the owner was never interviewed, interview them now,
before you build the scorecard.

### Step 2: Build the overall scorecard
Show the completed dimension grades and compute the **overall grade** (average of completed dimension
scores → A–F). State it's an expert judgement, not a lab score. If dimensions are missing, average only
what exists and say so.

### Step 3: Place every finding on the matrix
Assign each finding to its quadrant from its Impact × Effort (rules in
[report-format.md](report-format.md)). Build the 2×2. Sanity-check the ratings for consistency across
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
Full spec: [report-format.md](report-format.md).

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
above ~1/150 words is the main offender ([report-format.md](report-format.md), "Write like a human:
no AI patterns"). Details: [report-format.md](report-format.md), "Final consistency pass" and
"Deliverables bundle".

### Step 9: Bundle the ZIP
Pack **`[site]-website-audit.zip`** (built with code execution) in the layout from
[report-format.md](report-format.md), "Deliverables bundle": the `.md`/`.html` deliverables **flat at
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
5b. **No report without an owner brief.** If Goals & Discovery never ran, run it before assembling; never
   write section 2 from your own inference. The grades mean nothing against a goal nobody stated.
6. **One CTA, once.** The agency CTA block appears in exactly one place (the Action Report / consolidated
   report closing), nowhere else in the pack.
7. **The regenerated pack is canonical.** Mid-session files are working copies; the ZIP's regenerated set
   is the one that ships, with the full walk, tooltips, and reconciled TBDs.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)

---

## Skill reference materials: action-report

### Reference: rules-action-report.md

# Action Report Rules — Detailed Reference

This skill synthesises the whole audit. The Finding format, Impact/Effort scales, priority quadrants,
grade bands, ID scheme, the consolidated-report spec, cross-linking rules, the final consistency pass, and
the bundle all live in [report-format.md](report-format.md). This reference adds the synthesis method,
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
SEO, UX, CTA, quadrant labels), every occurrence. See [report-format.md](report-format.md).

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
[report-format.md](report-format.md); the essentials:

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
- **Findings tables use the fixed `<colgroup>` from [report-format.md](report-format.md)** ("the findings
  table uses this exact colgroup"): six percentage widths, `8 / 19 / 28 / 28 / 6 / 11`, summing to 100,
  with `min-width:860px`. Do not invent column widths and never mix `px` with `%` in one colgroup — a
  mixed set over-constrains the table, gets ignored, and squeezes `ID` and `Priority` to min-content.
- Uses the same `<style>` block and frame; use `utm_content=website-audit-report` in its brand links.
- End with the single agency `.ctablock` (if not already on the Action Report page you link to) and the
  Print hint. The final pass makes this the **entry** file of the walk (sorts first; no Previous; Next →
  `site-snapshot.html`).

---

## Final consistency pass & bundle

Do these last, per [report-format.md](report-format.md):
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)
