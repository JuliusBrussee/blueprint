---
name: archive
description: |
  Archive old SPEC.md content when file exceeds 500 lines. Copies full SPEC.md
  to .cavekit/archive/ then trims completed tasks, old bugs, and unreferenced
  invariants/interfaces. Nothing lost — archive is exact copy. Triggers when
  user says "archive spec", "trim spec", "spec too long", or invokes /archive.
---

# archive — compact SPEC.md

When SPEC.md > 500 lines. Full copy to archive. Trim working copy.

## PRECHECK

1. Read `SPEC.md`. If missing → "no spec, nothing to archive." Stop.
2. Count lines. If < 500 → "SPEC.md is <N> lines. Nothing to archive." Stop.
3. Read `FORMAT.md` if not loaded.

## RESEARCH — dry-run (no writes)

Analyze SPEC.md. Identify what would be archived. Show preview. No files touched.

Steps:

1. Count total lines → `lines before`.
2. §T: count rows with status `x`. List their IDs. Count their lines.
3. §B: count rows with age ≥ 90 days (date < today-90d). List their IDs. Count their lines.
4. §V: collect `cites` from active §T (`.` or `~`). Find V<n> not in live set. List them. Count their lines.
5. §I: same logic as §V. List unreferenced I items. Count their lines.
6. §C: same logic. Count their lines.
7. `lines after` = `lines before` - (§T lines + §B lines + §V lines + §I lines + §C lines) + (archive comment lines: 1 per trimmed section). Exact count.

Show preview:

```
## archive preview

§T would archive: T1, T3-T8, T12 (9 tasks completed)
§B would archive: B1-B4 (4 bugs older than 90 days)
§V would archive: V1,V3-V5 (4 invariants, no active task cites them)
§I would archive: I.cli (1 interface, no active task cites it)
§C would archive: 2 constraints, no active task cites them
§G untouched

lines before: 533
lines after: 100

Proceed? (yes / no / amend)
```

If user says **yes** → continue to ARCHIVE + TRIM.
If user says **no** → stop. Nothing written.
If user says **amend** → user specifies what to exclude/include, re-run RESEARCH.

## ARCHIVE

1. Create `.cavekit/archive/` dir if absent.
2. Copy **full** SPEC.md → `.cavekit/archive/SPEC-<YYYY-MM-DD>.md`. Exact copy, no changes.
3. If `.cavekit/archive/SPEC-<today>.md` already exists → append `-2`, `-3`, etc.

## TRIM

In working SPEC.md only. Archive untouched.

### §T — completed tasks

1. Find all rows with status `x`.
2. Record id range (e.g. `T1-T12`).
3. Remove those rows from table.
4. Insert HTML comment above §T table header:

```
<!-- archive: .cavekit/archive/SPEC-<date>.md §T T1-T12 -->
```

### §B — old bugs

1. Find all rows where age ≥ 90 days (date < today-90d).
2. Record id range (e.g. `B1-B5`).
3. Remove those rows from table.
4. Insert HTML comment above §B table header:

```
<!-- archive: .cavekit/archive/SPEC-<date>.md §B B1-B5 -->
```

### §V — unreferenced invariants

1. Collect all `cites` values from **active** §T rows (status `.` or `~`). Extract every V<n> reference.
2. This is the **live set** — invariants still actively enforced by pending work.
3. For each V<n> NOT in live set → candidate for archive.
4. Remove those invariant lines from §V.
5. Insert HTML comment above §V section:

```
<!-- archive: .cavekit/archive/SPEC-<date>.md §V V1,V3-V5 -->
```

### §I — unreferenced interfaces

1. Same logic as §V: collect all `I.*` references from active §T rows.
2. For each I item NOT in live set → candidate for archive.
3. Remove those interface lines from §I.
4. Insert HTML comment above §I section:

```
<!-- archive: .cavekit/archive/SPEC-<date>.md §I I.api,I.cli -->
```

### §C — unreferenced constraints

1. Same logic as §V: collect all §C references from active §T rows.
2. For each §C item NOT in live set → candidate for archive.
3. Remove those constraint lines from §C.
4. Insert HTML comment above §C section:

```
<!-- archive: .cavekit/archive/SPEC-<date>.md §C -->
```

### §G — never touched. Project identity.

## REPORT

Show diff of SPEC.md (before → after). Format:

```
## archive report

saved to: .cavekit/archive/SPEC-2026-05-15.md

§T archived: T1, T3-T8, T12 (9 tasks completed)
§B archived: B1-B4 (4 bugs older than 90 days)
§V archived: V1,V3-V5 (4 invariants, no active task cites them)
§I archived: I.cli (1 interface, no active task cites it)
§C archived: 2 constraints, no active task cites them
§G untouched

lines before: 542
lines after: 218
```

Apply only on user OK.

## RULES

- Archive = full copy. Nothing lost. Ever.
- `check` and `build` read `.cavekit/archive/` when they need historical context.
- One archive file per run. Multiple runs = multiple files. Oldest = furthest history.
- §G is sacred. Never remove.
- §C, §V and §I archived only when no active §T (`.` or `~`) cites them.
- After archive, spec and build skills parse archive comments for max ID.
  New tasks continue T13+ if T1-T12 archived. Never reuse IDs.
- New tasks may cite archived V/N or I/X — archive comment points to full text.
