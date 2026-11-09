"""Run data model, loader and validation for the report builder.

Claude writes one JSON file per skill into RUN_DIR/audit-data/. load_run reads them,
checks every rule, and raises a single DataError listing every problem found.
"""
from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from . import (BENCHMARK_STATUSES, BROWSERLESS_SCANS, DIMENSIONS, KEY_PATTERN, KEY_REF, RESULTS, SCAN_BACKING,
               SCAN_FILES)

_ANY_REF = re.compile(r"\[\[([^\[\]]+)\]\]")  # finds candidates so malformed ones are reported
_KEY_REF = re.compile(KEY_REF)


class DataError(Exception):
    """Raised when run data is invalid. `.errors` holds one message per problem."""

    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("\n".join(self.errors))


@dataclass
class Finding:
    key: str
    title: str
    issue: str
    impact_text: str
    fix: str
    impact: int
    effort: int
    evidence: str = ""
    measured: bool = False
    fix_brief: str = ""
    dim: str = ""    # set by rules
    id: str = ""     # set by rules
    quad: str = ""   # set by rules


@dataclass
class RubricRow:
    criterion: str
    result: str
    weight: int


@dataclass
class Dimension:
    page: str
    prefix: str
    title: str
    utm: str
    verdict: str
    rubric: list = field(default_factory=list)
    findings: list = field(default_factory=list)
    strengths: list = field(default_factory=list)
    notes: str = ""
    extra: list = field(default_factory=list)
    score: int = 0   # set by rules
    grade: str = ""  # set by rules


@dataclass
class Snapshot:
    description: str
    sections: list = field(default_factory=list)


@dataclass
class Goals:
    framing: str
    brief: list = field(default_factory=list)
    stated_vs_observed: list = field(default_factory=list)
    tensions: list = field(default_factory=list)
    advice: list = field(default_factory=list)
    shapes: str = ""


@dataclass
class Benchmark:
    standard: str
    status: str
    note: str
    keys: list = field(default_factory=list)


@dataclass
class Action:
    strengths: list = field(default_factory=list)
    benchmarks: list = field(default_factory=list)
    rating_notes: list = field(default_factory=list)


@dataclass
class Run:
    dir: Path
    site: str
    url: str
    slug: str
    date: str
    tagline: str
    primary_goal: str
    mode: str
    logo: str
    snapshot: "Snapshot | None" = None
    goals: "Goals | None" = None
    dims: dict = field(default_factory=dict)
    action: "Action | None" = None
    scans: dict = field(default_factory=dict)


# ---------------------------------------------------------------- validation helpers

class _Ctx:
    """Collects errors for one file, plus every string found in it."""

    def __init__(self, fname, errors):
        self.fname = fname
        self.errors = errors
        self.texts = []
        self.key_refs = []  # (path, finding key) pairs to check against the loaded findings
        self.measured_at = []  # indexes of findings marked measured: true

    def err(self, path, msg):
        self.errors.append(f"{self.fname}: {path + ' ' if path else ''}{msg}")

    def collect(self, value):
        if isinstance(value, str):
            self.texts.append(value)
        elif isinstance(value, list):
            for v in value:
                self.collect(v)
        elif isinstance(value, dict):
            for v in value.values():
                self.collect(v)


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _obj(ctx, value, path, required, optional=()):
    """Check that value is an object with only the allowed fields. True when usable."""
    if not isinstance(value, dict):
        ctx.err(path, "must be an object")
        return False
    for k in value:
        if k not in required and k not in optional:
            where = f"{path}." if path else ""
            ctx.errors.append(f"{ctx.fname}: unknown field '{where}{k}'")
    for k in required:
        if k not in value:
            ctx.err(path, f"missing required field '{k}'")
    return True


def _text(ctx, obj, key, path, required=True):
    """Return a string field, recording an error when it is empty or not text."""
    p = f"{path}.{key}" if path else key
    if key not in obj:
        return ""
    v = obj[key]
    if not isinstance(v, str):
        ctx.err(p, "must be text")
        return ""
    if required and not v.strip():
        ctx.err(p, "must not be empty")
    return v


def _text_list(ctx, obj, key, path, required=True):
    p = f"{path}.{key}" if path else key
    if key not in obj:
        return []
    v = obj[key]
    if not isinstance(v, list):
        ctx.err(p, "must be a list")
        return []
    if required and not v:
        ctx.err(p, "must not be empty")
    out = []
    for i, item in enumerate(v):
        if not isinstance(item, str) or not item.strip():
            ctx.err(f"{p}[{i}]", "must be non-empty text")
        else:
            out.append(item)
    return out


def _pairs(ctx, obj, key, path):
    """A non-empty list of [label, value] text pairs."""
    p = f"{path}.{key}" if path else key
    if key not in obj:
        return []
    v = obj[key]
    if not isinstance(v, list) or not v:
        ctx.err(p, "must be a non-empty list")
        return []
    out = []
    for i, row in enumerate(v):
        if (not isinstance(row, list) or len(row) != 2
                or not all(isinstance(c, str) for c in row)):
            ctx.err(f"{p}[{i}]", "must be a [label, value] pair of text")
        elif not row[0].strip():
            ctx.err(f"{p}[{i}]", "label must not be empty")
        else:
            out.append((row[0], row[1]))
    return out


def _triples(ctx, d, key, names):
    """A non-empty list of objects with the given text fields, as tuples."""
    out = []
    if key not in d:
        return out
    if not isinstance(d[key], list) or not d[key]:
        ctx.err(key, "must be a non-empty list")
        return out
    for i, item in enumerate(d[key]):
        p = f"{key}[{i}]"
        if _obj(ctx, item, p, names):
            vals = tuple(_text(ctx, item, n, p) for n in names)
            if all(vals):
                out.append(vals)
    return out


def _unix_newlines(value):
    """Turn CRLF and lone CR in every text into LF, so HTML and Markdown see the same line breaks."""
    if isinstance(value, str):
        return value.replace("\r\n", "\n").replace("\r", "\n")
    if isinstance(value, list):
        return [_unix_newlines(v) for v in value]
    if isinstance(value, dict):
        return {k: _unix_newlines(v) for k, v in value.items()}
    return value


def _load_json(path: Path, fname, errors):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{fname}: cannot read file ({exc.strerror or exc})")
        return None
    try:
        return _unix_newlines(json.loads(text))
    except ValueError as exc:
        errors.append(f"{fname}: invalid JSON ({exc})")
        return None


# ---------------------------------------------------------------- per-file parsers

def _parse_audit(ctx, d):
    if not _obj(ctx, d, "", ("site", "url", "primary_goal"),
                ("tagline", "slug", "date", "mode", "logo")):
        return None
    out = {k: _text(ctx, d, k, "") for k in ("site", "url", "primary_goal")}
    for k in ("tagline", "slug", "date", "mode", "logo"):
        out[k] = _text(ctx, d, k, "", required=False)
    if out["mode"] and out["mode"] not in ("extended", "basic"):
        ctx.err("mode", f"must be 'extended' or 'basic', got '{out['mode']}'")
    if out["slug"] and not re.fullmatch(KEY_PATTERN, out["slug"]):
        ctx.err("slug", "must be lowercase letters, digits and hyphens")
    if out["date"]:
        try:
            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", out["date"]):
                raise ValueError(out["date"])  # newer Pythons also accept 20261106
            datetime.date.fromisoformat(out["date"])
        except ValueError:
            ctx.err("date", f"must be an ISO date (YYYY-MM-DD), got '{out['date']}'")
    ctx.collect(d)
    return out


def _parse_rubric(ctx, d):
    rubric = []
    if "rubric" not in d:
        return rubric
    if not isinstance(d["rubric"], list) or not d["rubric"]:
        ctx.err("rubric", "must be a non-empty list")
        return rubric
    for i, r in enumerate(d["rubric"]):
        p = f"rubric[{i}]"
        if not _obj(ctx, r, p, ("criterion", "result", "weight")):
            continue
        crit = _text(ctx, r, "criterion", p)
        res, w = r.get("result"), r.get("weight")
        if "result" in r and res not in RESULTS:
            ctx.err(f"{p}.result", f"must be Pass, Partial or Fail, got {res!r}")
        if "weight" in r and (not _is_int(w) or w < 1):
            ctx.err(f"{p}.weight", f"must be a positive integer, got {w!r}")
        if crit and res in RESULTS and _is_int(w) and w >= 1:
            rubric.append(RubricRow(crit, res, w))
    return rubric


def _parse_findings(ctx, d, page, keys):
    findings = []
    if "findings" not in d:
        return findings
    if not isinstance(d["findings"], list):
        ctx.err("findings", "must be a list")
        return findings
    text_fields = ("key", "title", "issue", "impact_text", "fix")
    for i, f in enumerate(d["findings"]):
        p = f"findings[{i}]"
        if not _obj(ctx, f, p, text_fields + ("impact", "effort"),
                    ("evidence", "measured", "fix_brief")):
            continue
        vals = {k: _text(ctx, f, k, p) for k in text_fields}
        for k in ("evidence", "fix_brief"):
            vals[k] = _text(ctx, f, k, p, required=False)
        nums_ok = True
        for k in ("impact", "effort"):
            v = f.get(k)
            if k not in f:
                nums_ok = False
            elif not _is_int(v) or not 1 <= v <= 5:
                ctx.err(f"{p}.{k}", f"must be 1-5, got {v}")
                nums_ok = False
        measured = f.get("measured", False)
        if not isinstance(measured, bool):
            ctx.err(f"{p}.measured", "must be true or false")
            measured = False
        elif measured:
            ctx.measured_at.append(i)
        key = vals["key"]
        if key:
            if not re.fullmatch(KEY_PATTERN, key):
                ctx.err(f"{p}.key", f"must match {KEY_PATTERN}, got {key!r}")
            else:
                keys.setdefault(key, []).append(ctx.fname)
        if nums_ok and all(vals[k] for k in text_fields):
            findings.append(Finding(impact=f["impact"], effort=f["effort"],
                                    measured=measured, dim=page, **vals))
    return findings


def _parse_dimension_body(ctx, d, page, keys):
    """The per-file checks every dimension page gets. Returns the parsed fields, or None if d isn't an object."""
    if not _obj(ctx, d, "", ("verdict", "rubric", "findings", "strengths"), ("notes", "extra")):
        return None
    verdict = _text(ctx, d, "verdict", "")
    notes = _text(ctx, d, "notes", "", required=False)
    strengths = _text_list(ctx, d, "strengths", "")
    rubric = _parse_rubric(ctx, d)
    total = sum(r.weight for r in rubric)
    if rubric and total != 100 and len(rubric) == len(d["rubric"]):  # skip when invalid rows were dropped
        ctx.err("", f"rubric weights sum to {total}, must be 100")
    findings = _parse_findings(ctx, d, page, keys)
    extra = []
    if "extra" in d:
        if not isinstance(d["extra"], list):
            ctx.err("extra", "must be a list")
        else:
            for i, e in enumerate(d["extra"]):
                p = f"extra[{i}]"
                if _obj(ctx, e, p, ("title", "body")):
                    t, b = _text(ctx, e, "title", p), _text(ctx, e, "body", p)
                    if t and b:
                        extra.append((t, b))
    ctx.collect(d)
    return verdict, rubric, findings, strengths, notes, extra


def _parse_dimension(ctx, d, page, keys):
    body = _parse_dimension_body(ctx, d, page, keys)
    if body is None:
        return None
    _, prefix, title, utm = next(t for t in DIMENSIONS if t[0] == page)
    verdict, rubric, findings, strengths, notes, extra = body
    return Dimension(page, prefix, title, utm, verdict, rubric, findings, strengths, notes, extra)


def _check_duplicate_keys(keys, errors):
    for key, files in keys.items():
        if len(set(files)) > 1:
            errors.append(f"duplicate key '{key}' in {', '.join(files)}")
        elif len(files) > 1:
            times = "twice" if len(files) == 2 else f"{len(files)} times"
            errors.append(f"duplicate key '{key}' {times} in {files[0]}")


def _check_text_refs(ctx, keys, errors):
    seen = set()
    for text in ctx.texts:
        for raw in _ANY_REF.findall(text):
            if raw in seen:
                continue
            seen.add(raw)
            if not _KEY_REF.fullmatch(f"[[{raw}]]"):
                errors.append(f"{ctx.fname}: [[{raw}]] must not contain spaces; write [[{raw.strip()}]]")
            elif raw not in keys:
                errors.append(f"{ctx.fname}: [[{raw}]] does not name any finding")


def validate_dimension(raw, fname):
    """Check one dimension-style page file on its own; any page name works.

    Returns (errors, rubric, findings). Findings have dim="". Covers the per-file checks load_run gives a
    dimension file, plus duplicate keys and [[key]] references within this one file.
    """
    errors: list = []
    keys: dict = {}
    ctx = _Ctx(fname, errors)
    body = _parse_dimension_body(ctx, raw, "", keys)
    _check_duplicate_keys(keys, errors)
    _check_text_refs(ctx, keys, errors)
    if body is None:
        return errors, [], []
    return errors, body[1], body[2]


def _parse_snapshot(ctx, d):
    if not _obj(ctx, d, "", ("description", "sections")):
        return None
    desc = _text(ctx, d, "description", "")
    sections = []
    if "sections" in d:
        if not isinstance(d["sections"], list) or not d["sections"]:
            ctx.err("sections", "must be a non-empty list")
        else:
            for i, s in enumerate(d["sections"]):
                p = f"sections[{i}]"
                if _obj(ctx, s, p, ("title", "rows")):
                    sections.append((_text(ctx, s, "title", p), _pairs(ctx, s, "rows", p)))
    ctx.collect(d)
    return Snapshot(desc, sections)


def _parse_goals(ctx, d):
    req = ("framing", "brief", "stated_vs_observed", "tensions", "advice", "shapes")
    if not _obj(ctx, d, "", req):
        return None
    goals = Goals(
        framing=_text(ctx, d, "framing", ""),
        brief=_pairs(ctx, d, "brief", ""),
        stated_vs_observed=_triples(ctx, d, "stated_vs_observed", ("said", "observed", "gap")),
        tensions=_text_list(ctx, d, "tensions", ""),
        advice=_triples(ctx, d, "advice", ("headline", "detail", "analysis")),
        shapes=_text(ctx, d, "shapes", ""),
    )
    ctx.collect(d)
    return goals


def _parse_action(ctx, d):
    if not _obj(ctx, d, "", ("strengths", "benchmarks"), ("rating_notes",)):
        return None
    strengths = _text_list(ctx, d, "strengths", "")
    notes = _text_list(ctx, d, "rating_notes", "", required=False)
    benchmarks = []
    if "benchmarks" in d:
        if not isinstance(d["benchmarks"], list) or not d["benchmarks"]:
            ctx.err("benchmarks", "must be a non-empty list")
        else:
            for i, b in enumerate(d["benchmarks"]):
                p = f"benchmarks[{i}]"
                if not _obj(ctx, b, p, ("standard", "status", "note"), ("keys",)):
                    continue
                std, note = _text(ctx, b, "standard", p), _text(ctx, b, "note", p)
                st = b.get("status")
                if "status" in b and st not in BENCHMARK_STATUSES:
                    ctx.err(f"{p}.status", f"must be met, gap or na, got {st!r}")
                bkeys = _text_list(ctx, b, "keys", p, required=False)
                if isinstance(b.get("keys"), list):
                    ctx.key_refs += [(f"{p}.keys[{j}]", k.strip()) for j, k in enumerate(b["keys"])
                                     if isinstance(k, str) and k.strip()]
                if std and note and st in BENCHMARK_STATUSES:
                    benchmarks.append(Benchmark(std, st, note, bkeys))
    ctx.collect(d)
    return Action(strengths, benchmarks, notes)


# ---------------------------------------------------------------- loader

def _default_slug(url: str, site: str) -> str:
    host = urlparse(url if "//" in url else "//" + url).hostname or ""
    if host.startswith("www."):
        host = host[4:]
    label = re.sub(r"[^a-z0-9]+", "-", host.split(".")[0].lower()).strip("-")
    return label or re.sub(r"[^a-z0-9]+", "-", site.lower()).strip("-") or "site"


def load_run(run_dir: Path) -> Run:
    """Load and validate a run folder. Raises one DataError holding every problem."""
    run_dir = Path(run_dir)
    data_dir = run_dir / "audit-data"
    errors: list = []
    keys: dict = {}      # finding key -> files that define it
    contexts: list = []  # one per parsed file, for the [[key]] reference check

    def read(name, parser, *args):
        path = data_dir / name
        if not path.is_file():
            return None
        raw = _load_json(path, name, errors)
        if raw is None:
            return None
        ctx = _Ctx(name, errors)
        contexts.append(ctx)
        return parser(ctx, raw, *args)

    if not (data_dir / "audit.json").is_file():
        errors.append("audit.json: required file not found in audit-data/")
    audit = read("audit.json", _parse_audit)
    snapshot = read("site-snapshot.json", _parse_snapshot)
    goals = read("goals.json", _parse_goals)
    dims = {}
    measured_ctx = []  # (page, ctx) for the measured-claim check once the scans are known
    for page, *_ in DIMENSIONS:
        dim = read(f"{page}.json", _parse_dimension, page, keys)
        if dim is not None:
            dims[page] = dim
            measured_ctx.append((page, contexts[-1]))
    action = read("action-report.json", _parse_action)

    _check_duplicate_keys(keys, errors)

    for ctx in contexts:
        _check_text_refs(ctx, keys, errors)

    for ctx in contexts:
        for path, key in ctx.key_refs:
            if key not in keys:
                ctx.err(path, f"names unknown finding '{key}'")

    scans = {}
    for name in SCAN_FILES:
        p = run_dir / name
        if p.is_file():
            raw = _load_json(p, name, errors)
            if isinstance(raw, dict):
                scans[name] = raw
            elif raw is not None:
                errors.append(f"{name}: must be a JSON object")

    if audit is not None:
        mode = audit["mode"] or ("extended" if scans else "basic")
        for page, ctx in measured_ctx:
            backing = SCAN_BACKING.get(page, SCAN_FILES)
            usable = [f for f in backing if mode != "basic" or f in BROWSERLESS_SCANS]
            if any(f in scans for f in usable):
                continue
            # A Basic run can't have browser scans; say so unless the page has a no-browser scan that is just missing.
            msg = ("is marked measured but no scan for this page ran" if usable
                   else "is marked measured but this is a basic run, so no browser scan ran")
            for i in ctx.measured_at:
                ctx.err(f"findings[{i}]", msg)

    if errors or audit is None:
        raise DataError(errors)

    return Run(
        dir=run_dir,
        site=audit["site"],
        url=audit["url"],
        slug=audit["slug"] or _default_slug(audit["url"], audit["site"]),
        date=audit["date"] or datetime.date.today().isoformat(),
        tagline=audit["tagline"],
        primary_goal=audit["primary_goal"],
        mode=audit["mode"] or ("extended" if scans else "basic"),
        logo=audit["logo"],
        snapshot=snapshot,
        goals=goals,
        dims=dims,
        action=action,
        scans=scans,
    )
