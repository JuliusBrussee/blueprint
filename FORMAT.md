# SPEC.md FORMAT

Single file. Project root. Every cavekit command reads it.

## SECTIONS

Fixed order. Fixed headers. Addressable.

```
# SPEC

## §G GOAL
one line. what code must do.

## §C CONSTRAINTS
- bullet. non-negotiable boundary.
- bullet. tech/lang/lib locked in.

## §I INTERFACES
external surface. what world sees.
- cmd: `foo bar` → stdout JSON
- api: POST /x → 200 {id}
- file: `config.yaml` schema …
- env: `FOO_KEY` required

## §V INVARIANTS
numbered. testable. each ! MUST hold.
V1: ∀ req → auth check before handler
V2: token expiry ≤ ⊥ allowed
V3: DB write ! in transaction

## §T TASKS
pipe table. ids monotonic (never reused). status: `x` done / `~` wip / `.` todo.
id|status|task|cites
T1|.|scaffold repo|-
T2|.|impl §I.api POST /x|V2
T3|x|add §V.1 middleware|V1,I.api

## §B BUGS
pipe table. backprop log. each row = bug + invariant that catches recurrence.
id|date|cause|fix
B1|2026-04-20|token `<` not `≤`|V2
B2|2026-04-21|race on write|V3
```

**Table cell rules**: literal `|` → escape as `\|`. Backticks OK. Cells trimmed. Empty = `-`.

## ADDRESSING

`§<S>.<n>` = section.item. `§V.2` = invariants section, item 2.
Commands, commits, PRs all reference by §. Zero ambiguity.

## CAVEMAN ENCODING

Default for every section. Rules:

- Drop articles (a, an, the). Drop filler.
- Drop aux verbs (is, are, was) where fragment works.
- Short synonyms (fix > implement).
- Fragments fine.

**Preserve verbatim**: code, paths, identifiers, URLs, numbers, error strings, SQL, regex.

**Symbols** (save tokens, machine-readable):

```
→   leads to / becomes / triggers
∴   therefore / fix
∀   for all / every
∃   exists / some
!   must
?   may / optional
⊥   never / impossible / forbidden
≠   not equal / differs from
∈   in / member of
∉   not in
≤   at most
≥   at least
&   and
|   or
```

**Bad** (v1 prose):

> The authentication middleware must verify the token expiry on every request before allowing the handler to execute.

**Good** (v2 caveman):

> V1: ∀ req → auth check before handler

**Bad** (prose bug note):

> Fixed a bug where token expiry comparison used strict less-than instead of less-than-or-equal, causing tokens to be rejected exactly at their expiry timestamp.

**Good** (v2 caveman):

> B1: token `<` not `<=` ∴ tokens rejected @ expiry. §V.2 now ! `≤`.

## WHY CAVEMAN FOR SPECS

Spec loaded every invocation. 75% fewer tokens = 75% fewer dollars & faster reads.
Human skims fast too. Symbols unambiguous.

## ONE FILE RULE

Big project → more sections, not more files. grep ceremony kills agent speed.
If SPEC.md > 500 lines, invoke `/archive`. Never split into multiple specs.

## ARCHIVE

When SPEC.md > 500 lines, `/archive` skill handles it:

1. Copy **full** SPEC.md → `.cavekit/archive/SPEC-<date>.md`. If `SPEC-<date>.md` already exists → append `-2`, `-3`, etc.
2. In working SPEC.md:
   - §T: remove rows with status `x`. Add comment above table: `<!-- archive: .cavekit/archive/SPEC-<date>.md §T T1-T12 -->`
   - §B: remove rows older than 90 days. Add comment above table: `<!-- archive: .cavekit/archive/SPEC-<date>.md §B B1-B5 -->`
   - §V: remove invariants NOT cited by any active §T (status `.` or `~`). Add comment: `<!-- archive: ... §V V1,V3-V5 -->`
   - §I: remove interfaces NOT cited by any active §T. Add comment: `<!-- archive: ... §I I.cli -->`
   - §C: remove constraints NOT cited by any active §T. Add comment: `<!-- archive: ... §C -->`
   - §G: never touched
3. Show diff. Apply only on user OK.

Archive dir: `.cavekit/archive/`. One file per run. Full copy = nothing lost.
`check` and `build` read archive when needed.

After archive, new IDs continue from max(current + archived). Never reuse.
Archive comments carry the range for ID lookup. New tasks may cite archived V/N or I/X.

## WRITES

| command | writes | section |
|---|---|---|
| `/spec new` | creates | all |
| `/spec amend` | edits | chosen |
| `/spec bug` | appends | §B + §V |
| `/archive` | archives + trims | §T done, §B old, §V/§I/§C unreferenced |
| `/build` | flips | §T status cell `.` → `~` → `x` |
| `/check` | — | read only |

That is whole format.
