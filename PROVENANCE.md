# PROVENANCE

**What this is.** A record of how this instance of the memory system came to exist. It replaces
the original Windows build's `MIGRATION.md` / `MIGRATION-REPORT.md` / `MIGRATION-DEFERRED.md`,
which documented a phased self-migration that did not happen here. This instance was **built
fresh**, not migrated.

## Build

- **Date:** 2026-06-12
- **Machine:** personal macOS (Mac mini)
- **Workspace root:** `~/CODE` (`/Users/jonahelliott/CODE`)
- **Source of design:** the "Obsidian Memory System — Complete Reference" document, recreated
  here as `CHARLIE.md` (canonical) + `REFERENCE.md` (descriptive).
- **Built by:** Claude (Cowork), at Jonah's request to recreate the system on this machine.

## Decisions made at build time (the macOS adaptations)

| Original (Windows) | This instance (macOS) | Why |
|---|---|---|
| Workspace root `C:\Uniti\workspace\` | `~/CODE` | The folder Jonah selected on this machine. |
| Durable store `vault\` | the existing Obsidian vault `KB/` | `KB/` was already an empty Obsidian vault; reuse it rather than create a parallel one. |
| Linter in PowerShell (`lint-vault.ps1` + `lint.cmd`) | Python 3 (`lint_vault.py` + `lint.sh`) | No PowerShell on macOS by default; Python 3 stdlib gives robust frontmatter parsing while staying dependency-free. |
| `lint.cmd` invocation wrapper | `lint.sh` (POSIX, `chmod +x`) | Same "encode the parser-sensitive invocation exactly once" policy, in the native shell. |
| Migration records (3 files) | this `PROVENANCE.md` | Nothing was migrated; an honest build record is the correct artifact. |
| Retro hook in Claude Code `settings.json` (Windows) | `.claude/settings.json` advisory Stop hook | Same intent; the warmup staleness ratchet remains the primary enforcement (defense in depth). |

## Carried over unchanged

The conceptual model, state model, vault schema and its four laws, the transactional retro
protocol (with the retro note as a write-ahead log), the invariant contract I1–I9, the pinned-set
budget, the growth-trigger policy, and the operating rules are all faithful to the original.

## What was deliberately NOT done (entry triggers in `KB/Meta-Cognition.md` §Growth Triggers)

- No FTS5/SQLite index — grep suffices until the vault is large or grep gets noisy (twice).
- No weekly rollup tier — not needed until Monday warmups breach the pinned budget (twice).
- No separate structured task store — the flat `action-ledger.md` suffices under ~30 open items.
- No embeddings/semantic search — keyword search suffices until vocabulary drift bites (twice).

Each remains correctly absent until its written trigger fires. See `KB/Meta-Cognition.md`.

## First ledger entry

The inaugural `git commit` of this repository is the build itself, and the inaugural retro note
(`KB/Notes/Retro/2026-06-12 retro.md`) records the build as the first compaction and sets the
baseline for the warmup staleness ratchet.
