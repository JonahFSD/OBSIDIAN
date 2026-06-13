# The Memory System — Complete Reference (macOS instance)

**Status of this document:** Descriptive reference, written for consumption by another
document, agent, or person. It is **not** a second operating authority. Per invariant I6, the
single canonical operating document is `CHARLIE.md` at the workspace root; if this reference and
`CHARLIE.md` ever disagree, **`CHARLIE.md` wins and this document is stale.** Items marked
⚠ AS-BUILT depend on choices made when this instance was built and should be verified against
the machine before being relied on.

This instance was built on **2026-06-12** on a personal **macOS** machine, recreated from the
original Windows reference. Adaptations from the original: workspace root is `~/CODE` (not
`C:\Uniti\workspace`); the durable store is the existing Obsidian vault `KB/` (not `vault/`);
the schema linter is **Python 3** (not PowerShell); there was no migration, so the migration
records are replaced by `PROVENANCE.md`. See `PROVENANCE.md` for the full build record.

---

## 1. What the system is

A retrieval-first, ledger-structured personal memory system for an AI assistant ("Charlie")
operating on a personal macOS machine. Human-readable Markdown is the sole source of truth;
every guarantee that matters is enforced by mechanism (git, lint, hooks, budgets) rather than by
behavioral intention.

Design lineage: the architecture is one pattern — **append-only history as truth, with derived,
disposable projections serving reads** — instantiated at personal scale. The same pattern
underlies git, LSM trees, event sourcing, Kafka, and the Convex database.

## 2. Conceptual model (the mental map everything else hangs on)

| Component | Computing analog | Consequence |
|---|---|---|
| Context window | RAM | Expensive, volatile, never the system of record |
| `profile.md`, `Active Context.md`, `action-ledger.md`, today's `briefing.md` | **Pinned memory** (pages never evicted) | Loaded every session → highest cost per token → strictly budgeted |
| Daily `logs.md` / `briefing.md` | **Write-ahead log / journal** | In-session writes are cheap, append-only, judgment-free |
| Retro | **LSM compaction pass** | Merges journal → durable storage; extracts cross-session signal; promotes/demotes |
| Vault (`KB/`) | **Durable storage / source of truth** | Schema-enforced, lint-gated, supersession-aware |
| Git repository | **The ledger** | Every state transition recoverable, diffable, bisectable |
| Manifests, links | **Page table** | Sessions fault pages in lazily via read/grep |
| Retrieval (grep now; FTS5 later) | **Derived index** | Disposable; rebuildable from the Markdown at any time |

Write policy: **write-through journaling** — append observations/decisions/outcomes to today's
log with near-zero ceremony; defer all durability judgment to compaction (retro). Read policy:
**lazy page-in** — load the pinned set plus links followed on demand; never broad vault scans.

## 3. Physical layout

```
~/CODE/                              ← workspace root = transient operating surface; git repo root
├── .git/                            Local-only repository. No remote. The ledger.
├── .gitignore                       Excludes KB/.obsidian/, KB/.trash/, .DS_Store, etc.
│                                    Policy: application UI/session state is never part of the ledger.
│
├── CHARLIE.md                       ★ THE canonical operating document (invariant I6).
├── REFERENCE.md                     This file: descriptive snapshot.
├── PROVENANCE.md                    Build record (replaces the original migration documents).
│
├── profile.md                       Pinned. Stable profile of Jonah + Charlie.
├── Active Context.md                Pinned. Live scratchpad of what is in progress NOW.
│                                    Overwritten ONLY as the final, gated step of retro.
├── action-ledger.md                 Pinned. Open commitments. Erase-free: completions MOVE to
│                                    a ## Completed section with a date stamp, never deleted.
│
├── tools/
│   ├── lint_vault.py                Schema linter. Python-3 stdlib only; zero pip dependencies
│   │                                (policy: enforcement tooling depends only on a stock dev install).
│   ├── lint.sh                      The ONLY sanctioned invocation: wraps python3 lint_vault.py,
│   │                                propagates exit code. Parser-sensitive invocation encoded once.
│   └── retro_status.py              Days-since-newest-retro helper (drives the warmup ratchet + hook).
│
├── .github/prompts/
│   ├── Charlie.agent.md             Loader/pointer → CHARLIE.md.
│   ├── warmup.prompt.md             Warmup workflow + the staleness ratchet (§7, §8).
│   ├── remember.prompt.md           Durable-capture workflow.
│   ├── retro.prompt.md              The transactional retro protocol (§7.4).
│   └── thermonuclear-code-quality-review.prompt.md   Heavy code-review mode; explicit-request only.
│
├── .claude/settings.json            ⚠ AS-BUILT advisory retro Stop hook for Claude Code.
│
├── YYYY-MM-DD/                       Daily folders, kept at root for ~14 days.
│   ├── briefing.md                  Morning plan, focus, priorities; ## End of Day appended.
│   └── logs.md                      Append-only execution journal for the day.
│
└── KB/                             ← durable memory (the knowledge store; an Obsidian vault)
    ├── .obsidian/                   Obsidian app state. Gitignored. Not memory.
    ├── Meta-Cognition.md            Process memory: how Charlie improves Charlie. Holds the
    │                                Growth Triggers (§13). type: concept; folder-law exempt.
    ├── Retrieval Strategies.md      Hub of proven lookup patterns. type: concept; folder-law exempt.
    ├── Inbox/                       Triage for unclear/unrouted notes. Schema applies; folder↔type
    │                                law exempt. Drained at retro.
    ├── Archive/                     Retired material. Notes must be status: archived.
    │   └── daily/                   Day folders moved here by retro after 14 days.
    └── Notes/                       Canonical durable notes, by type:
        ├── People/      type: person       ├── Playbooks/  type: playbook
        ├── Systems/     type: system       ├── Concepts/   type: concept
        ├── Projects/    type: project      ├── Meetings/   type: meeting
        ├── Decisions/   type: decision     └── Retro/      type: retro
```

## 4. State model

| Layer | Contents | Stability | Where it lives |
|---|---|---|---|
| **Immediate** | Current prompt, chat, tool output | Seconds–hours | Context window only |
| **Working** | Active Context, action ledger, today's briefing + logs | Hours–days | Workspace root + today's folder |
| **Durable** | Vault notes, Meta-Cognition, Retrieval Strategies | Sessions–permanent | `KB/` |

Routing: matters today → briefing/logs. Matters across sessions → vault. Changes how Charlie
operates → Meta-Cognition. Changes how Charlie searches → Retrieval Strategies. Unclear → Inbox.

## 5. Data lifecycle

**Write path:** session events → appended to `logs.md` (no in-session durability judgment) →
retro reads uncompacted logs → extracts durable facts/decisions into typed vault notes
(canonical-note-first: update in place, never duplicate) → detects supersession (old note
marked, never silently contradicted) → promotes repeatedly load-bearing material toward pinned
files → demotes/evicts pinned material over budget → git commit. Daily logs are immutable after
compaction; the distilled layer is re-derivable from them.

**Read path:** session start → pinned set (profile, Active Context, action-ledger, today's
briefing) → at most ~3 followed links → on-demand grep/read for anything else. Broad vault dumps
are prohibited.

**Cross-session signal:** compaction sees across sessions, so it can extract second-order
patterns no single session contains (recurring blockers, estimate-vs-actual drift). This is
where the system gets smarter rather than just bigger.

## 6. Vault schema (enforced by lint)

Every `.md` under `KB/` carries YAML frontmatter:

```yaml
---
type: person | system | project | decision | playbook | concept | meeting | retro
created: YYYY-MM-DD
status: active | superseded | archived
superseded_by: <vault-relative path>   # required iff status: superseded
---
```

Laws: (1) **folder↔type** — type must match the `Notes/` subfolder (Inbox/Archive exempt from
the folder law, not the schema; Archive requires status: archived; the two root hub files are
folder-law exempt and carry type: concept). (2) **Supersession** — a reversed decision or stale
fact gets `status: superseded` + `superseded_by`; it is never edited into agreement or deleted.
(3) **Retrieval convention** — synthesis must filter or explicitly flag `status != active`; a
superseded note may only be cited alongside its successor. (4) **Canonical-note-first** — update
the existing canonical note in place; creating a near-duplicate is a lint violation.

**Linter contract** (`tools/lint.sh`): walks `KB/` recursively; FAILS on missing/invalid
frontmatter, bad type/created/status, folder↔type mismatch, superseded without resolvable
superseded_by, dangling superseded_by, near-duplicate filenames. Output: one violation per line
`FILE :: RULE :: DETAIL` + summary counts (notes by type, by status, Inbox depth). Exit 0 clean,
exit 1 otherwise. Runs at every retro; may be run manually anytime.

## 7. Workflows (trigger → flow → outcome)

Summarized here; the authoritative, step-by-step versions live in `CHARLIE.md` §7 and the
`.github/prompts/` files.

- **Morning** ("good morning") → read profile + yesterday's briefing → ask priorities → create
  today's briefing + logs.
- **Warmup** ("warmup", session start) → **staleness ratchet first** (retro overdue if > 1 day
  since newest retro note) → read Active Context → ≤ 3 links → profile → open ledger → today's
  briefing.
- **Remember** ("remember this") → decide durability → route by type → canonical-note-first →
  ask if ambiguous → unclear to Inbox.
- **Retro** ("retro", session end) → transactional compaction with the retro note as a
  write-ahead log; destructive Active-Context overwrite + git commit happen last, gated on all
  prior steps. Resumable from the first unchecked box if interrupted.
- **End of day** ("wrap up") → summarize done/undone → tomorrow's priorities → `## End of Day`
  in today's briefing. Usually followed by retro.

## 8. Enforcement & integrity mechanisms

1. **Git (I1):** every overwrite is recoverable; retros are diffable
   (`git log -p "Active Context.md"` = the history of Charlie's understanding). Local-only; no
   remote. Never amend/rebase/reset-hard; rollback is `git revert`.
2. **Retro-by-default (I2):** ⚠ AS-BUILT Claude Code Stop hook in `.claude/settings.json`
   prompting retro on exit (advisory); the warmup staleness ratchet is the primary mechanism and
   applies regardless. Skips are never silent — each writes `retro deferred YYYY-MM-DD` to the
   action ledger.
3. **Lint (I3):** schema violations block a clean retro; the linter depends only on stock
   tooling (Python 3 stdlib) so enforcement survives tooling changes.
4. **Supersession (I4):** structural (frontmatter), not prose; retrieval respects it.
5. **Retro WAL (I5):** partial retros are detectable and resumable; the destructive step commits
   last.
6. **Pinned budget (I7):** warmup set ≤ 4,000 tokens (~16 KB) ⚠ AS-BUILT (Jonah-tunable). Breach
   forces eviction during that same retro.
7. **Self-observation (I8):** every retro emits the Health block; trendable over time.

## 9. The invariant contract (I1–I9)

- **I1** No destructive write is unrecoverable (git).
- **I2** Compaction is the default, not the exception (hook + ratchet; logged skips).
- **I3** Every vault note conforms to schema (lint, machine-checked).
- **I4** Superseded knowledge cannot win retrieval (status fields + convention).
- **I5** Multi-step state transitions are resumable; destructive step last (retro WAL).
- **I6** Exactly one canonical operating document (CHARLIE.md; all others are pointers).
- **I7** The pinned set is budgeted; growth forces eviction.
- **I8** The system reports its own conformance every retro (Health block).
- **I9** Deferred components have explicit, written entry triggers (§13).

**Definition of done / ongoing conformance:** the Health block passes for three consecutive
retros that fired by default, without Jonah initiating them.

## 10. Tooling reference

| Tool | Invocation | Notes |
|---|---|---|
| Vault linter | `tools/lint.sh` | Only sanctioned form; never retype the raw python line |
| Retro staleness | `python3 tools/retro_status.py` | Drives the warmup ratchet |
| Git ledger | standard git, local | Commits at every retro |
| Obsidian (app) | manual | Viewer/editor only; state dir gitignored; close during bulk moves |

Environment constraints (load-bearing): personal macOS machine; git, Python 3, and POSIX shell
present; enforcement tooling is Python-stdlib-only by policy so it survives tooling changes; git
is fully local (internal content is not published off-machine).

## 11. Operating rules (condensed)

Write: today → briefing/logs · durable → vault (canonical-first) · process change →
Meta-Cognition · search change → Retrieval Strategies · unclear → Inbox. Read: pinned set + ≤ 3
links; grep on demand; no broad dumps. Never: duplicate durable notes; silent contradictions
(use supersession); delete ledger lines; cosmetic busywork; risky/irreversible actions without
consent; pretend to access systems not actually integrated. Interaction style: concise,
proactive, explicit about limits and uncertainty.

## 12. Document hierarchy & lineage

`CHARLIE.md` (canonical, on-machine) → this reference (descriptive snapshot) → `PROVENANCE.md`
(how/when this instance was built). On the original Windows machine this chain continued into
`MIGRATION.md` / `MIGRATION-REPORT.md`; this instance was built fresh rather than migrated, so
those are intentionally absent and `PROVENANCE.md` stands in their place.

## 13. Growth triggers (verbatim policy in `KB/Meta-Cognition.md` — invariant I9)

| Component (deferred) | Build when… | Form |
|---|---|---|
| FTS5/SQLite derived index | grep returns too many hits to rank by eye on two occasions, OR vault > ~150 notes | Single SQLite file; index derived from Markdown; rebuildable |
| Weekly rollup tier | Monday warmup (3 briefings) breaches the pinned budget twice | Sunday compaction → `KB/Notes/Retro/YYYY-Www weekly.md` |
| Structured task state | action ledger > ~30 open items, or dependencies stop fitting a flat list, twice | Separate table/file from knowledge memory (different retention semantics) |
| Embeddings / semantic search | keyword search misses a known-existing note via vocabulary drift, twice | Local embedding model; index remains derived/disposable |

Each firing is recorded in a retro before the component is built. Until a trigger fires, absence
is correct — the governing rule: **a component earns its place when the failure mode it prevents
has occurred twice.**

## 14. Failure modes & recovery

| Failure | Recovery |
|---|---|
| Bad retro mangled Active Context | `git revert` / restore from previous `retro:` commit |
| Retro interrupted mid-run | Open the retro note WAL; resume at first unchecked box |
| Vault note corrupted/duplicated | Lint detects; fix at retro; history in git |
| Distilled layer doubted wholesale | Re-derive from daily logs (immutable after compaction) |
| Linter/tooling lost | Re-create from spec in CHARLIE.md; only stock-tooling dependencies |
| Drift between docs | CHARLIE.md wins (I6); others are pointers by construction |

## 15. Success criteria

Sessions start fast without broad re-reading · durable notes stay clean, typed, and
non-duplicative · today's work stays in daily files · repeated patterns get promoted, stale
pinned material gets evicted · superseded knowledge is visible as such · the Health trend is
green without human prompting · a fresh instance can recover the full operating model from files
alone — this document plus `CHARLIE.md` being the proof.
