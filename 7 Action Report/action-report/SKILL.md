---
name: action-report
description: >
  The capstone of the Ananas-Agency Website Audit Suite. Synthesises the findings from the Messaging,
  Conversion, SEO, and UX/Technical analyses into one prioritised action plan: an overall site
  scorecard (letter grades per dimension + overall), an Impact × Effort priority matrix that sorts
  every finding into Quick Wins / Big Bets / Fill-ins / Skip, a phased roadmap (first two weeks /
  30–60 / 60–90 days), and the single consolidated Website Audit Report the user takes away. Use this
  skill when the user wants to: pull the audit together, get the action plan / roadmap / priorities,
  see the overall grade, know what to fix first, or produce the final report. Trigger: "action plan",
  "what should I fix first", "prioritise the findings", "overall grade", "final report", "audit
  summary", "roadmap", "put it all together", "quick wins".
---

# Action Report (Ananas-Agency — Website Audit capstone)

## Goal

Turn the five analyses into a decision. Produce: an **overall scorecard**, an **Impact × Effort priority
matrix**, a **prioritised roadmap** phased into first-two-weeks / 30–60 / 60–90 days, and the single
consolidated **Website Audit Report** the user keeps. This is where a pile of findings becomes "do these
three things Monday."

Written for **business owners and marketers**: the report leads with the decision, not the detail.

## Inputs

- The run folder `audit-<slug>/` with its `audit-data/` JSON: the Site Snapshot (`site-snapshot.json`), the
  Goals & Discovery brief if it was captured (`goals.json`; context, not findings), and whichever of the five
  analyses were run (`messaging.json`, `conversion.json`, `seo.json`, `ux-technical.json`, `design.json`).
  The shapes are in [audit-data-format.md](../../audit-data-format.md).
- Read the findings, grades and "what's working" notes from those files. **Do not re-analyse.** If some
  analyses weren't run, proceed with what exists and say clearly which dimensions are missing.

> **Precondition: check before you build anything.** Every grade in the report is judged against a goal the
> owner stated. If `goals.json` doesn't exist, **Goals & Discovery never ran**: stop and run it now (it's a
> short interview, and the scans are already done). Don't write the owner's brief from the scans, because a
> brief you inferred yourself is fabrication. Only if the owner is genuinely unavailable do you go on. Then
> make the first entry in `rating_notes` a plain sentence saying the audit is ungrounded because no owner
> input was available (the builder prints rating notes in the executive summary), and tell the user so in
> step 7. Do the same if `goals.json` exists but every owner field is NOT CAPTURED.

## What the final build produces

You write the judgement. The builder computes the grade, the matrix, the roadmap and the phased plan from the
dimension files, and writes the pages (see [references/rules-action-report.md](references/rules-action-report.md)
for what it computes and why):

1. The **overall scorecard**: dimension grades side by side and the overall grade.
2. The **"2026 standard vs your site" scorecard**, from the benchmark rows you write.
3. The **Impact × Effort matrix**, the **prioritised roadmap** and the **phased plan**.
4. The **executive summary** and the Action Report page (`action-report.html` and `.md`).
5. Every other page that has data, and the consolidated report `_<slug>-website-audit-report`.
6. The ZIP, `audit-<slug>/<slug>-website-audit.zip`.

## Conversation flow

### Step 1: Gather

Read every `audit-<slug>/audit-data/*.json`. Note which dimensions are missing. Check the precondition above.

### Step 2: Normalise the ratings

Compare `impact` and `effort` across the dimension files, using "Normalising across dimensions" in
[references/rules-action-report.md](references/rules-action-report.md). An Impact 5 in one analysis should be as
serious as an Impact 5 in another. Edit the outliers in the dimension files and record each change as a line in
`rating_notes`.

### Step 3: Write `action-report.json`

Create `audit-<slug>/audit-data/action-report.json` ([audit-data-format.md](../../audit-data-format.md),
"action-report.json"):

- `strengths`: one or two genuine strengths.
- `benchmarks`: one row for each line of the table "The 2026 baseline in one line per dimension" in
  [benchmarks-2026.md](../../benchmarks-2026.md), using that line's text from the "The 2026 bar" column as
  `standard`. Mark each `met`, `gap` or `na`, with a short note and `keys` for the findings that close the
  gap. A `note` may cite findings as `[[key]]`.
- `rating_notes`: the ratings you changed in step 2.

### Step 4: Reconcile the Site Snapshot and audit.json

Edit `site-snapshot.json` with whatever this session actually answered for its `TBD` values. Never invent one.
Also make `audit.json` agree with the settled goal: if the owner settled a different primary goal in Goals &
Discovery, update its `primary_goal` to match.

### Step 5: Run the final build

If the setup check hasn't run in this session, run it (`python "${CLAUDE_PLUGIN_ROOT}/scripts/setup-check.py"`;
use `python3` where `python` isn't available). Then run
`python "${CLAUDE_PLUGIN_ROOT}/scripts/build-report.py" "audit-<slug>" --final`. On exit 2, fix each field it names and run it again. It prints the ZIP path and a
`TBD left: <label>` line for each Site Snapshot value still unknown. Answer each one from the session if you
can. If you can't, leave it as a real unknown and tell the user.

### Step 6: House-style self-check

Read the prose you wrote against "Write like a human" in [report-format.md](../../report-format.md). Rewrite
anything flagged in the JSON, not in the output, then run `--final` again.

### Step 7: Deliver

Give the user `audit-<slug>/<slug>-website-audit.zip` and say: "Open `_<slug>-website-audit-report.html` inside
the zip first." For a partial run, say which dimensions are missing. If the audit is ungrounded, say that too.

## Critical rules

1. **Don't re-analyse.** Synthesise from the findings already produced. New insight is fine; re-running
   the analyses is not.
2. **Lead with the decision.** Quick wins and the overall grade come first; detail follows.
3. **Handle partial runs honestly.** Report only the dimensions that ran; name the gaps.
4. **Claude writes no HTML.** Text fields are light Markdown, and other findings are referenced as `[[key]]`.
5. **Edit the JSON, never the built files.** The next build overwrites them.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
