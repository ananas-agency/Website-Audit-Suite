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
- **Cross-link every reference to another deliverable** (see [report-format.md](../../../report-format.md)
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
