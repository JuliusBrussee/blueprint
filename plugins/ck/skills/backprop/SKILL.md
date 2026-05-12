---
name: backprop
description: |
  Bug → spec protocol. When a bug is found or a test fails, trace the cause,
  decide whether a new §V invariant would catch recurrence, append to §B.
  This is the one non-obvious thing SDD does that plan-then-execute doesn't.
  Triggers on test failure, bug report, post-mortem, or explicit user ask.
  Codex triggers: `use Cavekit backprop`, `backprop`, test failures, bug reports, and prompts that ask to turn a bug into SPEC.md memory.
---

# backprop — bug → spec

Plan-then-execute fixes the code & forgets.
SDD fixes the code AND edits spec so recurrence is impossible.
That edit is backprop.

## WHEN TO BACKPROP

- Test failed at `/build` verification.
- User reports bug.
- Post-mortem after production incident.
- `/check` flags VIOLATE with root cause found.

## SIX STEPS

### 1. TRACE
Read failure output / bug report.
Find exact file:line of wrong behavior.
Name root cause in one caveman sentence.

### 2. ANALYZE
Ask three questions:
- Would a new §V invariant catch this class of bug? (most common: yes)
- Is §I wrong — did spec claim shape the code cannot deliver? (sometimes)
- Is §T wrong — did we build the wrong thing? (rare but real)

### 3. PROPOSE
Draft the spec change. Never skip §B; §V/§I/§T are case-by-case.

Template:
```
§B row: B<next>|<date>|<root cause>|V<N>
§V line: V<next>: <testable rule that would have caught it>
```

Example:
```
§B row: B3|2026-04-20|refund job ran twice on retry|V7
§V line: V7: ∀ refund → idempotency key check before charge reversal
```

### 4. GENERATE TEST
New invariant without test = lie. Add failing test first.
Name test so it cites the invariant: `TestV7_RefundIdempotent`.

### 5. VERIFY
Fix code. Run test. Must pass. Run full suite. Must not regress.

### 6. LOG
Commit spec edit + test + code fix together.
Commit msg: `backprop §B.<n> + §V.<N>: <one-line cause>`.

## WHAT MAKES A GOOD INVARIANT

- Testable in code (grep-able or assert-able).
- Scoped to a behavior, not a file.
- Stated positively when possible (`! hold` over `⊥ forbid`).
- References §I surface where it applies.

**Bad**: V8: code should be correct.
**Good**: V8: ∀ pg_query ! params interpolated via driver, ⊥ string concat.

## WHEN NOT TO ADD §V

- Bug was purely mechanical typo with no class (`i++` vs `i--` in throwaway).
- Fix is a one-time migration.
- Root cause is external dep (upgrade deps instead, note in §C).

Still append §B entry — record that this failure mode was considered. Future bug with same smell → §B search shows precedent.

## OUTPUT SHAPE

Every backprop run produces:
1. §B entry (always).
2. §V entry (usually).
3. Test file (when §V added).
4. Code fix.
5. One commit.

No dashboards. No log files. SPEC.md + git is the full history.
