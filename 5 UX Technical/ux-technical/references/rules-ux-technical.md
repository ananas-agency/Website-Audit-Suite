# UX & Technical Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
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
[report-format.md](../../../report-format.md). **No `pagenav`** mid-session; end with the Print hint.

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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
