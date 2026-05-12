<h1 align="center">cavekit</h1>

<p align="center">
  <strong>compressed spec-driven development for claude code and codex</strong><br/>
  <sub>one file · three commands · zero sub-agents</sub>
</p>

---

## what this is

Plan-then-execute forgets. SDD remembers — but most SDD frameworks bury
that value under agent swarms, dashboards, and ceremony that costs more
tokens than it saves.

Cavekit 4 is a rewrite from the ground up. It keeps only what earns its
place:

- **durable spec** — `SPEC.md` at repo root survives context resets.
- **caveman encoding** — ~75% fewer tokens than prose. Symbols, fragments,
  pipe tables for repeating records.
- **backprop reflex** — every test failure becomes a `§B` entry; classes
  of bug become `§V` invariants the spec never forgets.

That's the whole pitch.

## commands

| cmd | job |
|---|---|
| `/ck:spec` | create / amend / backprop `SPEC.md`. Sole mutator. |
| `/ck:build` | native plan → execute against spec. Auto-backprops on failure. |
| `/ck:check` | read-only drift report. Lists §V / §I / §T violations. |

## install

### Claude Code

One line, via the `skills` CLI:

```bash
npx skills add ryanshepps/cavekit
```

Installs five skills into `~/.claude/skills/`: `spec`, `build`, `check`
(the workflow) plus `caveman` and `backprop` (the utilities). Claude
activates each when its trigger context matches — e.g. "write a spec
for…" invokes `spec`, "build the next task" invokes `build`. Claude Code
picks them up on next launch.

Or via the Claude Code marketplace (also adds `/ck:spec`, `/ck:build`,
`/ck:check` slash commands):

```bash
/plugin marketplace add ryanshepps/cavekit
/plugin install ck@cavekit
```

Or clone directly:

```bash
git clone https://github.com/ryanshepps/cavekit.git ~/.claude/plugins/cavekit
```

The Claude Code interface stays the same: `/ck:spec`, `/ck:build`,
`/ck:check`.

### Codex

This fork also ships a Codex plugin package at `plugins/ck/` and marketplace
metadata at `.agents/plugins/marketplace.json`, following the same dual-plugin
layout as `JuliusBrussee/caveman`.

Add the repository as a Codex plugin marketplace source:

```bash
github:ryanshepps/cavekit
```

The Codex plugin exposes the same workflows as skills:

| prompt | workflow |
|---|---|
| `/ck:spec` or `use Cavekit spec` | create / amend / backprop `SPEC.md` |
| `/ck:build` or `use Cavekit build` | implement against `SPEC.md` |
| `/ck:check` or `use Cavekit check` | read-only drift report |
| `use Cavekit caveman` | compact Cavekit spec encoding |
| `use Cavekit backprop` | bug → spec protocol |

## format

See [`FORMAT.md`](./FORMAT.md). Fixed sections: §G goal, §C constraints,
§I interfaces, §V invariants, §T tasks (pipe table), §B bugs (pipe table).

## files

```
FORMAT.md             spec schema + caveman encoding rules
commands/             three slash-command entry points (/ck:spec, /ck:build, /ck:check)
skills/spec           spec mutator (mirrors commands/spec.md as a skill)
skills/build          plan-execute skill (mirrors commands/build.md)
skills/check          drift report skill (mirrors commands/check.md)
skills/caveman        encoding utility
skills/backprop       bug → spec protocol (six steps)
plugins/ck            Codex plugin package (synced from root sources)
.agents/plugins       Codex marketplace metadata
scripts/              sync helper for Codex plugin copies
tests/                local repo verification
```

## non-goals

- no sub-agents. Main Claude does the work.
- no dashboards. `cat SPEC.md` is the dashboard.
- no parallel workers. One thread, one spec, one diff.
- no JSON / YAML spec bodies. Markdown + pipe tables.
- no hooks, no orchestration binaries, no TypeScript helpers.

---

## older cavekit (the Hunt lifecycle, v3.1.0 and earlier)

The previous generation is **not deprecated** — it is frozen at tag
[`v3.1.0`](https://github.com/juliusbrussee/cavekit/tree/v3.1.0) and
remains a fully working plugin.

**What it is**:

> Spec-driven AI development with an autonomous execution loop. Four-command
> Hunt lifecycle (`/ck:sketch` → `/ck:map` → `/ck:make` → `/ck:check`),
> plus `/ck:ship`, `/ck:review`, `/ck:revise`, `/ck:status`, `/ck:design`,
> `/ck:research`, `/ck:init`, `/ck:config`, `/ck:resume`, `/ck:help` — 16
> slash commands total. 12 named sub-agents. Per-task token budgets,
> stop-hook state machine, model-tier routing, auto-backpropagation from
> test failures, tool-result caching, Codex peer review, Karpathy
> behavioral guardrails, caveman token compression, knowledge-graph
> integration, and design-system enforcement. Parallel wave execution and
> team mode.

**Pick v3.1.0** if you want the full autonomous loop, parallel agents,
peer review, or design-system workflow. **Pick v4** if you want the
distilled core — one spec, three commands, no orchestration.

### install the older version

Marketplace:

```bash
/plugin marketplace add juliusbrussee/cavekit@v3.1.0
/plugin install ck@cavekit
```

Git:

```bash
git clone -b v3.1.0 https://github.com/juliusbrussee/cavekit.git
```

Full docs live at the tag — `git checkout v3.1.0` and read the README
there for command reference, skill catalog, and the Hunt lifecycle guide.

### choosing, or moving

See [`UPGRADE.md`](./UPGRADE.md). Honest framing:
- Stay on v3.1.0 if your project has active `context/kits/` investment.
- Move to v4 if you want fewer moving parts and smaller token bills.
- It is a **two-way door** — `SPEC.md` is plain markdown; nothing traps
  you in either direction.

## philosophy

> The spec is the only artifact that earns its tokens. Everything else
> that costs tokens must either save more tokens later, or the user's
> attention, or it gets cut.

See [`CHANGELOG.md`](./CHANGELOG.md) for the full v3 → v4 break.

## license

MIT.
