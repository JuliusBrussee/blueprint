---
name: check
description: |
  Read-only drift detector. Diffs SPEC.md against current code and reports
  violations grouped by severity. Writes nothing — suggests remedies via
  the spec or build skills but never invokes them. Triggers when the user
  asks to check drift, audit the spec, verify invariants, or ask whether
  code still matches the spec. Phrasings: "check drift", "audit the spec",
  "does the code still match §V", "check invariants", "spec vs code".
  Codex triggers: `/ck:check`, `ck check`, `use Cavekit check`, and prompts that ask to audit drift, check invariants, or compare SPEC.md to code.
---

# check — drift report

Pure diagnostic. Reports violations. Writes nothing. User decides remedy.

## LOAD

1. Read `SPEC.md`. If missing → "no spec, nothing to check." Stop.
2. Parse invocation args:
   - `§V` → check invariants only (default)
   - `§I` → check interfaces
   - `§T` → audit task status vs code
   - `--all` → all three

## CHECK §V — invariants

For each V<n>:

1. Translate invariant into verifiable claim about code.
2. Grep / read relevant files.
3. Classify: **HOLD** / **VIOLATE** / **UNVERIFIABLE**.
4. Record address + file:line evidence.

## CHECK §I — interfaces

For each I item:

1. Locate implementation.
2. Classify:
   - **MATCH** — shape in code = shape in spec.
   - **DRIFT** — impl exists, shape differs.
   - **MISSING** — impl absent.
   - **EXTRA** — code exposes surface not in §I.

## CHECK §T — tasks

For each T<n>:

1. If `x`: verify claimed work present.
2. If `~`: note as in-progress.
3. If `.`: note as pending.
4. Flag `x` rows with no evidence as **STALE**.

## REPORT

Caveman. Grouped by severity.

```
## §V drift
V2 VIOLATE: auth/mw.go:47 uses `<` not `≤`. see §B.1.
V5 UNVERIFIABLE: no test covers ∀ req path.

## §I drift
I.api DRIFT: POST /x returns `{result}` not `{id}`. route.go:112.
I.cmd MISSING: `foo bar` absent from cli/*.go.

## §T drift
T3 STALE: status `x`, no middleware file exists.

## summary
2 violate. 1 missing. 1 stale. 1 unverifiable.
next: spec skill with `bug:` or fix code at cited lines.
```

## REMEDY HINTS (not actions)

End report with one-line hint per class:
- VIOLATE / DRIFT → invoke spec skill `bug: <V.n>` or fix code.
- MISSING → invoke build skill on `§T.n` if task exists; else spec skill `amend §T`.
- STALE → spec skill `amend §T` to uncheck.
- EXTRA → spec skill `amend §I` to document, or delete code.

Never invoke fixes. Report only.

## NON-GOALS

- Zero writes. No SPEC.md edits. No code edits.
- No sub-agents. Main thread reads.
- No scores, no grades. Binary per item: holds or drifts.
