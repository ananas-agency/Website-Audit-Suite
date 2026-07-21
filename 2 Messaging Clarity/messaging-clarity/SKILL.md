---
name: messaging-clarity
description: >
  Analyses a website's messaging and clarity in the Ananas-Agency Website Audit Suite. Fetches the
  homepage and key pages and judges whether a visitor instantly understands what the site offers, for
  whom, and why to choose it — the value proposition, headline, subhead, primary call to action,
  differentiation, proof, and customer language. Produces graded findings in Issue · Impact · Fix
  format on an Impact × Effort priority scale, plus a 0–100 clarity grade. Use this skill when the
  user wants to: check if their website message is clear, review their homepage copy / headline /
  value proposition, understand why visitors "don't get it", or improve their site's wording.
  Trigger: "is my message clear", "review my homepage copy", "value proposition on my site", "my
  headline", "why don't visitors understand", "messaging audit", "website clarity", "above the fold".
---

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

Every observation is a Finding. See [report-format.md](../../report-format.md) for the full definition,
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
[benchmarks-2026.md](../../benchmarks-2026.md)**, so cite the benchmark in findings ("the standard is X,
you're at Y"), then apply the weights, and total to a **0–100 score**; map
to a **letter grade** (A–F, bands in [report-format.md](../../report-format.md)). Show the criteria table so
the grade is explainable. State plainly that the grade is an **expert judgement**, not a lab measurement.

### Step 5: Deliver the files

Generate `messaging.md` and a styled, self-contained `messaging.html` and share them. Format, the finding
card component, and the scorecard layout. See the reference, "Output file format". End the HTML with the
Print hint; **no `pagenav`** mid-session.

### Step 6: Add to the Website Audit Report & hand off

Record the **Messaging & Clarity** section (grade + criteria + findings) into the internal running
**Website Audit Report** (do not create/show a report file now; that's the Action Report skill's job at
the end). Format and section order: [report-format.md](../../report-format.md). Tell the user the next skill
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

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
