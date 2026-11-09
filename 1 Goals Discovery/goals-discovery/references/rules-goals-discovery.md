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
  python scripts/perf-a11y-scan.py   https://example.com/ --out "audit-<slug>" &
  python scripts/mobile-audit.py     https://example.com/ --out "audit-<slug>" &
  python scripts/design-scan.py      https://example.com/ --out "audit-<slug>" &
  python scripts/seo-sweep.py        https://example.com/ --out "audit-<slug>" &
  python scripts/tracking-scan.py    https://example.com/ --out "audit-<slug>" &
  python scripts/interaction-scan.py https://example.com/ --out "audit-<slug>" &
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

## Output
Write the results to the run folder as described in [audit-data-format.md](../../../audit-data-format.md),
section "goals.json", then build the page.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
