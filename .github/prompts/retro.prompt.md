---
mode: agent
description: The transactional compaction pass. Retro note is the write-ahead log.
---

# Retro (transactional compaction — invariants I5 + I8)

Triggers: "retro", session end, or the warmup ratchet firing.

Do the steps **in order**. The retro note is the write-ahead log: check each box off **in the
file** as you finish it. If a retro is interrupted, the next session resumes from the first
unchecked box. **The destructive step (i) runs last and is gated on a–h being checked.**

## Step a — Create the WAL (FIRST ACTION)
Create `KB/Notes/Retro/YYYY-MM-DD retro.md` with this exact skeleton:

```markdown
---
type: retro
created: YYYY-MM-DD
status: active
---
# Retro — YYYY-MM-DD

## Checklist (WAL)
- [ ] b. Synthesis
- [ ] c. Lint clean
- [ ] d. Promote Inbox notes
- [ ] e. Update Meta-Cognition / Retrieval Strategies
- [ ] f. Update action ledger
- [ ] g. Health block
- [ ] h. Archive aged daily folders
- [ ] i. Overwrite Active Context + git commit  (LAST, gated)

## Synthesis
<!-- what changed, reusable heuristics, gaps -->

## Health
<!-- filled at step g -->
```

## Steps b–h
- **b. Synthesis.** From today's `logs.md`/`briefing.md` and the session: what changed, reusable
  heuristics worth keeping, gaps to revisit. Write into `## Synthesis`.
- **c. Lint.** Run `tools/lint.sh`. Record the result line in the retro note. Fix every
  violation, then re-run until exit 0.
- **d. Promote.** Route qualifying `KB/Inbox/` notes to their typed homes (canonical-first;
  supersede rather than contradict).
- **e. Process/search memory.** Update `KB/Meta-Cognition.md` for process changes and/or
  `KB/Retrieval Strategies.md` for search changes. Skip if nothing changed.
- **f. Ledger.** In `action-ledger.md`, move finished items to `## Completed` with a date stamp.
  Never delete a line.
- **g. Health block.** Write `## Health` in the retro note:
  - lint result (clean / N violations fixed)
  - notes by type (from the lint summary)
  - Inbox depth
  - days since previous retro
  - pinned-set size: `bytes(profile.md + Active Context.md + action-ledger.md + today's briefing.md) ÷ 4` ≈ tokens, vs. the 4,000-token budget
  - archive actions taken
  - **If the pinned set is over budget, evict now:** move detail to a vault note, leave a
    one-line link, re-measure.
- **h. Archive.** Move any `YYYY-MM-DD/` folder older than 14 days into `KB/Archive/daily/`
  (move, not delete).

## Step i — Commit (LAST; gated on a–h all checked)
1. Overwrite `Active Context.md` with the new current state (focus, open threads, next action).
2. Commit the ledger:
   ```sh
   git add -A && git commit -m "retro: YYYY-MM-DD"
   ```
The commit is part of the protocol, not an afterthought. Then check box i.
