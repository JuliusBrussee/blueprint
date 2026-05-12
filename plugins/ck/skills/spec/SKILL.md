---
name: spec
description: |
  Create, amend, or backprop bugs into SPEC.md at repo root. Sole mutator
  of the project spec. Triggers when the user asks to write a spec, start
  a new spec, distill a spec from existing code, add invariants, amend
  sections (§G, §C, §I, §V, §T, §B), or record a bug via backprop.
  Codex triggers: `/ck:spec`, `ck spec`, `use Cavekit spec`, and prompts that ask to create, amend, distill, or backprop a SPEC.md.
  Common phrasings: "write the spec for...", "new spec", "bug: ...",
  "amend §V.3", "distill spec from code", "spec this idea". Reads and
  follows FORMAT.md for the caveman encoding rules and pipe-table shape
  of §T and §B.
---

# spec — spec mutator

Read `FORMAT.md` at repo root if not already loaded. Caveman skill applies to all writes here.

## DISPATCH

Inspect user request and project state:

1. No `SPEC.md` at repo root AND args describe idea → **NEW**
2. No `SPEC.md` AND `from-code` in args → **DISTILL**
3. `SPEC.md` exists AND args start `bug:` → **BACKPROP**
4. `SPEC.md` exists AND args start `amend` → **AMEND**
5. `SPEC.md` exists, no args → ask user which mode

## NEW — idea → spec

Input: user idea.

Steps:
1. Extract goal (1 line, caveman). → §G.
2. List constraints user stated or implied. → §C.
3. List external surfaces user named. → §I.
4. Propose initial invariants. → §V (numbered V1…).
5. Break goal into ordered tasks. → §T pipe table, all status `.`, ids T1…
6. §B section with header row only (`id|date|cause|fix`).

Write to `SPEC.md`. Show user full file. Ask: "spec OK? suggest edits or invoke build."

## DISTILL — code → spec

Walk repo. Produce §G (infer from README/package.json/main entry), §C (infer from stack), §I (enumerate public APIs/CLIs/configs), §V (derive from tests and assertions), §T (one task per known TODO or missing test), §B (empty).

Caveman everywhere. Flag uncertain items with `?` in text so user can confirm.

## BACKPROP — bug → §B + §V

Input: `bug: <description>`.

Steps:
1. Parse bug description.
2. Find root cause (read relevant code).
3. Decide: would a new invariant catch recurrence? If yes → draft `V<next>`.
4. Append §B row: `B<next>|<date>|<cause>|V<N>`.
5. Append new invariant to §V.
6. If fix also changes behavior → add/update §T rows.
7. Show diff. Apply only on user OK.

Rule: every bug gets a §B entry. Invariant optional but preferred.

## AMEND — targeted edit

Input: `amend §V.3` or `amend §T` etc.

Read that section. Show current. Ask user what changes. Write. Show diff.

Never silently rewrite sections user did not name.

## OUTPUT RULES

- Caveman format per `FORMAT.md`.
- Preserve identifiers, paths, code verbatim.
- Numbering monotonic — never reuse §V.N or §B.N.
- §T row `cites` column ! list §V/§I deps: `T5|.|impl auth mw|V2,I.api`.

## NON-GOALS

- No sub-agents. Main thread writes.
- No dashboards, no logs, no state files beyond SPEC.md itself.
- No auto-build after spec. User invokes build explicitly.
