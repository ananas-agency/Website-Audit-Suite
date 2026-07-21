# Conversion (CRO) Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
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
[report-format.md](../../../report-format.md). **No `pagenav`** mid-session; end with the Print hint.

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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
