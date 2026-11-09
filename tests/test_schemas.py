"""The JSON Schemas in schemas/ against the sample run, a real security.json and the loader (standard library only)."""
import copy
import json
import pathlib
import re
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO  # noqa: E402

sys.path.insert(0, str(REPO / "scripts"))
from report.data import DataError, load_run  # noqa: E402

from test_security_cli import ServerCase  # noqa: E402

SCHEMAS = REPO / "schemas"
SAMPLE = REPO / "tests" / "fixtures" / "sample-run"
HEADER = "https://json-schema.org/draft/2020-12/schema"

# audit-data file name -> schema file
MAPPING = {
    "audit.json": "audit.schema.json",
    "site-snapshot.json": "site-snapshot.schema.json",
    "goals.json": "goals.schema.json",
    "messaging.json": "dimension.schema.json",
    "conversion.json": "dimension.schema.json",
    "seo.json": "dimension.schema.json",
    "ux-technical.json": "dimension.schema.json",
    "design.json": "dimension.schema.json",
    "security.json": "dimension.schema.json",
    "action-report.json": "action-report.schema.json",
}

ANNOTATIONS = {"$schema", "title", "description", "$defs", "examples"}
VALIDATING = {"type", "properties", "required", "additionalProperties", "items", "prefixItems", "enum", "const",
              "minimum", "maximum", "minLength", "pattern", "minItems", "maxItems", "$ref", "anyOf", "oneOf"}


def load_schema(name):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def _type_ok(value, t):
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "null":
        return value is None
    raise AssertionError(f"unsupported type {t}")


def validate(value, schema, root=None, path="$"):
    """Errors (as 'path: message' strings) for value against schema; supports only VALIDATING keywords."""
    root = root or schema
    errs = []
    if "$ref" in schema:
        ref = schema["$ref"]
        assert ref.startswith("#/$defs/"), ref
        return validate(value, root["$defs"][ref[len("#/$defs/"):]], root, path)
    if "type" in schema and not _type_ok(value, schema["type"]):
        return [f"{path}: must be {schema['type']}"]
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{path}: must be one of {schema['enum']}")
    if "const" in schema and value != schema["const"]:
        errs.append(f"{path}: must be {schema['const']!r}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append(f"{path}: too short")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errs.append(f"{path}: does not match {schema['pattern']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append(f"{path}: below {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errs.append(f"{path}: above {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(f"{path}: needs at least {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(f"{path}: needs at most {schema['maxItems']} items")
        prefix = schema.get("prefixItems", [])
        for i, item in enumerate(value):
            if i < len(prefix):
                errs += validate(item, prefix[i], root, f"{path}[{i}]")
            elif "items" in schema:
                errs += validate(item, schema["items"], root, f"{path}[{i}]")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for k in schema.get("required", []):
            if k not in value:
                errs.append(f"{path}: missing required '{k}'")
        for k, v in value.items():
            if k in props:
                errs += validate(v, props[k], root, f"{path}.{k}")
            elif schema.get("additionalProperties") is False:
                errs.append(f"{path}: unknown property '{k}'")
    if "anyOf" in schema and not any(not validate(value, s, root, path) for s in schema["anyOf"]):
        errs.append(f"{path}: matches none of anyOf")
    if "oneOf" in schema and sum(not validate(value, s, root, path) for s in schema["oneOf"]) != 1:
        errs.append(f"{path}: must match exactly one of oneOf")
    return errs


def keywords(node, in_properties=False):
    """Every schema keyword used in a schema tree (property and $defs names are not keywords)."""
    found = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if not in_properties:
                found.add(k)
            if k in ("properties", "$defs"):
                for sub in v.values():
                    found |= keywords(sub)
            elif k in ("items", "additionalProperties"):
                found |= keywords(v)
            elif k in ("prefixItems", "anyOf", "oneOf"):
                for sub in v:
                    found |= keywords(sub)
    return found


def check(name, doc):
    return validate(doc, load_schema(MAPPING[name]))


def read_sample(name):
    return json.loads((SAMPLE / "audit-data" / name).read_text(encoding="utf-8"))


class SchemaTests(unittest.TestCase):
    def test_every_keyword_is_supported(self):
        for path in sorted(SCHEMAS.glob("*.schema.json")):
            used = keywords(json.loads(path.read_text(encoding="utf-8")))
            self.assertEqual(sorted(used - VALIDATING - ANNOTATIONS), [], path.name)

    def test_schemas_are_valid_json_with_header(self):
        files = sorted(SCHEMAS.glob("*.schema.json"))
        self.assertEqual({p.name for p in files}, set(MAPPING.values()))
        for p in files:
            s = json.loads(p.read_text(encoding="utf-8"))
            self.assertEqual(s.get("$schema"), HEADER, p.name)
            self.assertTrue(s.get("title"), p.name)
            self.assertTrue(s.get("description"), p.name)
            self.assertNotIn("$id", s, p.name)

    def test_validator_catches_basic_mistakes(self):
        s = load_schema("action-report.schema.json")
        doc = {"strengths": ["x"], "benchmarks": [{"standard": "s", "status": "met", "note": "n"}]}
        self.assertEqual(validate(doc, s), [])
        doc["benchmarks"][0]["status"] = "maybe"
        doc["extra"] = 1
        self.assertEqual(len(validate(doc, s)), 2)

    def test_mapping_covers_every_file(self):
        on_disk = {p.name for p in (SAMPLE / "audit-data").glob("*.json")} | {"security.json"}
        self.assertEqual(on_disk, set(MAPPING))

    def test_sample_run_validates(self):
        for p in sorted((SAMPLE / "audit-data").glob("*.json")):
            self.assertEqual(check(p.name, read_sample(p.name)), [], p.name)

    def test_required_matches_loader(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        run = pathlib.Path(tmp.name) / "run"
        for name, schema_name in MAPPING.items():
            if name == "security.json":
                continue
            schema = load_schema(schema_name)
            targets = [(schema, lambda d: d, "")]
            if schema_name == "dimension.schema.json":
                targets.append((schema["$defs"]["finding"], lambda d: d["findings"][0], "finding "))
            for sub, pick, label in targets:
                for field in sub["required"]:
                    with self.subTest(file=name, field=label + field):
                        shutil.rmtree(run, ignore_errors=True)
                        shutil.copytree(SAMPLE, run)
                        doc = read_sample(name)
                        self.assertTrue(pick(doc), "sample has no such object")
                        del pick(doc)[field]
                        (run / "audit-data" / name).write_text(json.dumps(doc), encoding="utf-8")
                        self.assertTrue(check(name, doc), "schema accepted the file")
                        with self.assertRaises(DataError):
                            load_run(run)

    def test_loader_and_schema_agree_on_value_rules(self):
        """Spot checks that a few rejected values are rejected by both."""
        cases = [
            ("seo.json", lambda d: d["findings"][0].update(impact=6)),
            ("seo.json", lambda d: d["findings"][0].update(key="Bad Key")),
            ("seo.json", lambda d: d["rubric"][0].update(result="Maybe")),
            ("seo.json", lambda d: d.update(typo=1)),
            ("audit.json", lambda d: d.update(mode="sideways")),
            ("audit.json", lambda d: d.update(date="20261106")),
            ("action-report.json", lambda d: d["benchmarks"][0].update(status="maybe")),
            ("goals.json", lambda d: d["brief"].append(["only one"])),
        ]
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        run = pathlib.Path(tmp.name) / "run"
        for name, mutate in cases:
            shutil.rmtree(run, ignore_errors=True)
            shutil.copytree(SAMPLE, run)
            doc = copy.deepcopy(read_sample(name))
            mutate(doc)
            (run / "audit-data" / name).write_text(json.dumps(doc), encoding="utf-8")
            with self.subTest(file=name):
                self.assertTrue(check(name, doc))
                with self.assertRaises(DataError):
                    load_run(run)


class SecuritySchemaTests(ServerCase):
    def test_generated_security_json_validates(self):
        code, _, err = self.scan()
        self.assertEqual(code, 0, err)
        self.assertEqual(check("security.json", self.page()), [])
        # a partial first draft without the optional blocks is still valid
        slim = {k: v for k, v in self.page().items() if k in ("verdict", "rubric", "findings", "strengths")}
        self.assertEqual(check("security.json", slim), [])


if __name__ == "__main__":
    unittest.main()
