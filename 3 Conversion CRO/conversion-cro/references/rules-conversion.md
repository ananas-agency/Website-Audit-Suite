# Conversion (CRO) Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
adds the conversion-specific tests, the scoring rubric, and worked finding examples.

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
Run the bundled tool (needs Playwright: the install commands the setup check prints; read-only, no clicks/submits):

```
python scripts/tracking-scan.py <URL> --out "audit-<slug>"
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
python scripts/interaction-scan.py <homepage-URL> --pages <home,contact,top-service> --out "audit-<slug>"
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

## Output
Write the results to the run folder as described in [audit-data-format.md](../../../audit-data-format.md),
section "Dimension files", then build the page.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
