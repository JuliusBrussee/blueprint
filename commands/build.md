---
description: Plan-then-execute against SPEC.md. Native Claude Code loop, no sub-agents.
argument-hint: "[§T.n | --all | --next]"
---

Invoke the **build** skill (`skills/build/SKILL.md`). Treat `$ARGUMENTS` as the
target (`§T.n`, `--next`, or `--all`). Plan in native plan mode, name the exact
test that proves each §V touched (verification contract), read §R for external
facts, execute, and auto-invoke backprop on failure. High blast radius? Suggest
`/ck:review` first. Build only flips §T status; other spec edits route through spec.
