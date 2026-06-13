---
mode: agent
description: Capture something into durable memory, correctly routed and non-duplicative.
---

# Remember

Triggers: "remember this", "put this in the vault", "save this for later".

## Flow
1. **Decide durability.** Does this matter across sessions? If it only matters today, it belongs
   in today's `logs.md`/`briefing.md`, not the vault — say so and stop.
2. **Route by type:**
   - changes how Charlie *operates* → `KB/Meta-Cognition.md`
   - changes how Charlie *searches* → `KB/Retrieval Strategies.md`
   - person → `KB/Notes/People/`        · system → `KB/Notes/Systems/`
   - project → `KB/Notes/Projects/`     · decision → `KB/Notes/Decisions/`
   - playbook → `KB/Notes/Playbooks/`   · concept → `KB/Notes/Concepts/`
   - meeting → `KB/Notes/Meetings/`
   - genuinely unclear → `KB/Inbox/` (retro will route it later)
3. **Canonical-note-first.** Before creating anything, grep for an existing note on this subject.
   If one exists, **update it in place.** Creating a near-duplicate is a lint violation.
4. **Frontmatter (required on every vault `.md`):**
   ```yaml
   ---
   type: <matching the folder>
   created: <YYYY-MM-DD>
   status: active
   ---
   ```
5. **Supersession, not contradiction.** If this reverses or invalidates an existing note, set the
   old note's `status: superseded` and `superseded_by: <path to the new/updated note>`. Never
   edit the old note into agreement; never delete it.
6. **Ask before writing ambiguous memory.** If you're unsure what Jonah wants remembered, or
   where it goes, ask one crisp question rather than guessing.

## After writing
Run `tools/lint.sh` if you created or moved a note, and fix anything it flags.
