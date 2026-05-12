#!/usr/bin/env python3
"""Local verification runner for Cavekit install surfaces."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CheckFailure(RuntimeError):
    pass


def section(title: str) -> None:
    print(f"\n== {title} ==")


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def run(args: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    result = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise CheckFailure(
            f"Command failed ({result.returncode}): {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_synced_files() -> None:
    section("Synced Files")

    result = run([sys.executable, "scripts/sync-codex-plugin.py", "--check"], check=False)
    if result.returncode != 0:
        raise CheckFailure(
            "Codex plugin mirror is out of sync\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    for skill in ["backprop", "build", "caveman", "check", "spec"]:
        ensure(
            (ROOT / "plugins" / "ck" / "skills" / skill / "SKILL.md").exists(),
            f"Codex plugin skill copy missing: {skill}",
        )

    ensure(
        (ROOT / "plugins/ck/FORMAT.md").exists(),
        "Codex plugin FORMAT.md copy missing",
    )

    print("Codex skill and FORMAT.md mirrors OK")


def verify_manifests() -> None:
    section("Manifests")

    claude_plugin = read_json(ROOT / ".claude-plugin/plugin.json")
    claude_marketplace = read_json(ROOT / ".claude-plugin/marketplace.json")
    codex_plugin = read_json(ROOT / "plugins/ck/.codex-plugin/plugin.json")
    codex_marketplace = read_json(ROOT / ".agents/plugins/marketplace.json")

    ensure(isinstance(claude_plugin, dict), "Claude plugin manifest must be an object")
    ensure(isinstance(claude_marketplace, dict), "Claude marketplace manifest must be an object")
    ensure(isinstance(codex_plugin, dict), "Codex plugin manifest must be an object")
    ensure(isinstance(codex_marketplace, dict), "Codex marketplace manifest must be an object")

    ensure(claude_plugin["name"] == "ck", "Claude plugin name must remain ck")
    ensure(codex_plugin["name"] == "ck", "Codex plugin name must be ck")
    ensure(codex_plugin["skills"] == "./skills/", "Codex plugin skills path must be ./skills/")

    ensure(codex_marketplace["name"] == "cavekit", "Codex marketplace name must be cavekit")
    ensure(
        codex_marketplace["interface"]["displayName"] == "Cavekit",
        "Codex marketplace display name must be Cavekit",
    )

    plugins = codex_marketplace["plugins"]
    ensure(len(plugins) == 1, "Codex marketplace must expose exactly one plugin")
    plugin = plugins[0]
    ensure(plugin["name"] == "ck", "Codex marketplace plugin name must be ck")
    ensure(
        plugin["source"] == {"source": "local", "path": "./plugins/ck"},
        "Codex marketplace source must point to ./plugins/ck",
    )
    ensure(
        plugin["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "Codex marketplace policy must be AVAILABLE/ON_INSTALL",
    )
    ensure(plugin["category"] == "Coding", "Codex marketplace category must be Coding")

    print("Claude and Codex manifests OK")


def verify_codex_trigger_text() -> None:
    section("Codex Trigger Text")

    expected = {
        "spec": "/ck:spec",
        "build": "/ck:build",
        "check": "/ck:check",
    }
    for skill, trigger in expected.items():
        text = (ROOT / "plugins" / "ck" / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        ensure("Codex triggers:" in text, f"{skill} skill missing Codex trigger line")
        ensure(trigger in text, f"{skill} skill missing {trigger} trigger")
        ensure(f"use Cavekit {skill}" in text, f"{skill} skill missing natural-language Cavekit trigger")

    print("Codex slash and natural-language triggers OK")


def main() -> int:
    checks = [
        verify_synced_files,
        verify_manifests,
        verify_codex_trigger_text,
    ]

    try:
        for check in checks:
            check()
    except CheckFailure as exc:
        print(f"\nFAIL: {exc}", file=sys.stderr)
        return 1

    print("\nAll local verification checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
