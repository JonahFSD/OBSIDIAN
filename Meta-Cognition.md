---
type: concept
created: 2026-06-12
status: active
---
# Meta-Cognition

**Process memory: how Charlie improves Charlie.** This is the hub for changes to *how the system
operates* — not domain facts (those go to typed `Notes/`). Root hub file: folder↔type law
exempt, schema still applies. Canonical operating rules live in `CHARLIE.md`; this file records
the *evolution* of process and the explicit triggers for deferred components.

## Operating principles (stable)
- Mechanism over intention: guarantees are enforced by git, lint, the retro protocol, and
  budgets — never by remembering to be careful.
- Write-through journaling, deferred judgment: capture cheaply to logs in-session; decide
  durability at compaction (retro).
- Canonical-note-first: update the one true note in place; never duplicate; supersede rather
  than contradict.
- A component earns its place only when the failure mode it prevents has occurred **twice.**
  Until then, its absence is correct.

## Growth Triggers (invariant I9 — verbatim policy)

| Component (deferred) | Build when… | Form |
|---|---|---|
| FTS5/SQLite derived index | grep returns too many hits to rank by eye on two occasions, OR vault > ~150 notes | Single SQLite file; index derived from Markdown; rebuildable |
| Weekly rollup tier | Monday warmup (3 briefings) breaches the pinned budget twice | Sunday compaction → `Notes/Retro/YYYY-Www weekly.md` |
| Structured task state | action ledger > ~30 open items, or dependencies stop fitting a flat list, twice | Separate table/file from knowledge memory (different retention semantics) |
| Embeddings / semantic search | keyword search misses a known-existing note via vocabulary drift, twice | Local embedding model; index remains derived/disposable |

Record each firing in a retro **before** building the component.

## Process log
- **2026-06-12** — System built fresh on macOS from the reference. macOS adaptations: linter is
  Python 3 (was PowerShell); migration records replaced by `PROVENANCE.md`. No growth triggers
  fired (correctly). See `[[2026-06-12 retro]]`.
- **2026-06-12** — Consolidated into the self-contained **Obsidian Knowledge Base (OKB)** repo at
  `~/ARCHIPELIGO/OBSIDIAN/`: operating files moved into the vault, git scoped to the vault, the
  linter rescoped to the durable subtree (`Notes/`, `Inbox/`, `Archive/` + hubs). See `PROVENANCE.md`.

<!-- Append future process changes here, newest at the bottom, each dated and linked to its retro. -->


---
## Related
[[CHARLIE]] · [[Retrieval Strategies]] · [[REFERENCE]] · [[2026-06-12 retro]]
