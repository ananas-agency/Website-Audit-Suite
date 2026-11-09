# Website Audit Suite for the Claude app (frozen version)

This folder holds the suite as it was at commit `7ecf3dc`, for people who use the Claude web or desktop
app or paste the instructions into any chat. These files are frozen and no longer maintained. New work
happens in the Claude Code plugin described in the [main README](../README.md).

What's here:
- Eight `.skill` packages, one per skill, ready to upload to the Claude app.
- [Website Audit Suite - Handbook by Ananas Agency.md](Website%20Audit%20Suite%20-%20Handbook%20by%20Ananas%20Agency.md),
  every skill and reference in one document.

## Path 1: Copy and paste (works on any plan, no setup)
1. Open the Handbook and find the skill you want, for example **Site Snapshot**.
2. Copy that skill's instructions, from its first `#` heading down.
3. Paste them into a new Claude conversation and send: *"Follow these instructions and audit my website,
   here's the URL: …"*.
4. Answer the few questions it asks. It produces your finished document.

> Tip: do **Site Snapshot** first. The analyses build on it. When a later skill asks for your snapshot,
> paste the result you got from Site Snapshot.

## Path 2: Install as a Skill in the Claude app
1. In Claude, open **Settings → Capabilities** and turn on **Skills** (and code execution if prompted).
2. Pick a package from this folder, for example `site-snapshot.skill`. **It's a ZIP**. If the uploader only
   accepts `.zip`, rename it. Click **Upload skill** and select it. Repeat for each skill.
3. Start a chat and describe what you need (*"Audit my website"*, *"Is my homepage message clear?"*,
   *"Give me an SEO review of …"*), and Claude runs the matching skill.

In the Claude app the measured scans usually can't reach your site, so this version gives Claude's
read-and-reason review and marks measured checks as "not measured".

## Recovering the old build tools
The scripts that rebuilt these packages and the Handbook were retired with the move to the plugin. Get
them back from git history if you need them:

```bash
git show 7ecf3dc:scripts/repack-all-skills.py > repack-all-skills.py
git show 7ecf3dc:scripts/build-handbook.py > build-handbook.py
```
