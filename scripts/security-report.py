#!/usr/bin/env python3
"""Re-render security.md from an edited audit-data/security.json.

    python scripts/security-report.py RUN_DIR

Exit codes: 0 success, 2 usage error or invalid data (one message per line on stderr).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from security.text import render_text  # noqa: E402

USAGE = "usage: security-report.py <RUN_DIR>"


def main(argv):
    if len(argv) != 1 or argv[0].startswith("-"):
        print(USAGE)
        return 2
    run = Path(argv[0])
    docs = {}
    for label, path in (("audit-data/security.json", run / "audit-data" / "security.json"),
                        ("security-scan.json", run / "security-scan.json")):
        try:
            docs[label] = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            hint = "; run security-scan.py first" if label == "security-scan.json" else ""
            print("%s is missing%s" % (label, hint), file=sys.stderr)
            return 2
        except (OSError, ValueError) as exc:
            print("%s could not be read: %s" % (label, exc), file=sys.stderr)
            return 2
        if not isinstance(docs[label], dict):
            print("%s must be a JSON object" % label, file=sys.stderr)
            return 2
    page, scan = docs["audit-data/security.json"], docs["security-scan.json"]
    for key in ("url", "date"):
        if not isinstance(scan.get(key), str):
            print("security-scan.json has no '%s'" % key, file=sys.stderr)
            return 2
    try:
        text = render_text(page, scan["url"], scan["date"])
    except ValueError as exc:
        for msg in str(exc).split("; "):
            print(msg, file=sys.stderr)
        return 2
    except (KeyError, TypeError, AttributeError) as exc:
        print("audit-data/security.json is incomplete (%s: %s)" % (type(exc).__name__, exc), file=sys.stderr)
        return 2
    target = run / "security.md"
    target.write_text(text, encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):   # a path a cp1252 console can't show is escaped, not a crash
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    sys.exit(main(sys.argv[1:]))
