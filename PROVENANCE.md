# PROVENANCE

**What this is.** A record of how this instance of the memory system — the **Obsidian Knowledge
Base (OKB)** — came to exist. It replaces the original Windows build's `MIGRATION.md` /
`MIGRATION-REPORT.md` / `MIGRATION-DEFERRED.md`, which documented a phased self-migration that did
not happen here. This instance was **built fresh**, not migrated.

## Build

- **Date:** 2026-06-12
- **Machine:** personal macOS (Mac mini)
- **Repo / system root:** `~/ARCHIPELIGO/OBSIDIAN/` — the OKB (self-contained Obsidian vault + git repo).
- **Source of design:** the "Obsidian Memory System — Complete Reference" document, recreated
  here as `CHARLIE.md` (canonical) + `REFERENCE.md` (descriptive).
- **Built by:** Claude (Cowork), at Jonah's request to recreate the system on this machine.

## Decisions made at build time (the macOS adaptations)

| Original (Windows) | This instance (macOS) | Why |
|---|---|---|
| Workspace root `C:\Uniti\workspace\` | the OKB repo `~/ARCHIPELIGO/OBSIDIAN/` | A self-contained vault+repo on Jonah's machine (see Restructure below). |
| Durable store `vault\` | the durable subtree of the vault (`Notes/`, `Inbox/`, `Archive/` + hubs) | Reuses Jonah's existing Obsidian vault rather than a parallel store. |
| Linter in PowerShell (`lint-vault.ps1` + `lint.cmd`) | Python 3 (`lint_vault.py` + `lint.sh`) | No PowerShell on macOS by default; Python 3 stdlib gives robust frontmatter parsing while staying dependency-free. |
| `lint.cmd` invocation wrapper | `lint.sh` (POSIX, `chmod +x`) | Same "encode the parser-sensitive invocation exactly once" policy, in the native shell. |
| Migration records (3 files) | this `PROVENANCE.md` | Nothing was migrated; an honest build record is the correct artifact. |
| Retro hook in Claude Code `settings.json` | the warmup staleness ratchet (primary); hook optional | The ratchet is sufficient and tool-independent; a Stop hook is an optional mirror, not part of OKB. |

## Restructure (same day, 2026-06-12)

After the initial build, Jonah reorganized the folders, and the system was consolidated to match:

- Renamed `~/CODE` → `~/ARCHIPELIGO` (his code workspace, which also holds independent repos
  `Arena/`, `Bayview/`, `MedAI/`) and the vault `KB/` → `OBSIDIAN/`.
- **Scoped the git repo to `OBSIDIAN/`** (its own `.git`), so the OKB is self-contained and the
  other projects' repos are untouched. `~/ARCHIPELIGO/` is just the parent folder, not a repo.
- **Moved all operating files into the vault** (`CHARLIE.md`, `REFERENCE.md`, `PROVENANCE.md`,
  the pinned set, `tools/`, the daily folders), so the entire system lives in one folder you open
  in both Obsidian and Claude Code.
- **Rescoped the linter** to check only the durable-note subtree (`Notes/`, `Inbox/`, `Archive/`
  + the two hubs); the operating files that now share the vault are skipped.
- Named the repo the **Obsidian Knowledge Base (OKB)**.
- The `.github/prompts/` and `.claude/` tooling were intentionally left out of OKB (the §7
  workflows in `CHARLIE.md` are authoritative); any copies under `~/ARCHIPELIGO/` are not part of
  this repo.

## Carried over unchanged

The conceptual model, state model, vault schema and its four laws, the transactional retro
protocol (with the retro note as a write-ahead log), the invariant contract I1–I9, the pinned-set
budget, the growth-trigger policy, and the operating rules are all faithful to the original.

## What was deliberately NOT done (entry triggers in `Meta-Cognition.md` §Growth Triggers)

- No FTS5/SQLite index — grep suffices until the vault is large or grep gets noisy (twice).
- No weekly rollup tier — not needed until Monday warmups breach the pinned budget (twice).
- No separate structured task store — the flat `action-ledger.md` suffices under ~30 open items.
- No embeddings/semantic search — keyword search suffices until vocabulary drift bites (twice).

Each remains correctly absent until its written trigger fires. See `Meta-Cognition.md`.

## First ledger entry

The inaugural commits of this repository record the build and the same-day restructure, and the
inaugural retro note (`Notes/Retro/2026-06-12 retro.md`) records the build as the first
compaction and sets the baseline for the warmup staleness ratchet.
