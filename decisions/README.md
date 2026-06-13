# Decisions (ADR-lite)

Durable, append-only record of project decisions the agent must respect. One file per decision:
`NNNN-short-title.md` (e.g. `0001-use-pnpm.md`). **Never edit a past decision** — to change one,
write a new file and mark the old one `superseded`. The agent reads the current `accepted`
decisions; the history stays for the *why*. Keep each short.

Only record a real invariant — a stable, broadly-applicable choice you'd want enforced. Anything
inferable from the code, or a passing preference, does not belong here.

## Template

```markdown
---
status: accepted        # accepted | superseded
date: YYYY-MM-DD
supersedes:             # NNNN-... (if this replaces one)
superseded_by:          # NNNN-... (filled in if later reversed)
---
# NNNN — <decision title>

**Context.** Why this came up.
**Decision.** What we chose.
**Consequences.** Trade-offs and what this now constrains.
```
