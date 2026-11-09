"""Packaging checks: the frozen Claude app copy, the plugin manifests, shared scripts, links and docs."""
import json
import pathlib
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from helpers import REPO, frozen_skill_dirs, git_show, has_commit, skill_dirs  # noqa: E402

FROZEN_REV = "7ecf3dc"
HANDBOOK = "Website Audit Suite - Handbook by Ananas Agency.md"
# The two checks against the frozen commit need the git history; a ZIP download has none.
needs_history = unittest.skipUnless(has_commit(FROZEN_REV), f"commit {FROZEN_REV} is not in this checkout")


class FrozenAppTest(unittest.TestCase):
    @needs_history
    def test_skill_files_match_commit(self):
        for numbered, skill in frozen_skill_dirs():
            old = f"{numbered.name}/{skill.name}.skill"
            self.assertEqual((REPO / "claude-app" / f"{skill.name}.skill").read_bytes(), git_show(FROZEN_REV, old))

    @needs_history
    def test_handbook_matches_commit(self):
        local = (REPO / "claude-app" / HANDBOOK).read_bytes().replace(b"\r\n", b"\n")  # text=auto checks out CRLF on Windows
        self.assertEqual(local, git_show(FROZEN_REV, HANDBOOK))

    def test_no_skill_archives_outside_claude_app(self):
        stray = [p for p in REPO.rglob("*.skill") if "claude-app" not in p.parts and ".git" not in p.parts]
        self.assertEqual(stray, [])

    def test_retired_scripts_removed(self):
        for n in ("repack-all-skills.py", "build-handbook.py"):
            self.assertFalse((REPO / "scripts" / n).exists(), n)


def read_json(rel: str) -> dict:
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


class PluginManifestTest(unittest.TestCase):
    def test_plugin_json_values(self):
        m = read_json(".claude-plugin/plugin.json")
        self.assertEqual((m["name"], m["version"], m["license"]), ("website-audit-suite", "1.1.0", "MIT"))
        self.assertEqual(m["repository"], "https://github.com/ananas-agency/Website-Audit-Suite")

    def test_skills_paths_cover_every_skill(self):
        m = read_json(".claude-plugin/plugin.json")
        self.assertEqual(m["skills"], [f"./{n.name}/" for n, _ in skill_dirs()])
        for _, skill in skill_dirs():
            front = (skill / "SKILL.md").read_text(encoding="utf-8").split("---")[1]
            self.assertIn(f"name: {skill.name}", front)

    def test_marketplace_json_values(self):
        mk = read_json(".claude-plugin/marketplace.json")
        self.assertEqual(mk["name"], "ananas-agency")
        self.assertEqual([(p["name"], p["source"]) for p in mk["plugins"]], [("website-audit-suite", "./")])
        self.assertNotIn("version", mk["plugins"][0])  # plugin.json owns the version


SCRIPT_REF = re.compile(r"scripts/([a-z0-9-]+\.py)")


def skill_text(skill: pathlib.Path) -> str:
    """SKILL.md plus every references/*.md of one skill."""
    files = [skill / "SKILL.md", *sorted((skill / "references").glob("*.md"))]
    return "\n".join(p.read_text(encoding="utf-8") for p in files)


class ScriptPathsTest(unittest.TestCase):
    def test_no_script_copies_inside_skills(self):
        self.assertEqual([s for _, s in skill_dirs() if (s / "scripts").exists()], [])

    def test_every_mentioned_script_exists(self):
        for _, s in skill_dirs():
            for name in SCRIPT_REF.findall(skill_text(s)):
                self.assertTrue((REPO / "scripts" / name).is_file(), f"{s.name}: scripts/{name}")

    def test_skills_that_use_scripts_name_the_plugin_root(self):
        for _, s in skill_dirs():
            if SCRIPT_REF.search(skill_text(s)):
                self.assertIn("${CLAUDE_PLUGIN_ROOT}/scripts/", (s / "SKILL.md").read_text(encoding="utf-8"), s.name)

    def test_skill_commands_quote_plugin_root(self):
        for _, s in skill_dirs():
            body = (s / "SKILL.md").read_text(encoding="utf-8")
            # assertIsNone keeps a failure message short (assertNotRegex would print the whole file)
            self.assertIsNone(re.search(r"(?m)^\s*python3? scripts/", body), s.name)
            self.assertIsNone(re.search(r"python3? \$\{CLAUDE_PLUGIN_ROOT\}", body), f"{s.name}: unquoted root")


def markdown_links(path: pathlib.Path) -> list:
    """Relative link targets in a Markdown file, ignoring code (fences and inline spans hold report templates)."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return [t for t in re.findall(r"\]\(([^)\s]+)\)", text) if not re.match(r"(https?:|mailto:|#)", t)]


LINKED_FILES = sorted(
    {p for _, s in skill_dirs() for p in s.rglob("*.md")}
    | {REPO / n for n in ("report-format.md", "benchmarks-2026.md", "audit-data-format.md", "README.md", "CHANGELOG.md", "claude-app/README.md", "schemas/README.md")}
)


# Top-level folders that are git-ignored (local data and maintainer-only notes), so a public link into them breaks.
IGNORED_TOP = {"test-runs", "misc", "website", "docs", "dev", ".superpowers"}


def link_target(f: pathlib.Path, t: str) -> pathlib.Path:
    return (f.parent / unquote(t.split("#")[0])).resolve()


class LinksTest(unittest.TestCase):
    def test_relative_links_resolve(self):
        broken = [f"{f.relative_to(REPO)} -> {t}" for f in LINKED_FILES for t in markdown_links(f)
                  if not link_target(f, t).exists()]
        self.assertEqual(broken, [])

    def test_no_links_into_ignored_folders(self):
        bad = []
        for f in LINKED_FILES:
            for t in markdown_links(f):
                target = link_target(f, t)
                if not target.is_relative_to(REPO) or target.relative_to(REPO).parts[0] in IGNORED_TOP:
                    bad.append(f"{f.relative_to(REPO)} -> {t}")
        self.assertEqual(bad, [])


README = REPO / "README.md"


class GitIgnoreTest(unittest.TestCase):
    def test_no_tracked_file_is_ignored(self):
        # A rule that also matches a tracked file silently drops it from any fresh `git add -A`.
        out = subprocess.run(["git", "ls-files", "--cached", "--ignored", "--exclude-standard"], cwd=REPO,
                             capture_output=True, text=True)
        if out.returncode != 0:
            self.skipTest("not a git checkout")
        self.assertEqual(out.stdout.splitlines(), [])


class ReadmeTest(unittest.TestCase):
    def test_plugin_install_commands(self):
        r = README.read_text(encoding="utf-8")
        self.assertIn("/plugin marketplace add ananas-agency/Website-Audit-Suite", r)
        self.assertIn("/plugin install website-audit-suite@ananas-agency", r)

    def test_no_retired_tooling(self):
        r = README.read_text(encoding="utf-8")
        for s in ("repack-all-skills.py", "build-handbook.py"):
            self.assertNotIn(s, r)

    def test_old_install_migration_note(self):
        r = README.read_text(encoding="utf-8")
        para = next((p for p in r.split("\n\n") if "~/.claude/skills/" in p), "")
        self.assertRegex(para.lower(), r"delete|remove", "no note telling old installs to remove their copies")
        self.assertNotIn("Copy a skill's **unpacked folder**", r)  # the old copy-a-folder install is gone

    def test_release_needs_version_bump(self):
        # Claude Code keeps installed users on plugin.json's version until it changes.
        r = README.read_text(encoding="utf-8")
        self.assertIn("bump `version`", r)
        self.assertIn(".claude-plugin/plugin.json", r)


class SetupWiringTest(unittest.TestCase):
    def test_site_snapshot_runs_setup_check(self):
        body = (REPO / "0 Site Snapshot/site-snapshot/SKILL.md").read_text(encoding="utf-8")
        self.assertIn('"${CLAUDE_PLUGIN_ROOT}/scripts/setup-check.py"', body)
        self.assertNotIn("Quietly test whether a tool can run", body)

    def test_site_snapshot_handles_missing_mode_line(self):
        # No Python, Python 2, or a crash: the check prints no MODE line at all.
        body = (REPO / "0 Site Snapshot/site-snapshot/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("No `MODE:` line", body)
        self.assertIn("winget install", body)

    def test_scan_skills_run_setup_check(self):
        for rel in ("1 Goals Discovery/goals-discovery", "3 Conversion CRO/conversion-cro",
                    "5 UX Technical/ux-technical", "6 Design Visual/design-visual",
                    "8 Security/security"):
            self.assertIn("setup-check.py", (REPO / rel / "SKILL.md").read_text(encoding="utf-8"), rel)


if __name__ == "__main__":
    unittest.main()
