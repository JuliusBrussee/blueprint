#!/usr/bin/env python3
"""Sync Codex plugin assets from the root Cavekit sources."""

from __future__ import annotations

import argparse
import difflib
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "ck"

SKILLS = {
    "spec": [
        "Codex triggers: `/ck:spec`, `ck spec`, `use Cavekit spec`, and prompts that ask to create, amend, distill, or backprop a SPEC.md.",
    ],
    "build": [
        "Codex triggers: `/ck:build`, `ck build`, `use Cavekit build`, and prompts that ask to implement, execute, or build against SPEC.md.",
    ],
    "check": [
        "Codex triggers: `/ck:check`, `ck check`, `use Cavekit check`, and prompts that ask to audit drift, check invariants, or compare SPEC.md to code.",
    ],
    "caveman": [
        "Codex triggers: `use Cavekit caveman`, `caveman`, `compress this`, and spec-adjacent writes that need compact Cavekit encoding.",
    ],
    "backprop": [
        "Codex triggers: `use Cavekit backprop`, `backprop`, test failures, bug reports, and prompts that ask to turn a bug into SPEC.md memory.",
    ],
}


def add_codex_triggers(text: str, skill: str) -> str:
    insert = "\n".join(f"  {line}" for line in SKILLS[skill])
    marker = "  Common phrasings:"

    if f"Codex triggers:" in text:
        return text

    if marker in text:
        return text.replace(marker, f"{insert}\n{marker}", 1)

    needle = "---\n\n# "
    if needle not in text:
        raise ValueError(f"{skill}: could not find frontmatter boundary")
    return text.replace(needle, f"{insert}\n---\n\n# ", 1)


def expected_files() -> dict[Path, str]:
    files: dict[Path, str] = {
        PLUGIN / "FORMAT.md": (ROOT / "FORMAT.md").read_text(),
    }

    for skill in sorted(SKILLS):
        source = ROOT / "skills" / skill / "SKILL.md"
        files[PLUGIN / "skills" / skill / "SKILL.md"] = add_codex_triggers(
            source.read_text(),
            skill,
        )

    return files


def diff_text(path: Path, expected: str) -> str:
    actual = path.read_text() if path.exists() else ""
    return "".join(
        difflib.unified_diff(
            actual.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile=str(path),
            tofile=f"{path} (expected)",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated Codex plugin assets are out of sync",
    )
    args = parser.parse_args()

    expected = expected_files()
    stale = [(path, content) for path, content in expected.items() if not path.exists() or path.read_text() != content]

    if args.check:
        if not stale:
            return 0
        for path, content in stale:
            sys.stderr.write(diff_text(path, content))
        return 1

    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    # Remove copied skill folders that no longer exist at the root.
    skills_dir = PLUGIN / "skills"
    if skills_dir.exists():
        for child in skills_dir.iterdir():
            if child.is_dir() and child.name not in SKILLS:
                shutil.rmtree(child)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
