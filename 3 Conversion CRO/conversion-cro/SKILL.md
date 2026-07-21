---
name: conversion-cro
description: >
  Analyses a website's conversion effectiveness (CRO) in the Ananas-Agency Website Audit Suite. Fetches
  the homepage and key pages and judges whether the site removes friction and drives visitors toward its
  primary conversion — the conversion path, calls to action (CTAs), forms, trust signals at the ask,
  distractions and leaks, pricing clarity, urgency, and the mobile path. Produces graded findings in
  Issue · Impact · Fix format on an Impact × Effort priority scale, plus a 0–100 conversion grade. Use
  this skill when the user wants to: improve conversions, understand why visitors don't buy or enquire,
  fix a form or a call to action, tighten a landing page, or reduce checkout drop-off.
  Trigger: "improve conversions", "why don't visitors buy", "my form", "call to action", "checkout
  drop-off", "CRO audit", "landing page conversion", "why aren't people enquiring", "fix my CTA".
---

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

Every observation is a Finding. See [report-format.md](../../report-format.md) for the full definition,
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
[benchmarks-2026.md](../../benchmarks-2026.md)**, so cite the benchmark in findings ("the standard is X,
you're at Y"), then apply the weights, and total to a **0–100 score**; map
to a **letter grade** (A–F, bands in [report-format.md](../../report-format.md)). Show the criteria table so
the grade is explainable. State plainly that the grade is an **expert judgement**, not a lab measurement,
and that real conversion behaviour needs the user's own analytics (see the honesty rule below).

### Step 5: Deliver the files

Generate `conversion.md` and a styled, self-contained `conversion.html` and share them. Format, the finding
card component, and the scorecard layout. See the reference, "Output file format". End the HTML with the
Print hint; **no `pagenav`** mid-session.

### Step 6: Add to the Website Audit Report & hand off

Record the **Conversion (CRO)** section (grade + criteria + findings) into the internal running **Website
Audit Report** (do not create/show a report file now; that's the Action Report skill's job at the end).
Format and section order: [report-format.md](../../report-format.md). Tell the user the remaining skills are
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
