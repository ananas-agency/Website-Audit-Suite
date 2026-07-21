---
name: site-snapshot
description: >
  URL-first intake for the Ananas-Agency Website Audit Suite. Fetches a website, reads it, and
  captures the fundamentals — what the site is, who it's for, its single most important conversion
  goal, its key pages, and its platform — into a reusable Site Snapshot that every analysis skill
  (Messaging & Clarity, Conversion/CRO, SEO & Content, UX & Technical, Action Report) consumes
  instead of re-establishing the basics. Use this skill when the user wants to: audit or analyse
  their website, review their site, "check my website", start a website audit, or give the site
  before a messaging / conversion / SEO / UX review. Trigger: "analyse my website", "audit my
  site", "review my website", "website snapshot", "check my homepage", "look at my site", "start
  the website audit", "here's my URL".
---

# Site Snapshot (Ananas-Agency — Website Audit intake)

## Goal

Fetch the user's website and produce a reusable **Site Snapshot**: the shared foundation for every
other Website Audit skill. Establish it once (what the site is, who it's for, and the one action it
most wants a visitor to take), then reuse it in each analysis instead of re-establishing the basics.

This suite is **URL-first**: you read the live page and pull the facts yourself; the user only
confirms them and fills the few things a page can't tell you (the real business goal, the audience,
who they see as competitors). Written for **business owners and marketers**, not developers. Keep
the language plain and explain any shorthand.

## Why a Site Snapshot

The Messaging, Conversion, SEO, and UX/Technical skills all need the same starting facts: the site's
purpose, its primary conversion, its audience, and which pages to look at. Capturing them once:

- removes repetition across skills,
- keeps every downstream finding anchored to the **same primary goal** (so recommendations pull in
  one direction),
- gives the user a single profile they can update as the site changes.

This skill is intake only. It does **not** grade or produce findings; it feeds the skills that do.

## What the snapshot captures

1. **Site & business:** the site/brand name and a one-line description of what it does; the
   category (e-commerce, SaaS, lead-gen / services, local business, content/media, other).
2. **Primary conversion goal:** the single most important action a visitor should take (buy, book a
   call, request a quote, sign up, subscribe, contact, download). Plus any secondary goals. *This is
   the anchor for the whole audit.*
3. **Audience:** who the site is for and what they're trying to do when they arrive.
4. **Page inventory:** the key pages and page *types* (home, services, products, case studies,
   articles, about, contact). Note which is the main entry page. This drives the suite's two-tier depth:
   the **homepage** gets the full in-depth audit, while the **secondary page types** get a quick site-wide
   SEO sweep (see [report-format.md](../../report-format.md), "Audit depth").
5. **Platform & signals:** the platform/CMS if detectable (WordPress, Shopify, Webflow, Wix, custom…),
   whether analytics/pixels are present, HTTPS, language/region (**only what's actually observable**).
6. **Competitors / references:** 1–3 sites the user compares themselves to (optional, user-supplied).
7. **Context:** the URL(s) audited, and any constraints (e.g. "don't judge the blog", "mobile
   matters most").

## Conversation flow

You do the reading; keep the user's part short. Aim for **one fetch + one confirmation pass** (roughly
3–5 questions, 2–3 at a time).

> **How to run this session: read before you start.**
> - **Fetch first, ask second.** As soon as you have the URL, fetch it and extract everything you can
>   (name, what it does, category, likely primary CTA, key pages from the nav, platform signals). Come
>   to the user with a *draft* snapshot to confirm, not a blank questionnaire.
> - **Only ask what the page can't tell you.** The real business goal, the true target audience, and
>   who they consider competitors are the three things you usually must ask. Everything else, propose
>   from what you read and let them correct it.
> - **Nail the primary goal.** If the page has several calls to action, ask the user which single
>   action matters most commercially; the whole audit is scored against it. Don't guess silently.
> - **Prefer pickable options.** For category (e-commerce / SaaS / lead-gen / local / content) and
>   primary goal (buy / book / quote / sign up / subscribe / contact / download), offer a short
>   pickable list rather than open prompts.
> - **Don't invent.** If you can't fetch the page (blocked, JS-only, paywalled), say so and ask the
>   user to paste the key pages' text or a screenshot. Anything genuinely unknown stays **TBD**, never
>   a guess; the later skills and the final reconciliation pass fill it in.

### Required inputs — capture before delivering
Check each off (or mark **TBD**) before Step 4 (Confirm & deliver):
- [ ] Site/brand name, one-line description, and the **URL(s)** audited
- [ ] Category (e-commerce / SaaS / lead-gen·services / local / content / other)
- [ ] **Primary conversion goal** (the single most important visitor action) + any secondary goals
- [ ] Audience: who it's for and their intent
- [ ] Page inventory: the key pages, and the main entry page
- [ ] Platform & signals: platform/CMS, analytics present?, HTTPS, language/region (observable only)
- [ ] Competitors / references (optional) and any constraints

### Step 1: Get the URL and fetch it

Ask for the website URL (and any specific pages the user cares about). The moment you have it, **fetch
the page(s)** and read them. From what you read, draft:
- the site name and a one-line description of what it does,
- the likely category,
- the calls to action you can see (to propose the primary goal),
- the key pages from the navigation,
- observable platform/tech signals (generator meta tag, script hosts, HTTPS, `lang`).

If the fetch fails or the page is essentially empty without JavaScript, tell the user plainly and ask
them to paste the homepage (and one or two key pages') text, or share a screenshot.

### Step 2: Confirm the draft, fill the gaps

Show the user your draft snapshot and ask them to confirm or correct it. Ask the 2–3 things the page
can't tell you:
- **Primary goal:** "Of everything on the site, what's the single most important thing you want a
  visitor to do?" (offer the pickable list).
- **Audience:** "Who is this really for, and what are they trying to do when they land?"
- **Competitors (optional):** "Whose sites do you compare yourself to?"

### Step 3: Note constraints & scope

Ask if there's anything specific to focus on or ignore (a page in progress, mobile-first, a specific
landing page for a campaign). Record it so the analysis skills respect it.

### Step 4: Confirm & deliver

Summarise the snapshot back and ask for a final confirm. Mark anything unknown as **TBD** rather than
guessing. Then deliver the files.

### Step 5: Hand off (and note the run layer)

Tell the user the snapshot is ready. The recommended next step is the **Goals & Discovery** interview. It
captures how they feel about the site and what they want it to achieve, and it runs *while* the site is
being read/measured (it's paced by the owner answering, so in the Extended layer you launch the background
scans first and interview during them). After that, any of the five analyses (**Messaging & Clarity**,
**Conversion**, **SEO**, **UX & Technical**, **Design & Visual**) can run; they're independent. From here
on, the user pastes this snapshot (and the Goals & Discovery brief) whenever a later skill asks about the site.

Also tell them which **layer** this audit will run in (both are free; see
[report-format.md](../../report-format.md), "Basic & Extended layers"):
- **Extended:** the measured tools can run here (you can execute `python`/Playwright), so the audit will
  include real Core Web Vitals, accessibility, mobile, design-token and tracking measurements.
- **Basic:** the tools can't run in this environment (e.g. the Claude web/desktop app), so those checks
  will be reported as *"not measured: available with the Extended layer"* and the audit is Claude's
  read-and-reason review. Everything else is identical.
Quietly test whether a tool can run (or infer from the environment) and say which mode they're getting.

## Output: deliver the snapshot as files

Generate TWO files (`site-snapshot.md` and a styled, self-contained `site-snapshot.html`) and share them
with the user. The `.html` must follow the shared navigation rules: cross-links to the other deliverables,
hover hints on short terms, and end with the Print hint (no `pagenav` mid-session). Format and the full
shared design system (CSS + page frame). See: [references/rules-snapshot.md](references/rules-snapshot.md),
section "Output file format".

Save both files and share them with the user for download.

## Add to the Website Audit Report

This suite is meant to run as one continuous session, start to finish. **Deliver only your own two files
now** (`.md` + `.html`). Keep the **Website Audit Report** as an **internal running document**. Do **not**
create, show, or hand over a report file mid-session; it is assembled and delivered only at the very end
(by the Action Report skill). As the first skill, start that internal record and add the **Site Snapshot**
section from what you just captured. Full format and section order:
[report-format.md](../../report-format.md).

## Critical rules

1. **URL-first.** Fetch and read the site before asking anything. Come with a draft, not a blank form.
2. **Intake, not analysis.** No grades, no findings here; that's the five analysis skills' job. Keep it
   to one short pass.
3. **Don't invent.** Report only observable signals; mark unknowns **TBD**. The Action Report's
   reconciliation pass backfills any TBDs answered later, so leave a genuine unknown as **TBD**, never a
   guess.
4. **One primary goal, anchored.** Pin down the single most important conversion and make the user
   confirm it; every later finding is judged against it.
5. **One snapshot, reused everywhere.** Remind the user to paste this into the other skills instead of
   re-establishing the site.
6. **Plain language.** The audience is business owners/marketers. Explain any shorthand; no unexplained
   jargon.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
