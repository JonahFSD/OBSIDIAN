# CLAUDE.md — Coding Agent

A lean, curated knowledge base of coding standards and heuristics for an AI coding agent. Follow
the rules here; read the three notes below on demand for depth. **Keep this file short — a line
stays only if removing it would cause a mistake.** When in doubt, the live session and the target
repo's own conventions win over this file.

## Always
- **Verify outside the model.** Trust types, tests, and the build over your own judgment. Run the
  checks; never call a change done on a clean-looking diff alone.
- **Treat recalled APIs/packages as low-trust.** Confirm a package exists and an API is current
  before using it; pin versions; don't invent signatures.
- **Make types explicit.** Lean on the type checker as the first error gate.
- **Small, atomic diffs.** One logical change per commit; keep changes reviewable and revertible.
- **Conventional Commits.** `type(scope): summary` — the body carries the *why*; the diff shows the *what*.
- **Keep code localizable.** Clear, intention-revealing names; consistent, grep-able structure;
  find the right place before editing.
- **Don't trust agreement.** If the user — or your own first idea — might be wrong, say so and
  check; weigh the counter-case before converging.
- **Match the codebase.** Existing conventions in the repo beat personal preference.

## Working memory
- Read `NOTES.md` first; record your plan, progress, and decisions there as you work; keep it
  pruned — edit in place and delete stale lines, don't let it grow into contradictory clutter.
- Durable decisions graduate to `decisions/` (ADR-lite: append-only; supersede, never overwrite).
- Non-negotiable rules belong in the target repo's CI / hooks / linters, not in prose here.

## Knowledge base (read on demand)
Knowledge notes are **append-only ledgers** — add entries and supersede; don't overwrite or delete.
- [[Good Code in the AI Age]] — the durable LLM failure modes (the "why") + caveats.
- [[Invariants]] — the coding invariants that follow (ledger).
- [[Writing Tests]] — test-writing heuristics (ledger).
- [[Writing Documentation]] — documentation heuristics (ledger).
- [[Code Conventions]] — conventions hub (Conventional Commits; per-language standards).
- [[TypeScript Development]] — TypeScript patterns, generics, utility types, type guards, React/Node, `tsconfig`, strict mode.
