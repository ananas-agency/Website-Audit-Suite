# JSON Schemas

Machine-readable versions of the files the skills write into `audit-<slug>/audit-data/`. They use JSON Schema draft 2020-12.

| File | Schema | Written by |
|---|---|---|
| `audit.json` | [`audit.schema.json`](audit.schema.json) | Site Snapshot (the first skill) |
| `site-snapshot.json` | [`site-snapshot.schema.json`](site-snapshot.schema.json) | Site Snapshot |
| `goals.json` | [`goals.schema.json`](goals.schema.json) | Goals Discovery |
| `messaging.json` | [`dimension.schema.json`](dimension.schema.json) | Messaging Clarity |
| `conversion.json` | [`dimension.schema.json`](dimension.schema.json) | Conversion CRO |
| `seo.json` | [`dimension.schema.json`](dimension.schema.json) | SEO Content |
| `ux-technical.json` | [`dimension.schema.json`](dimension.schema.json) | UX Technical |
| `design.json` | [`dimension.schema.json`](dimension.schema.json) | Design Visual |
| `security.json` | [`dimension.schema.json`](dimension.schema.json) | Security (via `scripts/security-scan.py`) |
| `action-report.json` | [`action-report.schema.json`](action-report.schema.json) | Action Report |

To check a file with any JSON Schema tool, for example:

```
python -m pip install check-jsonschema
check-jsonschema --schemafile schemas/goals.schema.json audit-x/audit-data/goals.json
```

[`audit-data-format.md`](../audit-data-format.md) is the prose explanation of the format, and `scripts/build-report.py` is the final judge: it also checks things a schema can't, such as `[[key]]` references between files, unique finding keys, rubric weights adding up to 100, and `measured` findings having a scan behind them.
