---
type: concept
created: 2026-06-12
status: active
---
# Retrieval Strategies

**Hub of proven lookup patterns and retrieval discipline.** Records *how to find things* in this
system. Root hub file: folder↔type law exempt, schema still applies. Changes to search behavior
get recorded here at retro.

## Retrieval discipline (stable)
- **Pinned-set first.** Start from `profile.md`, `Active Context.md`, `action-ledger.md`, and
  today's `briefing.md`. They are already loaded — exploit them before searching.
- **≤ 3 links, then stop.** Follow at most three links out from the pinned set per orientation.
- **Grep on demand, never broad scans.** Targeted `grep`/`rg` over `Notes/` beats reading folders.
- **Canonical-note-first lookup.** Before writing a new note, grep for an existing one on the
  subject and update it in place.
- **Supersession-aware.** Filter or explicitly flag `status != active`. Cite a superseded note
  only alongside its successor (`superseded_by`).

## Proven patterns
- Find all notes of a type: `grep -rl '^type: project' Notes/Projects/` (or just list the
  folder — folder↔type law guarantees the mapping).
- Find superseded notes that still need a successor check:
  `grep -rl '^status: superseded' Notes/ Inbox/ Archive/`.
- Find recent activity: scan the newest `YYYY-MM-DD/` daily folders at the repo root.
- Find a person/system/project by partial name: `grep -ril '<term>' Notes/`.
- Locate the newest retro (and the Health trend): `ls Notes/Retro/`.

## Patterns log
- **2026-06-12** — Initial strategies seeded at build. Retrieval is grep-based; no FTS5/SQLite
  index yet (its growth trigger has not fired — see `[[Meta-Cognition]]`). See `[[2026-06-12 retro]]`.

<!-- Append future search-behavior changes here, dated and linked to the retro that introduced them. -->
