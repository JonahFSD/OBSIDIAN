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

## Knowledge base (read on demand)
- [[Good Code in the AI Age]] — the invariants above, each grounded in a durable LLM failure mode, with sources.
- [[Code Conventions]] — conventions hub (Conventional Commits; per-language standards).
- [[TypeScript Development]] — TypeScript patterns, generics, utility types, type guards, React/Node, `tsconfig`, strict mode.
