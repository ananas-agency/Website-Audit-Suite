# Audit data format

Each skill writes one JSON file; machine-readable JSON Schemas for them are in [`schemas/`](schemas/README.md). The report builder checks it and makes the pages. You write the data, never the HTML. The builder rejects fields not listed here and tells you which ones. Write each JSON file with your file-writing tool, not a shell heredoc; quotes in the prose break heredocs.

## The run folder

All files live in `audit-<slug>/audit-data/`, inside the user's working directory. `<slug>` is the first label of the site's domain (`ananas-agency.com` gives `ananas-agency`).

The first skill creates `audit-data/audit.json`. Every later skill reuses the same folder. Scan files from the scripts sit in `audit-<slug>/` itself.

## Writing text

Text fields take light Markdown only: `**bold**`, `*italic*`, `` `code` ``, `[text](https://…)`. There is no HTML, so type `<title>` inside backticks if you need to show a tag.

- Refer to another finding as `[[key]]`: its `key` in lowercase letters, digits and hyphens, no spaces. The key must exist in some dimension file. Keys must be unique across all dimension files, so give each skill its own (`vague-headline`, `long-form`, `missing-meta`, `slow-lcp`, `weak-contrast`).
- Never type an ID such as `MSG-01`. The builder assigns IDs, strongest finding first, and renumbers them when ratings change.
- Separate paragraphs with a blank line; a single line break renders as a space. There are no lists, tables or headings (the builder draws tables itself), so write them as sentences.
- Write each finding once. The builder makes both the `.md` and the `.html` from it.
- Don't label priority quadrants. The builder computes them from impact and effort.

Every field named below is required unless marked optional. These lists must not be empty: `sections` and each section's `rows`, `brief`, `stated_vs_observed`, `tensions`, `advice`, `rubric`, `strengths`, `benchmarks`. If there is truly nothing to report, one plain entry is valid, for example "No real tension: the goal and the constraints agree."

## audit.json

Optional: `tagline`, `slug`, `date` (YYYY-MM-DD), `mode`, `logo`. Set `mode` to `extended` or `basic`, from the setup check's `MODE:` line. `logo` is the file name of an image saved in the run folder (`audit-<slug>/`). Leave it out if there is none, and never invent one.

```json
{
  "site": "Ananas Agency",
  "url": "https://ananas-agency.com",
  "primary_goal": "Book discovery calls",
  "mode": "extended"
}
```

## site-snapshot.json

`sections` is a list of `title` plus `rows`. Each row is a `[label, value]` pair. Write `TBD` as the value when the site doesn't show it.

```json
{
  "description": "A small agency site that sells web design to local businesses.",
  "sections": [
    {
      "title": "Site & business",
      "rows": [["Business", "Digital agency"], ["Platform / CMS", "TBD"]]
    }
  ]
}
```

## goals.json

All six fields are required. `brief` holds `[label, value]` pairs. `tensions` is a list of text. `stated_vs_observed` items have `said`, `observed`, `gap`. `advice` items have `headline`, `detail`, `analysis`.

```json
{
  "framing": "The owner wants more booked calls and says the site should *show* the work.",
  "brief": [["Primary goal", "Book discovery calls"]],
  "stated_vs_observed": [
    {
      "said": "We want more calls",
      "observed": "The only contact path is a nine-field form",
      "gap": "The path is longer than the goal needs."
    }
  ],
  "tensions": ["Showing the work competes with a short, clear pitch"],
  "advice": [
    {
      "headline": "Lead with one outcome",
      "detail": "Rewrite the hero around the call.",
      "analysis": "A clear hero gives the form a reason to exist."
    }
  ],
  "shapes": "Every later finding is judged against the call booking goal."
}
```

## Dimension files

One file per dimension: `messaging.json`, `conversion.json`, `seo.json`, `ux-technical.json`, `design.json`. Fields:

- `verdict`: one or two sentences.
- `rubric`: one row per criterion, with `criterion`, `result` and `weight`. Copy each name and weight exactly from the skill's rubric table. Weights are whole numbers and must sum to 100. `result` is `Pass`, `Partial` or `Fail`.
- `findings`: may be an empty list. Each has `key`, `title`, `issue`, `impact_text`, `fix`, `impact` (1-5) and `effort` (1-5). Impact High = 3-5, Low = 1-2. Effort Low = 1-2, High = 3-5.
- Optional per finding: `evidence`, `measured`, `fix_brief`. Set `measured: true` only when a scan backs the finding; the builder rejects it when none of the scans that can back that page's findings is in the run folder. A `basic` run has no browser scans, so only the SEO sweep can back a measured finding there. If `fix_brief` is missing, the builder shortens `fix`.
- `strengths`: list of short text.
- Optional: `notes`, and `extra` (a list of `title` plus `body`). Statements about what could not be assessed (no render, no brand guidelines, the owner's search data) go in `notes`. Every rubric criterion is still rated: use Fail or Partial with the reason in `notes` when it can't be assessed, and never drop a criterion, because the weights must still sum to 100.

```json
{
  "verdict": "The offer is clear to insiders but the **hero** does not say who it is for.",
  "rubric": [
    {"criterion": "Hero states the offer", "result": "Fail", "weight": 60},
    {"criterion": "Proof is near the claim", "result": "Pass", "weight": 40}
  ],
  "findings": [
    {
      "key": "vague-headline",
      "title": "Hero headline is generic",
      "issue": "The headline reads \"We build digital experiences\" and names no audience.",
      "impact_text": "Visitors cannot tell in five seconds whether the site is for them.",
      "fix": "Rewrite the headline around one outcome for one audience.",
      "impact": 5,
      "effort": 2
    }
  ],
  "strengths": ["Plain language, little jargon"]
}
```

## action-report.json

Optional: `rating_notes` (list of text), and `keys` on a benchmark (finding keys it relates to). `status` is `met`, `gap` or `na`.

```json
{
  "strengths": ["Plain language", "A clear primary action"],
  "benchmarks": [
    {
      "standard": "Clear hero message",
      "status": "gap",
      "note": "The headline is generic, see [[vague-headline]].",
      "keys": ["vague-headline"]
    },
    {"standard": "HTTPS everywhere", "status": "met", "note": "All pages load over HTTPS."}
  ],
  "rating_notes": ["Rated on the scans in this run only"]
}
```

## Building

After each skill, run `python "${CLAUDE_PLUGIN_ROOT}/scripts/build-report.py" "audit-<slug>" --page <page>`. The page is `site-snapshot`, `goals`, `messaging`, `conversion`, `seo`, `ux-technical`, `design` or `action-report`. Use `python3` where `python` isn't available.

At the end of the Action Report, run the same command with `--final` instead of `--page <page>`. It writes every page that has data and the ZIP, and prints the ZIP path.

- Exit 0: the files were written.
- Exit 2: the data needs fixing. Each line on stderr names the file and field. Fix them and run again.
- `--final` also prints `TBD left:` lines for Site Snapshot values still marked `TBD`. Fill those in or tell the user.
