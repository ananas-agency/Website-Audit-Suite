# Messaging & Clarity Rules — Detailed Reference

The core unit is a **Finding (Issue · Impact · Fix)**; the Impact/Effort scales, priority quadrants,
grade bands, and cross-linking rules live in [report-format.md](../../../report-format.md). This reference
adds the messaging-specific tests, the scoring rubric, and worked finding examples.

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

## Output
Write the results to the run folder as described in [audit-data-format.md](../../../audit-data-format.md),
section "Dimension files", then build the page.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
