---
name: goals-discovery
description: >
  The owner's-voice intake for the Ananas-Agency Website Audit Suite. A short structured interview that
  captures how the owner feels about their website today and what they actually want it to achieve — are
  they happy with it, what frustrates them most, the single most important goal, what "success" would
  look like (a number if they have one), who the site is really for in their words, sites they admire,
  and their appetite and constraints for change — then cross-examines those answers against what the fetched
  page and the parallel measured scans actually show, surfacing the gaps and closing with prioritised advice.
  Produces a reusable Goals & Discovery diagnostic (not a transcript) that runs alongside the Site Snapshot
  and gives every later analysis the human context the page can't reveal.
  Runs perfectly WHILE the site is being read/measured — it's paced by the owner answering, so launch
  any background scans first, then interview while they render. Use this skill when the user wants to:
  talk about their goals for the site, say whether they're happy with it, be interviewed about the
  website, capture what they're trying to achieve, or start the "discovery" step of an audit. Trigger:
  "am I happy with my website", "what do I want from my site", "website goals", "owner interview",
  "discovery", "what are we trying to achieve", "are you happy with your site", "what's the site for".
---

# Goals & Discovery (Ananas-Agency — Website Audit intake)

## Goal

Capture the **owner's voice**, then **cross-examine it against the site**, and turn the gap into insight. A
transcript of the owner's answers is low value; the value is putting *what they believe* next to *what the
page and the measured scans actually show*, and surfacing where the two disagree.

So this skill produces a **diagnostic**, not a form:
1. a short **owner brief** (satisfaction, the one goal, success, frustrations, audience, appetite),
   compressed, not the bulk;
2. a **"Stated vs. observed" reality-check:** each belief the owner holds, set against what the fetch +
   the parallel scans reveal, with **the gap** called out (this is the centre of gravity);
3. the **tensions:** where the goal, the constraints and the data pull against each other;
4. a short, **prioritised "How to reach your goal":** opinionated direction, each item pointing to the
   analysis that will detail it.

This works *because* the interview runs while the scans render (below): by the time the owner finishes
answering, the measured data is already in, so you can immediately hold their answers against it. Where the
[Site Snapshot](../../0%20Site%20Snapshot/site-snapshot/SKILL.md) records what the *page* says and the owner
brief records what the *person* says, the reality-check is where you **add judgment neither could give alone**.
Written for **business owners and marketers**. Keep it a warm conversation, not a form; plain language, no jargon.

## Why a Goals & Discovery brief

The five analyses grade the site against the 2026 standard. But "good" only means something relative to a
goal. Two facts change how every finding should be read:

- **What the owner is trying to achieve:** more leads, more sales, fewer support calls, looking credible
  to investors. The same page is a success or a failure depending on which.
- **What they can and will change:** a beautiful redesign recommendation is useless if the brand is locked
  or the budget is an afternoon. Appetite and constraints keep the advice realistic.

Captured once, this brief travels with the [Site Snapshot](../../0%20Site%20Snapshot/site-snapshot/SKILL.md)
into every skill. It is **discovery + diagnosis + direction**. It produces **no graded findings** (the five
analyses do that, with IIF findings and letter grades), but it *does* hold the owner's answers against the
observed reality and close with **prioritised advice on how to reach their stated goals**, giving the
analyses and the [Action Report](../../7%20Action%20Report/action-report/SKILL.md) their bearings. The
reality-check and advice are directional, not the final plan; the analyses verify the specifics and the
Action Report ranks them.

## Runs *while* the site is being analysed

This interview is paced by the **owner answering**, so it costs almost no machine time, which makes it the
ideal thing to run **concurrently** with the parts of the audit that do:

- **Extended layer (tools can run, e.g. Claude Code):** as soon as you have the URL and a Site Snapshot,
  **launch the measured scans in the background** (`perf-a11y-scan.py`, `mobile-audit.py`, `design-scan.py`,
  `seo-sweep.py`, `tracking-scan.py`, `interaction-scan.py`; run them in the background so control returns
  to you), then **run this interview while they render**. When the interview wraps, the scan outputs are
  waiting. This hides the slowest part of the whole audit behind the conversation.
- **Basic layer (no tools, e.g. the Claude app):** there's no background thread, so simply **interleave**:
  read a page, ask a question, read the next while the owner types. It still feels concurrent and nothing
  is wasted.

Either way: **don't make the owner wait for a scan bar.** Talk to them while the machine works.

## What the brief captures

**Core, always capture (the fast interview):**
1. **Satisfaction today:** how happy they are with the site overall, and (optional) a quick 1–5
   self-rating across a few areas: look & feel, message clarity, getting leads/sales, ease of updating.
   *This is the owner's own view, clearly labelled, not the audit's grade.*
2. **The one goal:** the single most important thing they want the site to achieve. Reconcile this with
   the Snapshot's **primary conversion goal** (they should agree; if not, resolve it here).
3. **What success looks like:** how they'd know it's working, with a **number if they have one** (e.g.
   "20 qualified leads a month", "a 2% checkout rate", "10 booked calls a week"). Mark **TBD** if none.
4. **Biggest frustrations:** the one or two things that bother them most, in their own words.
5. **Audience, in their words:** who they think the site is really for and what those people come to do.
6. **References they admire:** sites they look at and want to emulate, and *what* they like about each.
7. **Appetite & constraints:** how much time/budget they have for change, and anything off-limits (brand
   locked, can't change platform, don't touch page X, a redesign already underway).
8. **History & wishlist** *(light)*: anything they've changed or tried recently, and the one new thing
   they wish the site could do.

**Deeper, capture when there's time, or for a fuller brief** (these sharpen the advice at the end):
9. **Current results baseline:** roughly how many enquiries/sales the site brings now, and how good the
   quality is. Gives the target a starting point ("from ~3 to ~10 a month").
10. **Traffic sources:** where visitors come from today (search, ads, referrals, social, word of mouth),
    even roughly. Tells you which lever moves the goal.
11. **Why clients really choose them:** the true differentiator, in the owner's words (not the tagline).
12. **Biggest objection:** the doubt or question prospects raise most before they buy/commit.
13. **Money pages:** the pages/products/services that matter most commercially (where to focus effort).
14. **Marketing in flight:** what's running now (ads, content/SEO, email, events, outbound) that the site
    should support.
15. **Brand & assets:** do they have brand guidelines / a logo / photography, or is a rebrand underway?
16. **Budget & timeline:** a rough band and any deadline (a launch, a campaign, a trade show).
17. **Who decides:** who signs off on changes (owner alone, a marketing lead, a committee).
18. **The competitor to beat:** one rival or example site they want to outclass, and why.
19. **Anything we missed** *(open catch-all)*: "What haven't I asked that matters for this site?" Always
    end on this; it's where owners volunteer the thing no fixed question would surface.

**Ask each in the right form:**
- **Single-select pickable** (force one answer): satisfaction · the **one** goal · appetite. The point is
  a priority; don't let these be multi.
- **Multi-select pickable** (pick all that apply): traffic sources · frustrations · audiences ·
  marketing-in-flight · brand assets. More than one is usually true.
- **Open (their own words)**: what success/"wow" looks like · why clients really choose them · the biggest
  objection · references they admire · the wishlist · the competitor to beat · the catch-all above. These
  can't be pre-listed, and they carry the richest material; quote them verbatim.
- Every pickable question still offers an **"Other"** so a pick never traps them.

Scale to the session: the **Core** eight are enough for a quick brief; add as many **Deeper** questions as
the owner has patience for. The more of the Deeper set you capture, the more specific the closing advice
can be.

## What it produces (diagnosis, not a transcript)

The output leads with the **judgment**, not the answers. In order:

**1. Owner brief (compressed).** The answers in a few tight rows: satisfaction, the one goal, success (+ a
number or **TBD**), top frustration, audience, appetite & constraints. Keep it short; it's context, not the
main event.

**2. "Stated vs. observed" reality-check, the centre of the deliverable.** For each belief the owner holds,
set it beside what the **fetched page and the parallel scans** actually show, and name **the gap**. Examples:
- Owner's goal is *"look credible"* → the scan measured **LCP 10.8s / 6 MB / no security headers** → *the
  #1 credibility killer is technical, not visual: a 10-second load reads as amateur before design is seen.*
- Owner says *"the message isn't sharp"* → the H1 is a slogan, services are generic, the portfolio is
  anonymised → *confirmed, and it's a copy fix: name what you do + who for, and name the clients.*
- Owner's satisfaction is *"okay"* → the measured foundation grades poorly → *the self-rating is generous.*

Each row is **you said → what we see → the gap**. This is what the owner can't get from a form, and it's the
reason the interview runs while the scans render; the data is ready to hold their answers against.

**3. Tensions.** Where the goal, the constraints and the data pull against each other, e.g. *"you want 'wow'
but have only a few days and want to keep the design"* → then resolve it (often the constraint and goal turn
out compatible, which is itself worth saying).

**4. "How to reach your goal": prioritised advice.** 3–6 opinionated, plain recommendations, **ordered by
leverage toward the stated goal**, each tied to an answer + the reality-check and pointing to the analysis
that details it. Sharp and short, not a hedge.

Rules that keep it honest:
- **Cross-examine, don't just record:** a row that only restates an answer adds nothing; every row must
  carry an observation or a gap.
- **Ground the "observed" side in fact:** the fetched page, or the measured scans (cite the real number).
  Don't invent metrics; the real-world numbers only analytics can show stay owner-reported.
- **No grades or IIF findings:** that's the five analyses and the Action Report. This is the orienting
  diagnosis, not the graded plan.

## Conversation flow

Keep it human and warm: **2–3 questions at a time**, in a few short passes. Always cover the **Core** eight;
then go as deep into the **Deeper** set as the owner has patience for (a quick brief is ~8 questions; a full
one is ~14–18). Come curious, not clipboard-in-hand, and let the depth follow their energy, not a checklist.

> **How to run this session: read before you start.**
> - **Kick off the machine work first (if you can), then talk.** In the Extended layer, launch the
>   background scans before you ask question one, so they render while you interview (see "Runs while the
>   site is being analysed"). Never leave the owner watching a progress bar.
> - **Mix pickable and open questions, don't make it all multiple-choice.** Use a short **pickable list**
>   for quick categorical answers (satisfaction: very happy / okay / frustrated; the goal: more leads /
>   sales / bookings / sign-ups / credibility / fewer support calls; appetite: an afternoon / a few days / a
>   project), always with an **"Other"** escape so they can type their own. But ask a genuine **open
>   question** wherever the answer needs their own words and can't be pre-listed: *what "success" actually
>   looks like, why clients really choose them, the sites they admire and why, the one thing they wish the
>   site did, and "what am I missing?"*. The open answers are where the richest material comes from; quote
>   them verbatim.
> - **Let pickable questions take more than one answer where more than one is true.** Traffic sources,
>   frustrations, audiences, and marketing-in-flight are rarely a single item, so offer these as
>   **multi-select** (pick all that apply) rather than forcing one choice. Satisfaction, the *one* goal, and
>   appetite stay single-select (the whole point is to force a priority).
> - **Nail the one goal and a number.** Push gently for the single most important goal and, if it exists,
>   a target number; it's what makes "is the site working?" answerable. If there's genuinely no number,
>   record **TBD**, don't invent one.
> - **Reconcile with the Snapshot.** If the owner's stated goal differs from the primary conversion in the
>   Site Snapshot, surface the mismatch and settle it; the analyses are scored against one goal.
> - **Their words are evidence.** Quote the owner directly in the brief (e.g. *"it looks dated and I'm
>   embarrassed to send the link"*). Don't paraphrase their frustration into blandness.
> - **Cross-examine, don't transcribe.** A brief that only echoes the answers is low value. Once you've
>   captured enough, hold each belief against the page + the finished scans and write the **"Stated vs.
>   observed"** reality-check (you said → what we see → the gap), then the **tensions**, then prioritised
>   advice. No grades or IIF findings (that's the analyses), but real judgment, grounded in what you saw.

### Required inputs — capture before delivering
Check each off (or mark **TBD**) before you deliver:
- [ ] **Core:** Satisfaction today (overall; optional per-area 1–5 self-rating)
- [ ] **Core:** The **one goal** (reconciled with the Snapshot's primary conversion)
- [ ] **Core:** What success looks like (+ a target number if they have one, else **TBD**)
- [ ] **Core:** Biggest frustration(s), in their words
- [ ] **Core:** Audience in their words
- [ ] **Core:** References they admire (optional) and what they like
- [ ] **Core:** Appetite & constraints (time/budget; anything off-limits)
- [ ] **Core:** History & wishlist (optional)
- [ ] **Core:** "Anything we missed?", the open catch-all (always ask last)
- [ ] **Deeper (as captured):** results baseline · traffic sources · true differentiator · biggest objection ·
      money pages · marketing in flight · brand & assets · budget & timeline · who decides · competitor to beat
- [ ] **Reality-check:** a **"Stated vs. observed"** row per belief (you said → what we see → the gap)
- [ ] **Tensions:** goal vs. constraints vs. data conflicts, each resolved
- [ ] **Advice:** the prioritised **"How to reach your goal"** recommendations, each tied to a gap and an analysis

### Step 1: Set up the parallel work, then open the conversation
If you have the URL and a Snapshot and can run tools, **start the background scans now**. Then open warmly:
*"Before I dig into the site, how do you feel about it today, and what do you most want it to do for you?"*

### Step 2: Satisfaction & the one goal
Ask how happy they are (offer very happy / okay / frustrated) and, optionally, a quick 1–5 on look & feel,
message clarity, getting leads/sales, and ease of updating. Then pin the **single most important goal**
(pickable list) and reconcile it with the Snapshot's primary conversion.

### Step 3: Success, frustrations & audience
Ask what success looks like (chase a number), the one or two things that frustrate them most, and who they
think the site is really for. Quote them.

### Step 4: References, appetite & constraints
Ask which sites they admire and why, how much appetite/budget they have for change, and what's off-limits.
Optionally: anything they've changed recently, and the one thing they wish the site could do.

### Step 5: Deeper context (as far as they'll go)
If the owner has patience, go into the **Deeper** set, a couple of questions at a time: current results
baseline and traffic sources, why clients really choose them and the biggest objection, the money pages and
marketing in flight, brand/assets, budget & timeline, who decides, and the competitor to beat. Stop whenever
their energy dips; every extra answer just makes the closing advice sharper. Mark anything skipped **TBD**.

### Step 6: Cross-examine — build the "Stated vs. observed" reality-check
This is the step that makes the deliverable worth reading. By now the parallel scans have finished, so hold
each of the owner's beliefs against what you can actually see:
- Read the fetched page yourself (hero, copy, CTA, proof, structure) and pull the measured numbers from the
  scans (perf/CWV, security headers, axe/keyboard, mobile, design tokens, tracking/consent, links).
- For each belief (the goal, the satisfaction rating, the frustration, the audience) write one row:
  **you said → what we see → the gap**. Prefer rows where the two *disagree* (that's the insight); confirm
  the ones where they agree, briefly.
- Then list the **tensions**: where the goal, the constraints and the data conflict, and resolve each
  (often the constraint and the goal are compatible, which is worth stating).
Ground every "observed" claim in the page or a real measured number; never invent one.

### Step 7: Write the prioritised "How to reach your goal" advice
Turn the reality-check into 3–6 **opinionated, ordered** recommendations, highest leverage toward the
stated goal first. Anchor each to a belief + its gap, make it concrete and plain, cite the real number where
one exists, and point it to the analysis that will detail it. No grades, no IIF findings; the analyses and
Action Report produce the graded, prioritised plan.

### Step 8: Confirm & deliver
Summarise the reality-check and the top advice back in a few lines and get a quick confirm. Mark genuine
unknowns **TBD** (the Action Report's reconciliation pass backfills any answered later). Then deliver the files.

### Step 9: Hand off
Tell the owner the brief is ready and travels with the Site Snapshot; they paste both whenever a later
skill asks about the site. Point them to the analyses (**Messaging**, **Conversion**, **SEO**,
**UX & Technical**, **Design & Visual**), any of which can run next, and note that by now the background
scans (if you launched them) are likely done.

## Output: deliver the brief as files

Generate TWO files (`goals.md` and a styled, self-contained `goals.html`) and share them. The `.html` uses
the **shared design system** and follows the shared navigation rules: cross-links to the other deliverables,
hover hints on short terms, and the Print hint at the end (no `pagenav` mid-session). Format and the full
shared page frame. See [references/rules-goals-discovery.md](references/rules-goals-discovery.md),
section "Output file format".

Save both files and share them with the user for download.

## Add to the Website Audit Report

This suite runs as one continuous session. **Deliver only your own two files now** (`.md` + `.html`). Keep
the **Website Audit Report** as an **internal running document**. Do **not** create, show, or hand over a
report file mid-session; the [Action Report](../../7%20Action%20Report/action-report/SKILL.md) assembles and
delivers it at the very end. Record the **Goals & Discovery** section (the compressed owner brief, the
**"Stated vs. observed"** reality-check, the tensions, and the prioritised **"How to reach your goal"**
advice) into that internal record, in its fixed slot right after Site Snapshot. Full format and section
order: [report-format.md](../../report-format.md).

## Critical rules

1. **Run it in parallel.** It's owner-paced: launch the background scans first (Extended) or interleave
   (Basic), so the interview and the machine work overlap. Never make the owner wait on a scan.
2. **Cross-examine, don't transcribe.** The value is the gap between what the owner *believes* and what the
   page + scans *show*. Lead with the **"Stated vs. observed"** reality-check and tensions, then prioritised
   advice. No letter grades and no IIF findings (that's the five analyses), but every row must carry an
   observation or a gap, grounded in the page or a real measured number, never invented.
3. **One goal, reconciled.** Pin the single most important goal and make it agree with the Snapshot's
   primary conversion; every later finding is judged against it.
4. **Chase a number.** Push gently for a target metric; if there genuinely isn't one, record **TBD**, never
   invent a figure.
5. **Quote the owner.** Their own words are the evidence in this brief; don't sand them down.
6. **Don't invent.** Anything unknown stays **TBD**; the reconciliation pass backfills what's answered later.
7. **Plain language, warm tone.** Business owners are the audience: a conversation, not a questionnaire.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
