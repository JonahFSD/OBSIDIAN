---
description: The process spine — how an idea becomes verified code. Sequences [[Invariants]], [[Deterministic Gates]] and [[Writing Tests]] into a spec-driven loop: plan in Cowork, build in Claude Code, distill the lessons back here. The "how"; the atomic notes are the "what" and "why".
---
# Spec-Driven Build Loop

The harness, not the model, is the lever. The model is stochastic and you *want* it to be — that flexibility is its value inside a unit. So you make the **boundaries** deterministic instead: stochastic in the cell, deterministic at the membrane. Slop is unconstrained state space filled with plausible guesses; every stage here removes a degree of freedom until mostly-correct things are what's expressible. This note is the *process* — it sequences the enforcement in [[Deterministic Gates]], the why in [[Good Code in the AI Age]], and the rules in [[Invariants]].

Convergent with what mid-2026 calls **harness engineering** + **spec-driven development (SDD)**; the value is the discipline and the by-construction bias, not novelty (see Skeptic's corner).

## Operating principles (process-level — extend [[Invariants]])
- **Spec is the single source of intent; code is regenerable output.** The spec, not the chat, carries the contract. (SDD)
- **Prefer impossibility to detection.** By-construction beats checking: generate the seam, make illegal states unrepresentable, gate only what you couldn't eliminate. A check works only if it runs; an impossibility always holds.
- **The handoff is a git commit, not a conversation.** The plan crosses the Cowork→Claude Code boundary as spec + ordered units + skeleton + first commit in the repo — never as prose the next session reinterprets.
- **Done = green and shown, never asserted.** A passing gate run, pasted; not the agent's word. ([[Invariants]] #2, #9)
- **Scale-tier the process.** Most ideas are small; full ceremony on a throwaway is itself slop (the overhead trap). Pick a tier first.
- **The harness is model-disposable.** Every scaffold is a hypothesis about a model weakness with an expiry date; delete what a model upgrade made dead weight.
- **Floor from [[Invariants]]; growth from the Slop Register.** The universal invariants are the baseline gate; each new scar becomes a new rule (Stage 6).

## The loop at a glance

| # | Stage | Where | Input → Output | Gate to pass |
|---|-------|-------|----------------|--------------|
| 1 | Capture | Cowork / vault | idea → one falsifiable line | can you name a criterion that would make it *wrong*? |
| 2 | Specify | Cowork | idea → spec (contracts + acceptance criteria) | every requirement maps to an observable pass/fail |
| 3 | Decompose | Cowork | spec → ordered units + failing tests + first commit | repo is red, skeletoned, committed |
| 4 | Build-to-green | Claude Code | one unit → passing unit | fast gate green; oracle test unweakened |
| 5 | Gate | Claude Code + CI | diff → mergeable diff | full `gate` green + security review |
| 6 | Distill | vault | what you learned → a rule | the lesson is executable, not prose |

Cowork owns 1–3 (plan + initialize). Claude Code owns 4–5 (build + verify). The vault owns 6 (durable memory). The boundary between Cowork and Claude Code is the **first commit**, nothing softer.

## Stage 1 — Capture
An idea note in the vault, then a falsifiability triage: if you can't state one criterion whose failure would make the idea *wrong*, it isn't ready to build — it's a prototype. Prototype freely with no harness; promote to Stage 2 only once "correct" is nameable. This is the cheapest slop filter you have.

## Stage 2 — Specify (the keystone)
Slop enters through underspecification — the model fills vague intent with plausible guesses, and plausible-but-wrong *is* slop. The spec removes the room. Every requirement gets an observable pass/fail, and the two non-functional qualities that never survive as review notes — **security** and **idempotency** — are written as testable criteria here, or they silently don't happen.

Lean template (graduate to GitHub **Spec Kit** for heavier, multi-agent work):

```
---
id: SPEC-<slug>
status: draft | approved | building | done
tier: throwaway | standard | system
---
# <Title>

## Problem / intent
One paragraph. What is true after this ships that isn't now.

## Non-goals
What this explicitly does not do (bounds the blast radius).

## Contracts (the seams)
The types/schemas crossing each boundary — the single source both sides
generate from (Zod / Pydantic / OpenAPI / tRPC). List each seam + its owner.

## Acceptance criteria (falsifiable)
- [ ] AC1 — <observable behavior> → test: <path::name>
- [ ] AC2 — ...
Each line maps to ONE test written in Stage 3. No criterion without a test.

## Security cases
- authz:   <who may / may not, per mutation>
- input:   <what is validated / rejected>
- secrets/effects: <none in client bundle; egress; …>  (→ [[Deterministic Gates]])

## Idempotency / effects
- run-twice: <end state identical; no duplicate side effects>
- effect inventory: <writes, emails, charges, migrations>

## Open questions
Unknowns that block a falsifiable criterion. Resolve before building.

## Decisions
Link to the decision-log entries this spec settled (the *why*).
```

Skeptic: don't over-spec exploration. Spec depth matches the tier — a `standard` feature gets contracts + acceptance criteria; a `system` adds security/idempotency/decisions; a `throwaway` skips this stage. Over-specification is the same overhead trap as over-gating.

## Stage 3 — Decompose / Initialize (the initializer)
In Cowork, turn the approved spec into the build's starting state — the one-time setup the per-session build agent never repeats:

1. **Order the units** by dependency — contracts/seams first, then the code that fills them.
2. **Scaffold the skeleton** — files, module boundaries, and the generated seams (run codegen so the contracts *exist* before the code does).
3. **Write the acceptance tests red** — one test per acceptance criterion, all failing. Humans/Cowork own these oracles; the build session may not edit them ([[Writing Tests]] #12).
4. **First commit.** This commit *is* the handoff artifact.

The unit list is a **generated view, not a hand-maintained ledger**: "what's left" = run the tests and read which are red. Don't keep a parallel JSON truthful by willpower — it drifts and lies. Git history + the red suite are the state. (Claude Code's `--init-only` / `Setup` hook is the native seam for an initializer distinct from per-session start.)

## Stage 4 — Build-to-green (in Claude Code)
The per-unit loop the executing agent runs — one unit per session, repo left clean for the next shift ([[Invariants]] #5, #8):

1. **Read ground truth first** — the spec, `git log`, and the failing tests. Never re-derive intent from memory.
2. **Take ONE red unit** — the smallest shippable slice.
3. **Make its test pass without weakening it.** The acceptance test is frozen upstream; if it's wrong, that's a spec change in Cowork, not an edit here. This kills the tautological-test failure — the agent writing impl *and* test from the same wrong assumption. It may *add* tests; it may not *edit* the oracle.
4. **Run the fast gate** (per-edit ring, below). Red → fix before continuing; escalate to a stronger model on a *repeated* red rather than guessing past it.
5. **Commit small and atomic** — Conventional Commits, the *why* in the body ([[Invariants]] #5).
6. **Stop.** Hand-update nothing; the next session re-reads ground truth.

## Stage 5 — The Gate (the deterministic membrane)
The full tool table, configs, and retrofit order live in [[Deterministic Gates]] — this note doesn't restate them. What's specific to the loop is **where** the gate fires and the rule that there is **one definition of green**:

> A single `gate` entrypoint (an npm script / `make gate`) runs typecheck → lint → fitness functions → tests → secret scan. **Pre-commit, CI, and the agent's Stop hook all call the same script.** One source of truth for "green" — you can't be green locally and red in CI.

Three rings, cheapest first:

- **Per-edit (fast).** Claude Code `PostToolUse` hook matched `Edit|Write` → typecheck/lint the *changed file*, exit non-zero to bounce the model immediately. Cheap, file-scoped.
- **Per-turn (the green-wall).** `Stop` / `SubagentStop` *command* hook runs the full `gate`; the agent cannot end its turn while red. This is "done = green," enforced by mechanism. Caveats: read `stop_hook_active` to avoid the loop-cap; raise the ceiling with `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`; prefer `command` over the experimental `agent` hook.
- **Pre-merge.** `gate` again in pre-commit + CI, plus the adversarial pass — `/security-review` and SAST for the semantics static checks miss. Protected paths (`.git`, `.claude`, pre-commit/husky configs) mean the agent can't disable its own gates to pass.

By-construction column — do this *before* reaching for a check:

- **Generate the seam.** tRPC erases the client/server type boundary; Zod/Pydantic/OpenAPI give one schema both sides derive from. Two things generated from one can't drift.
- **Make illegal states unrepresentable.** Discriminated unions + `never` exhaustiveness, branded types, smart constructors. A forgotten case becomes a compile error.
- **Fitness functions.** `dependency-cruiser` (TS) / `import-linter` (Python) make architecture a gate, not a hope:

```js
// .dependency-cruiser.js — forbid UI → DB direct imports
module.exports = { forbidden: [{
  name: 'no-ui-to-db',
  severity: 'error',
  from: { path: '^src/ui' },
  to:   { path: '^src/db' },
}]};
```

An agent that wires a component straight into the DB fails the build, reads the error, and reroutes — documented real-world behavior, not theory.

## Stage 6 — Distill (grow the floor)
Only the durable goes back into the vault; transient state stays in the repo. Three things qualify:

- **Decisions** → a decision log (ADR-style: context → decision → why → consequences). The one artifact that genuinely can't be regenerated from code.
- **New invariants** → [[Invariants]], when a lesson proves universal.
- **The Slop Register** → every slop caught in review becomes a rule that feeds *both* the prompt and a gate.

Prefer **executable lessons** over prose: a new ESLint rule, a `dependency-cruiser` constraint, a regression test. Executable lessons fail loud when they rot; prose lessons mislead silently (the stale-doc trap [[Invariants]] #7 warns about). Give each lesson provenance — the failure that birthed it, `path:line` — so its staleness is checkable.

**Slop Register** (new; grows one incident at a time):

| Date | Slop observed | Rule added (prompt / gate) | Provenance |
|------|---------------|----------------------------|------------|
| 2026-06-14 | *seeded from the [[Deterministic Gates]] clusters* | the baseline `gate` suite | — |

Floor from [[Invariants]] (the failure modes everyone hits); accretion from the register (your scars). Both: the universal set is the starting gate, the register is how it grows.

## Scale tiers (pick before you build)
- **Throwaway** (a script, a spike): Capture → Build. Skip spec/decompose/distill. Floor only — strict types + secret scan.
- **Standard** (a feature): Specify (contracts + acceptance criteria) → Build-to-green → Gate. No decision log unless something surprised you.
- **System** (durable, multi-session, others depend on it): the full loop + initializer + decision log + idempotency/security criteria.

Over-applying the process is the same mistake as skipping it. The tier *is* the first decision.

## Bootstrapping order (highest ROI first; mirrors the [[Deterministic Gates]] retrofit)
1. **One `gate` script + strict types** (`tsc --noEmit` strict / `mypy --strict`) as the CI gate. ~80% of the determinism for near-zero design.
2. **Secret scan + frozen lockfile + dep audit** — the supply-chain floor.
3. **`PostToolUse` fast gate + `Stop` green-wall** in `.claude/settings.json`.
4. **One fitness function** (`dependency-cruiser` / `import-linter`) for your main layer boundary.
5. **Spec template + decision log** for the first `system`-tier idea.
6. **Slop Register**, grown per incident.

Add reactively. A guard earns its place once its absence has cost you, or the failure mode is universal enough to seed from [[Invariants]].

## Skeptic's corner
- **Convergent, not novel.** This is the 2026 consensus (harness engineering / SDD); the edge is the by-construction bias and the single-`gate` discipline, not the parts.
- **Gates catch interface and known-pattern slop, not semantics.** Code can be green and wrong — green types are a filter, never a correctness proof ([[Good Code in the AI Age]] skeptic's corner; [[Invariants]] #4).
- **Claude Code hook specifics are version-gated**; the `agent`-type hook is experimental. Pin the load-bearing wall to `command` hooks and re-check the docs on each upgrade (the harness is disposable).
- **Most SDD / "harness" best-practice content is vendor SEO.** Load-bearing here: the Claude Code docs, GitClear's churn data, Spec Kit's adoption, and fitness functions as a pre-existing concept.
- **Agent-written tests are weak oracles** ([[Writing Tests]] #12) — the loop leans on *pre-written* acceptance tests as the target, which is why Stage 3 freezes them upstream.

## Sources
- SDD: [Spec Kit](https://github.com/github/spec-kit) · [9 Best SDD Tools 2026 — MarkTechPost](https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/)
- Harness engineering: [Augment Code](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents) · [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)
- Fitness functions: [InfoQ](https://www.infoq.com/articles/fitness-functions-architecture/) · [python-ai-guardrails-template](https://github.com/tortastudios/python-ai-guardrails-template)
- Quality gates / churn: [How to Avoid AI Code Slop](https://newsletter.eng-leadership.com/p/how-to-avoid-ai-code-slop) · [Quality Gates against AI slop — Frank Neff](https://www.frankneff.com/blog/2026-02-19-quality-gates-against-ai-slop/)
- Claude Code: [Hooks](https://code.claude.com/docs/en/hooks) · [Hooks guide](https://code.claude.com/docs/en/hooks-guide) · [Sub-agents](https://code.claude.com/docs/en/sub-agents) · [Permission modes](https://code.claude.com/docs/en/permission-modes)

---
## Related
[[CLAUDE]] · [[Invariants]] · [[Deterministic Gates]] · [[Good Code in the AI Age]] · [[Writing Tests]] · [[TypeScript Development]] · [[Code Conventions]]
