---
mode: agent
description: Warm up a session — staleness ratchet first, then load the working set.
---

# Warmup

Triggers: "warmup", "load active context", or the start of any working session.

## Step 0 — Staleness ratchet (MANDATORY FIRST STEP)
Run the retro-staleness check:

```sh
python3 tools/retro_status.py
```

This reports days since the newest `KB/Notes/Retro/*.md`. **If retro is more than 1 day overdue**,
open with exactly this and then default to running a retro:

> "Retro is N days overdue — running it now before new work (say 'defer' to override)."

If Jonah says "defer", append a `retro deferred YYYY-MM-DD` line under `## Open` in
`action-ledger.md` (skips are never silent — invariant I2) and continue.

## Step 1 — Load the working set (lazy page-in, no broad scans)
1. Read `Active Context.md` — the current focus and open threads.
2. Follow **at most 3** links from it that are relevant to what Jonah is about to do.
3. Read `profile.md`.
4. Read the open items in `action-ledger.md`.
5. Read today's `YYYY-MM-DD/briefing.md` if it exists.

Do **not** broad-scan the vault. Anything else is grep/read on demand.

## Return
A short orientation: **current focus**, **top open threads**, and the **next likely action.**
