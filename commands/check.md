---
description: Drift detector. Diff SPEC.md against code. Read-only, zero writes.
argument-hint: "[§V | §I | §T | --all]"
---

Invoke the **check** skill (`skills/check/SKILL.md`). Treat `$ARGUMENTS` as the
scope (`§V` default, `§I`, `§T`, or `--all`). Read-only — classify each item
HOLD/VIOLATE/UNVERIFIABLE (or MATCH/DRIFT/MISSING/EXTRA for §I), cite file:line
evidence, end with remedy hints. Writes nothing. Run it after each build.
