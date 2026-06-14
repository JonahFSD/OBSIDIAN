---
description: How to write Convex backends well — validators as the trust boundary, the query/mutation/action model, OCC + determinism as the canonical ledger-pattern example, convex-test, write-conflict avoidance, and HIPAA. Stack-specific companion to [[Invariants]] and [[Deterministic Gates]]; Convex collapses the typed-seam problem (Drizzle/Prisma + tRPC + Zod) into one end-to-end-typed system.
---
# Convex Conventions

Facts tagged **[V]** = verified against Convex docs / primary sources (2026-06-14); **[R]** = reported / single-source / directional.

Convex replaces the multi-tool typed seam (Drizzle/Prisma + tRPC + Zod) with one end-to-end-typed system. The generated `api` object and `Doc`/`Id` types from `convex/_generated/dataModel` **are** the seam — you don't assemble it. The [[TypeScript Development]] "type the seams" rule still holds; the mechanism differs.

## Validators are the boundary (parse-don't-validate, Convex style)
- Every public `query`/`mutation`/`action` needs `args` validators (and ideally `returns`) built with `v.*`. Public functions can be called by anyone, including attackers — arg validators are the [[Invariants]] #2 "verify outside the model" boundary. **[V]**
- Enforce in CI (out of beta): `@convex-dev/require-argument-validators` (every function validated) and `@convex-dev/no-filter-in-query` (prefer `.withIndex` over `.filter` on large scans). **[V]** → these belong in [[Deterministic Gates]].
- `Infer<typeof validator>` derives the TS type from the validator — one source, no drift. **[V]**
- Reach for Zod only for refinements `v.*` can't express (`.email()`, branded/refined types) via `convex-helpers/server/zod` (`zCustomQuery`/`zCustomMutation`, `zid()`, `zodToConvex`/`zodOutputToConvex`); convex-helpers supports Zod 4. For data at rest, prefer `v.*` and trust server code to write valid data; reserve Zod for arguments and refined read-side assertions. Trap: `zodOutputToConvex` (output shape) vs `zodToConvex` (input shape) — pick by whether you validate before insert. **[V]/[R]**

## The query / mutation / action model (the load-bearing mental model)
- **Query** — read-only, deterministic, reactive (drives subscriptions). **[V]**
- **Mutation** — transactional read+write, deterministic, atomic, **no external I/O**. **[V]**
- **Action** — may call third-party APIs / do nondeterministic work, **not transactional**; calls mutations/queries via `ctx.runMutation`/`ctx.runQuery`. **[V]**
- Discipline that mirrors the planner→executor loop: side effects live in **actions**, state transitions live in validated **mutations**; an action never "guesses" a write it should delegate to a mutation. Same shape as [[Spec-Driven Build Loop]]'s build step.

## OCC + determinism = the ledger pattern (canonical worked example)
Convex is ACID with **serializable isolation and optimistic concurrency control**, giving "true serializability … regardless of what transactions are issued concurrently" — not mere snapshot isolation. **[V]** Because mutations are **deterministic**, a read-set/write-set conflict is resolved by simply **re-running** the transaction until it commits cleanly — determinism is what guarantees there is never a "merge conflict." Convex's own analogy: a conflict means "HEAD is out of date, so we need to rebase … this rebase will always eventually succeed." **[V]**

Underneath: a replicated transaction log + read/write-set conflict detection at commit timestamps = an append-only log of committed transactions with derived, reactive query projections. **That is the ledger pattern exactly** — immutable append-only history as the source of truth + disposable derived projections — the same shape as git, event sourcing, and LSM trees. Determinism is the non-negotiable that makes the retry/rebase safe, which is *why* mutations may not call third-party APIs.

Corollary — **design to avoid write conflicts**: never read a whole table in a mutation that conflicts with every insert; use precise `.withIndex` reads, the sharded-counter pattern for hot counters, and a Workpool for queued async work; avoid prefix-redundant indexes. **[V]/[R]**

## Testing — `convex-test`
- A pure-JS **mock** of the backend, run via Vitest: `convexTest(schema)` → `t.query` / `t.mutation` / `t.action` / `t.run`. **[V]**
- It's a mock, not the real backend ("doesn't have many of the behaviors of the real Convex backend") — don't assert on error-message text. **[V]**
- Pass the schema (for validation + correct `t.run` typing). The `import.meta.glob` setup is mandatory and non-obvious — document it once in a shared test helper. **[V]/[R]**
- Test scheduled functions / crons with Vitest fake timers + `t.finishInProgressScheduledFunctions` / `t.finishAllScheduledFunctions` — there is no SQL-stack analog. **[V]**
- Higher fidelity: run the open-source local backend in CI; Convex Pro gives per-PR preview deployments. Coverage is a floor, not a target ([[Writing Tests]] #5; Convex's own testing post says the same). **[V]/[R]**

## HIPAA (PHI apps)
- Convex is **SOC 2 Type II** and **HIPAA-compliant with a signed BAA** — verbatim: "Provided businesses subject to HIPAA sign Convex's Business Associate Agreement they may process PHI on the platform." 256-bit AES at rest, TLS in transit, hosted on AWS (HIPAA-eligible). **[V]** (primary: convex.dev/security)
- Gate before real PHI: sign Convex's BAA **and** a BAA with every other vendor touching PHI (transcription, LLM/summarization — confirm a zero-retention path). No real PHI in the system until all BAAs are signed. Device side → [[React Native & Expo Security]]; chatbot side → [[Agent Eval & Injection Defense]].
- Name collision: **convex.dev** (this backend) ≠ convex.com (an unrelated firm). HIPAA facts here are sourced to convex.dev only.

## Sources
- [Argument/Return Validation](https://docs.convex.dev/functions/validation) · [ESLint rules](https://docs.convex.dev/eslint) · [OCC and Atomicity](https://docs.convex.dev/database/advanced/occ) · [convex-test](https://docs.convex.dev/testing/convex-test) · [Best Practices](https://docs.convex.dev/understanding/best-practices/)
- [Types & Validators cookbook](https://stack.convex.dev/types-cookbook) · [How Convex Works](https://stack.convex.dev/how-convex-works)
- [Convex Platform Security — HIPAA/SOC 2/BAA](https://www.convex.dev/security)

---
## Related
[[Invariants]] · [[Deterministic Gates]] · [[Spec-Driven Build Loop]] · [[Writing Tests]] · [[TypeScript Development]] · [[React Native & Expo Security]] · [[Agent Eval & Injection Defense]]
