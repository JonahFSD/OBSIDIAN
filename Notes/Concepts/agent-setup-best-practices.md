---
type: concept
created: 2026-06-12
status: active
---
# Agent setup best practices (2025–2026)

Synthesis of current, credible guidance on what good AI-agent setups look like, captured for the
OKB. The through-line: **treat the context window as a scarce resource — find the smallest set of
high-signal tokens that produces the outcome — then do the simplest thing that works.** This note
also records where this system ([[CHARLIE]]) already aligns.

## Durable patterns

- **Memory = files on disk, pulled in on demand.** Agents append progress/notes as they work and
  re-read them after a context reset; git history lets a fresh session reconstruct state. This is
  exactly write-through journaling → compaction. *(OKB: logs → retro → vault.)*
- **Grep beats vectors for structured/Markdown corpora.** Claude Code shipped a vector DB early
  and removed it — agentic grep/find "works better, simpler, and doesn't have the security,
  privacy, staleness, and reliability issues." Reserve embeddings for large, shapeless prose.
  *(OKB: grep-first retrieval; FTS5 deferred behind a written trigger — see [[Retrieval Strategies]].)*
- **Keep the always-loaded rules file short.** Test each line: "would removing this cause a
  mistake?" If not, cut it — bloated `CLAUDE.md`/`AGENTS.md` files get ignored.
- **The loop is gather → act → verify → repeat**, and *verification is the highest-leverage part*
  — give the agent a check it can run (tests, a linter, a reviewer subagent in a fresh context).
  Separate explore→plan from implement→commit. *(OKB: retro's lint-gate + git-commit-last.)*
- **Context isolation via subagents; determinism via hooks.** Push context-heavy or repeatable
  work out of the main thread.
- **Git as an append-only ledger / event sourcing.** History is truth; derived views (indexes,
  summaries, the "current state" file) are disposable projections you can rebuild. *(OKB's core
  design thesis.)*

## Failure modes to avoid

Kitchen-sink sessions (clear context between unrelated tasks) · correction spirals (reset after
~2 failed fixes) · over-stuffed rules files · the trust-then-verify gap (never ship unverified
output) · unbounded context growth · "premature victory" (a later session declaring done). *(OKB:
persistent [[Active Context]] + the Health block guard the last one; see [[Meta-Cognition]].)*

## Where this system stands

OKB already embodies the durable principles: scarce/budgeted context, write-through journaling,
grep-first retrieval, and ledger-as-truth. The main growth edge is the **verification / subagent**
side — a reviewer pass or test-style check that the retro hints at but doesn't yet automate. Watch
`CHARLIE.md` length if it ever becomes always-on context for an agent (push detail to on-demand
notes).

## Sources

- Anthropic — Effective context engineering for AI agents: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic — Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic — Building effective agents: https://www.anthropic.com/research/building-effective-agents
- Anthropic — Claude Code best practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Cursor — Rules documentation: https://cursor.com/docs/rules
- Zansara — Is grep really better than a vector DB?: https://www.zansara.dev/posts/2026-03-15-vector-dbs-vs-grep/

---
## Related
[[CHARLIE]] · [[Retrieval Strategies]] · [[Meta-Cognition]]
