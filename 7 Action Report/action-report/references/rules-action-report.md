# Action Report Rules — Detailed Reference

This skill synthesises the whole audit. The Finding format, Impact/Effort scales, priority quadrants and
grade bands live in [report-format.md](../../../report-format.md); the builder assigns the IDs and writes the
consolidated report and the ZIP (see [audit-data-format.md](../../../audit-data-format.md)). This reference adds
the synthesis method, the matrix and roadmap layout, the phased plan, and the one CTA block.

## Computing the overall grade

- Take each **completed** dimension's 0–100 score (Messaging, Conversion, SEO, UX/Technical).
- **Overall score = the mean of the completed dimension scores**, rounded to the nearest whole number.
- Map to a letter with the shared bands (A 90–100 · B 80–89 · C 70–79 · D 60–69 · F 0–59).
- If not all five ran, average only what exists and state plainly which dimensions are missing (e.g.
  "Overall C (74), from Messaging and SEO only; Conversion and UX/Technical not run").
- The grade is an **expert judgement**, not a measurement; say so.

## Normalising across dimensions

Before building the matrix, sanity-check that Impact and Effort mean the same thing across the five
analyses. An "Impact 5" in Conversion (kills the primary conversion) should be as serious as an "Impact 5"
in SEO (blocks the whole site from being indexed). If an outlier is mis-rated, adjust it and record the change
in `rating_notes` so the roadmap ordering is trustworthy.

## The Impact × Effort matrix

The builder places **every** finding from every dimension into one quadrant, by its Impact (High = 3–5, Low = 1–2) and
Effort (Low = 1–2, High = 3–5):

| | Low effort (1–2) | High effort (3–5) |
|---|---|---|
| **High impact (3–5)** | **Quick Win** — do first | **Big Bet** — plan & schedule |
| **Low impact (1–2)** | **Fill-in** — do when convenient | **Skip** — backlog |

It lists the findings in each quadrant by ID, highest impact first, with each finding in exactly one cell.
You don't list them.

## The prioritised roadmap

The builder writes a single ordered list the user can work top-down:
1. **Quick Wins:** impact descending (these are the first-two-weeks list).
2. **Big Bets:** impact descending (schedule these).
3. **Fill-ins:** do alongside the above when convenient.
4. **Skip:** listed as backlog, explicitly deprioritised (don't hide them; just mark them low value).

Each roadmap row holds the ID (linked + tooltipped), the one-line issue, the fix in brief, Impact, Effort,
and the dimension it came from.

## The phased plan

- **Your first two weeks:** the Quick Wins, as a checklist. Each item links to the finding's dimension page.
- **Days 30–60:** kick off the top Big Bets; start measuring against the site's **primary conversion goal**
  (recommend the user watch the relevant analytics, e.g. GA4 conversions, form completions).
- **Days 60–90:** finish the Big Bets, action the worthwhile Fill-ins, then **re-run the audit** to see the
  grades move.

## The agency CTA block

The builder adds the one call-to-action block, to the Action Report only; write no CTA text yourself.

---

## Output
Write the results to the run folder as described in [audit-data-format.md](../../../audit-data-format.md),
section "action-report.json", then build the page.

---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License. Keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../../LICENSE)
