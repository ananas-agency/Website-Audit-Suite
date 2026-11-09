# Site Snapshot Rules — Detailed Reference

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
  provides. Save the image file in the run folder (`audit-<slug>/`) and put its file name in `audit.json`'s
  `logo`; the builder embeds it. If there is none, leave `logo` out. Never invent a logo.

---

## If the page can't be read

Some sites render nothing useful without JavaScript, block fetching, or sit behind a login. If so:
- Say plainly what happened ("I couldn't read the page directly; it looks JavaScript-rendered / blocked").
- Ask the user to paste the homepage (and 1–2 key pages') visible text, or share a screenshot.
- Work from what they provide; mark anything still unknown as **TBD**.

---

## Output
Write the results to the run folder as described in [audit-data-format.md](../../../audit-data-format.md),
section "site-snapshot.json", then build the page.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
