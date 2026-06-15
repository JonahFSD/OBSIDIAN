# CLAUDE.md — Coding Agent

A lean, curated knowledge base of coding standards and heuristics for an AI coding agent. Follow
the rules here; read the notes (mapped in [[README]]) on demand for depth. **Keep this file short —
a line stays only if removing it would cause a mistake.** When in doubt, the live session and the
target repo's own conventions win over this file.

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
- **Write the least code that works.** Before adding code, stop at the first rung that holds: does it need to exist (YAGNI) → stdlib → native platform feature → installed dependency → one line → only then the minimum that works. Never cut security, input validation, data-loss handling, or accessibility. (Ponytail.)

## Safety (the backstop — [[Deterministic Gates]] is what actually enforces these)
- **Never run irreversible/destructive commands** — force-push, `reset --hard`, `DROP`, prod
  migrations, `rm -rf` — unprompted. Ask first.
- **Security:** authz check on every mutation; never hand-roll crypto; secrets never in source.
- **Surface and handle errors** — never silently swallow.
- **Reproduce and root-cause before fixing** — don't suppress the symptom.

## Knowledge base (read on demand)
Start at [[README]] — it maps every note. Pull the relevant one into context as needed.
