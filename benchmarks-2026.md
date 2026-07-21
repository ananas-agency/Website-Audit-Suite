# What a website should be in 2026 — benchmarks & standards

This is the **standard the Website Audit Suite grades against**. Every skill's rubric "Pass" definition
and every finding's "the standard is X, you're at Y" framing traces back to the thresholds below. It turns
the audit from opinion into a measurable gap against current, sourced best practice — so a company gets a
concrete update plan, not a matter of taste.

> **Living document.** Web standards move. These figures are current for **early 2026**; the ones most
> likely to shift are Core Web Vitals thresholds, the accessibility baseline, and answer-engine (AEO/GEO)
> practice. Review this file at least once a year (the year is in the filename on purpose). Where a number
> is a genuine measured threshold from a standards body it's marked with its source; where it's an
> accepted convention it's marked *(convention)*.

How to use it: each dimension below lists the **2026 expectation** and the **threshold**. In a finding,
state both — e.g. *"Largest Contentful Paint should be ≤ 2.5s (Google Core Web Vitals); the bundled
`perf-a11y-scan.py` measured 9.5s here."* (In the Basic layer, with no headless browser, mark it "not
measured" instead.) The **Action Report** renders a compact **"2026 standard vs your site"** scorecard from
these.

---

## 1. Performance & Core Web Vitals

The single biggest 2026 baseline shift: page experience is measured, mobile-first, on **field data** (real
users, 75th percentile), and it's a Google ranking input.

| Metric | 2026 target ("good") | Needs work | Poor | Notes |
|--------|----------------------|-----------|------|-------|
| **LCP** — Largest Contentful Paint (load) | **≤ 2.5s** | 2.5–4.0s | > 4.0s | Main content visible. |
| **INP** — Interaction to Next Paint (responsiveness) | **≤ 200ms** | 200–500ms | > 500ms | **Replaced FID in March 2024** — this is the current CWV. |
| **CLS** — Cumulative Layout Shift (stability) | **≤ 0.1** | 0.1–0.25 | > 0.25 | No jumping layout. |
| **TTFB** — Time to First Byte | **≤ 0.8s** *(convention)* | 0.8–1.8s | > 1.8s | Server/response speed. |

- Serve images as **WebP/AVIF**, sized to their display box, **lazy-loaded** below the fold; a hero image
  should rarely exceed a few hundred KB. *(convention)*
- **HTTP/2 or HTTP/3**, **Brotli/gzip** compression, sensible caching. *(convention)*
- Every 100ms of extra load measurably costs conversions — performance is a revenue issue, not just SEO.
- **Source:** Google `web.dev` / Chrome Core Web Vitals. **Measured** here by the bundled `perf-a11y-scan.py`
  (lab CWV + a Total-Blocking-Time INP proxy). Real-world *field* percentiles need many real users and are
  out of scope; in the Basic layer (no browser) flag these "not measured".

## 2. Mobile-friendliness

Most traffic is mobile, and Google now crawls and indexes **mobile-first** (smartphone Googlebot is the
default; the desktop-crawl transition completed in 2024). The mobile experience *is* the experience.

- **Responsive layout** with `<meta name="viewport" content="width=device-width, initial-scale=1">`;
  the page must **fit the screen at 320–430px with no horizontal scroll**.
- **Tap targets ≥ 44×44 CSS px** (Apple HIG) / **48×48** (Google Material). The legal floor is **WCAG 2.2
  SC 2.5.8 Target Size (Minimum) = 24×24**, but **44** is the design standard. Space adjacent targets.
- **Body text ≥ 16px** ideal, **never below 12px** *(convention)*.
- No element or image wider than the viewport.
- **Source:** Google Search mobile-first indexing; Apple HIG; Google Material; WCAG 2.2. Measure by
  **rendering** the page at phone widths (the suite's `mobile-audit.py` does this).

## 3. Accessibility

2026 is the year accessibility became **legally required**, not just good practice, for a large share of
businesses.

- **WCAG 2.2 Level AA is the baseline.** In the EU, the **European Accessibility Act (EAA)** applies from
  **28 June 2025** — many products and services (notably e-commerce, banking, transport, and their
  websites/apps) must meet AA (harmonised via EN 301 549). Similar pressure exists elsewhere (ADA/Section
  508 in the US).
- **Text contrast ≥ 4.5:1** (normal text), **≥ 3:1** (large text and UI components).
- **Alt text** on every informative image; empty `alt=""` only for decorative ones.
- **Labels** on all form fields; fully **keyboard-operable** with a **visible focus** indicator.
- **Semantic structure:** exactly one `<h1>`, logical heading order, `<html lang>` set.
- **Source:** W3C WCAG 2.2 (AA); EN 301 549; EAA. **Measured** here by the bundled `perf-a11y-scan.py`
  (axe-core WCAG scan + a keyboard focus-order pass); contrast/focus/keyboard come from that scan, and full
  screen-reader testing stays manual (out of scope).

## 4. UI/UX design & usability

The interface should be usable, credible, and low-effort. The recognised evaluation frameworks are
**Nielsen's 10 Usability Heuristics** and **ISO 9241** (human-centred design); the practical 2026 bars:

- **Navigation & information architecture:** clear, consistently-placed, plainly-labelled navigation; key
  pages reachable in **~1–3 clicks**; breadcrumbs on deep pages; site search once the catalogue is large;
  no dead ends or orphan pages.
- **Visual hierarchy:** **one clear focal point per screen** that leads the eye to the primary action;
  size, colour, and spacing used to rank importance (the visual analogue of the 5-second test).
- **Readability:** body text **≥ 16px**, line length **45–75 characters** (~66 ideal), line height **~1.5**,
  and text contrast **≥ 4.5:1** (ties to §3 Accessibility).
- **Consistency (Jakob's Law):** the site behaves like the sites users already know; buttons, patterns, and
  wording are internally consistent across pages.
- **Feedback & response time (Nielsen's limits):** every action gives visible feedback — **< 0.1s** feels
  instant, **< 1s** keeps flow, show a loading state beyond ~1s, and **~10s** is the limit of user
  attention.
- **Error prevention & recovery:** prevent errors where possible; clear, human error messages; easy undo;
  favour **recognition over recall**.
- **Aesthetic & minimalist design:** whitespace and restraint over clutter — and via the *aesthetic-usability
  effect*, a clean, current design is also **trusted** more (Stanford Web Credibility).
- **Interaction targets:** clickable/tappable elements look interactive and are large enough (**≥ 44px**,
  see §2) and fully **keyboard-operable** (see §3).
- **The UX "laws"** (Fitts's, Hick's, Miller's, Jakob's) are useful design checks, not hard thresholds.
- **Source:** Nielsen Norman Group (10 Usability Heuristics; response-time limits); ISO 9241-210 / 9241-11;
  Laws of UX; Stanford Web Credibility. *(ISO standard + accepted convention)*

## 5. SEO & content

- **Title tag:** unique per page, **~50–60 characters**, primary keyword front-loaded. *(convention,
  aligned to Google SERP truncation)*
- **Meta description:** **~140–160 characters**, compelling, per page (not a ranking factor, but drives
  click-through).
- **Exactly one `<h1>`**, logical H2/H3 hierarchy.
- **HTTPS**, an **XML sitemap**, a **robots.txt**, and **canonical tags** on every page.
- **Structured data (schema.org JSON-LD):** Organization/LocalBusiness, plus Product, FAQ, Article,
  BreadcrumbList as relevant — increasingly what makes a page eligible for rich results **and** citable by
  AI answer engines.
- **Core Web Vitals are a ranking signal** (page experience) — see §1.
- **People-first content** that demonstrates **E-E-A-T** (Experience, Expertise, Authoritativeness, Trust);
  Google's Helpful Content system rewards genuine usefulness over keyword-stuffing.
- **Clean, descriptive URLs**; descriptive internal-link anchors (no "click here").
- **New for 2025–26 — AEO / GEO** (Answer-Engine / Generative-Engine Optimization): being **cited by AI
  answer engines** (Google AI Overviews, ChatGPT, Perplexity). Levers: strong structured data, clear
  factual and well-structured content, a solid entity/brand footprint. (An `llms.txt` convention is
  emerging but not yet a standard.)
- **Source:** Google Search Essentials / Search Central; schema.org.

## 6. Messaging & clarity

- A first-time visitor understands **what you offer, for whom, and the next action within ~5 seconds**,
  from the hero alone — StoryBrand calls this the **"grunt test."** *(convention — the "5-second" / "grunt"
  test)*
- **One primary call to action**, benefit-led and specific.
- **A concrete, differentiated value proposition:** it names the customer's problem, your solution, and the
  outcome, and passes the "a competitor couldn't paste their name on this" test. Recognised frameworks: the
  **Value Proposition Canvas** (Strategyzer / Osterwalder), **positioning** (April Dunford, *Obviously
  Awesome*; Geoffrey Moore's positioning template), and the **conversion-sequence / value-proposition**
  heuristics (MarketingExperiments / MECLABS, CXL).
- **Written the way people actually read online:** users **scan in an F-pattern** and read only ~20–28% of
  the words on a page, so front-load the point, use benefit-led headings, short paragraphs, and bullets
  (Nielsen Norman Group).
- **Plain, customer-language copy** — no unexplained insider jargon; aim for a general-audience reading
  level. Standards: **plainlanguage.gov**, **ISO 24495-1:2023 (Plain language)**, and the widely-copied
  **GOV.UK content design / style guide**.
- **Social proof / trust** near the claims (named testimonials, client logos, numbers).
- **Source:** NN/g (how users read; F-pattern); StoryBrand; Strategyzer Value Proposition Canvas; April
  Dunford; MarketingExperiments / CXL; plainlanguage.gov / ISO 24495-1; GOV.UK content design. *(conventions
  + one ISO standard)*

## 7. Conversion (CRO)

- **Minimise form friction:** ask only for what's needed; each extra field costs completions.
- **Trust at the point of action:** logos, testimonials, guarantees, security/payment badges beside the
  CTA/form.
- **A mobile-first conversion path**, and **fast load** (see §1) — both directly move conversion rate.
- **Clear pricing, or a clear path to it** (B2B: at least an engagement/"how we work" model).
- **More than one path:** a low-commitment option (lead magnet, newsletter) for visitors who aren't ready
  to buy/book.
- **Source:** established CRO practice (Baymard Institute, Nielsen Norman Group) *(convention)*.

## 8. Security, privacy & trust

- **HTTPS everywhere** with a valid certificate, **HSTS**, **TLS 1.2+/1.3**, and **no mixed content**
  (no `http://` assets on an `https://` page). HTTPS is a baseline ranking and trust signal.
- **Consent & privacy:** a compliant **cookie-consent** mechanism (GDPR/ePrivacy in the EU), analytics
  **consent mode**, and reachable **privacy & cookie policies**.
- **Security headers** (CSP, X-Content-Type-Options, Referrer-Policy, etc.) — a plus, not yet universal.
- **Source:** GDPR / ePrivacy; Google HTTPS-as-a-ranking-signal; OWASP secure-headers.

---

## The 2026 baseline in one line per dimension

| Dimension | The 2026 bar |
|-----------|--------------|
| **Performance** | LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1, on mobile field data |
| **Mobile** | Responsive, fits 320–430px, tap targets ≥ 44px, text ≥ 16px |
| **Accessibility** | WCAG 2.2 **AA** (legally required for many under the EAA since 28 Jun 2025) |
| **UI/UX & usability** | Passes Nielsen's heuristics: clear IA (~1–3 clicks), one focal point, ≥16px / 45–75-char / 1.5 text, consistency, visible feedback (<1s), minimalist & credible |
| **SEO** | Unique 50–60-char titles, one H1, HTTPS + sitemap + canonical + schema, CWV, E-E-A-T, AEO-ready |
| **Messaging & clarity** | Offer + audience + next action clear in 5s (grunt test); differentiated value prop (VP Canvas); F-pattern, plain-language copy; one CTA; real proof |
| **Conversion** | Low-friction forms, trust at the ask, fast + mobile path, clear pricing, a second path |
| **Security/Privacy** | HTTPS + HSTS + TLS 1.3, no mixed content, compliant consent + policies |

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](LICENSE)
