# Logs — 2026-06-12

Append-only execution journal. Newest at the bottom.

- Inspected `~/CODE`: found an empty Obsidian vault `KB/`; not yet a git repo.
- Decisions confirmed with Jonah: use `KB/` as the vault; linter in Python 3; replace migration
  records with a provenance note.
- Scaffolded directories: `tools/`, `.github/prompts/`, `.claude/`, `KB/Notes/{8 typed folders}`,
  `KB/Inbox`, `KB/Archive/daily`, today's daily folder. Removed the default Obsidian `Welcome.md`.
- Wrote `.gitignore` (excludes `KB/.obsidian/`, `KB/.trash/`, `.DS_Store`).
- Wrote canonical docs: `CHARLIE.md`, `REFERENCE.md`, `PROVENANCE.md`.
- Wrote pinned files: `profile.md`, `Active Context.md`, `action-ledger.md`.
- Wrote workflow prompts: `Charlie.agent.md`, `warmup`, `remember`, `retro`, thermonuclear review.
- Built enforcement tooling: `tools/lint_vault.py` (stdlib only), `tools/lint.sh`,
  `tools/retro_status.py`, `.claude/settings.json` advisory Stop hook. Smoke-tested: lint exits
  0 on the empty vault; retro_status reports no baseline yet.
- Wrote vault hubs `Meta-Cognition.md` + `Retrieval Strategies.md` and the inaugural retro note.
- Measured pinned budget (~895 tokens), filled the retro Health block, initialized git, committed.

## Restructure (later same day)
- Jonah renamed `~/CODE` → `~/ARCHIPELIGO` (his code workspace, also holding `Arena/`, `Bayview/`,
  `MedAI/` — each its own repo) and the vault `KB/` → `OBSIDIAN/`, and moved the operating files
  into the vault.
- Consolidated to match: scoped the git repo to `OBSIDIAN/` (its own `.git`) so the **Obsidian
  Knowledge Base (OKB)** is self-contained and the other repos are untouched; rescoped the linter
  to the durable subtree (`Notes/`, `Inbox/`, `Archive/` + hubs); repaired all paths in the docs
  and tools; left `.github/.claude` out of OKB per Jonah (the §7 workflows are authoritative).
- Verified lint clean + negative test; re-committed.


---
_Related:_ [[CHARLIE]] · [[2026-06-12 retro]]
