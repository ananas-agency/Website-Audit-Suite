"""Shared helpers for the suite's tests (standard library only)."""
import importlib.util
import pathlib
import re
import subprocess
import types

REPO = pathlib.Path(__file__).resolve().parent.parent


def _skill_pairs(pattern: str) -> list:
    pairs = []
    for numbered in sorted(p for p in REPO.iterdir() if p.is_dir() and re.match(pattern, p.name)):
        skills = [d for d in numbered.iterdir() if d.is_dir() and (d / "SKILL.md").is_file()]
        if len(skills) != 1:
            raise AssertionError(f"{numbered.name}: expected one skill folder, found {len(skills)}")
        pairs.append((numbered, skills[0]))
    return pairs


def skill_dirs() -> list:
    """(numbered folder, skill folder) pairs for the nine skills, sorted by folder name."""
    return _skill_pairs(r"^[0-8] ")


def frozen_skill_dirs() -> list:
    """The first eight skills, the ones the frozen claude-app copy holds."""
    return _skill_pairs(r"^[0-7] ")


def load_script(relpath: str) -> types.ModuleType:
    """Import a script whose file name has hyphens, such as scripts/setup-check.py."""
    path = REPO / relpath
    name = re.sub(r"\W", "_", path.stem)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_show(rev: str, path: str) -> bytes:
    """The bytes git stores for `path` at commit `rev`."""
    return subprocess.run(["git", "show", f"{rev}:{path}"], cwd=REPO, capture_output=True, check=True).stdout


def has_commit(rev: str) -> bool:
    """True when this checkout's git history holds commit `rev`. A ZIP download has no history."""
    try:
        found = subprocess.run(["git", "cat-file", "-e", f"{rev}^{{commit}}"], cwd=REPO, capture_output=True)
    except OSError:  # git isn't installed
        return False
    return found.returncode == 0
