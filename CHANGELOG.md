# Changelog

All notable changes to this project are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.0] - 2026-11-09

First release as a Claude Code plugin.

### Added

- Claude Code plugin and marketplace manifests. Install with `/plugin marketplace add` and `/plugin install`.
- A shared `scripts/` folder that every skill runs from the plugin folder.
- `scripts/setup-check.py`: checks Python, Playwright and Chromium and prints which layer you get
  (`MODE: extended`, `basic` or `unsupported`), with the commands to fix what is missing.
- A report builder, `scripts/build-report.py`. Skills now write their results once as JSON; the builder
  checks it and writes the `.md` and `.html` pages, the consolidated report and a ZIP bundle.
- The audit-data format: [audit-data-format.md](audit-data-format.md), with the report method slimmed down to
  [report-format.md](report-format.md).
- JSON Schemas for the audit data files in [schemas/](schemas/README.md).
- A ninth skill, **8 Security**: a passive, outside-in security check covering HTTPS and certificate, security
  headers, cookies, information leaks, forms and SPF and DMARC email records. It shows a disclaimer first and
  asks about ownership. With the owner's yes (`--probe-files`) it also checks a list of well-known file
  addresses, chosen by the site's platform. The file checks are paced and stop early if the site stops
  answering.
  Includes `scripts/security-scan.py` and `scripts/security-report.py`.
- Standard-library tests for the builder, the scans, the Security step, the schemas and the packaging.

### Changed

- The skills no longer write HTML. The builder does, from the JSON.
- Output templates were removed from the skills' rules files; the builder owns the page layout.
- The Action Report gathers the JSON files and runs the final build.
- The README was rewritten for the plugin, with diagrams of the step flow, the scripts and the Security check.
- The Claude app version is frozen in [claude-app/](claude-app/README.md) and is no longer maintained. The old
  copy-a-folder install is gone; delete copies in `~/.claude/skills/` before installing the plugin.

### Removed

- The `.skill` packages and the Handbook left the skill folders and the repo root; they now live only in
  [claude-app/](claude-app/README.md).
- The per-skill copies of the scan scripts (every skill uses the shared `scripts/` folder) and the old
  packaging and Handbook build scripts.

## [1.0.0]

The original eight skills for the Claude app, with the Handbook. This version is kept as it was in
[claude-app/](claude-app/README.md).
