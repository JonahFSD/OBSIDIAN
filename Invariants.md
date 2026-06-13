---
type: concept
created: 2026-06-12
status: active
description: Append-only ledger of code invariants for the AI age — each grounded in a durable LLM failure mode. See [[Good Code in the AI Age]] for the failure-mode substrate and the caveats.
---
# Invariants

Append-only ledger of durable coding invariants. Each earns its place by countering a structural
LLM failure mode (substrate + sources live in [[Good Code in the AI Age]]). **Append new entries;
supersede — don't overwrite or delete.** Each entry: what it counters → why it's always true →
context cost vs. payoff.

## Active

1. **Make the context smaller and denser than feels necessary.** *Counters:* finite attention,
   context rot. *Why always true:* attention is a fixed budget; effective << advertised. *Cost/
   payoff:* costs editorial discipline; large payoff — omission is a feature, not a loss.
2. **Put verification outside the model.** Types, a pre-existing human test suite, static
   analysis, a reproducible build — signals it can't fake. *Counters:* no self-verification.
   *Why:* the model can't introspect correctness but *can* react to a concrete failure report.
   *Payoff:* the single highest-evidence lever here. See [[Writing Tests]].
3. **Treat recalled facts as low-trust hypotheses; check them against ground truth.** Pin
   versions, load current docs, confirm a package exists before importing. *Counters:* stale
   knowledge / hallucinated APIs. *Why:* knowledge is frozen at cutoff; re-prompting repeats the
   same hallucination rather than fixing it.
4. **Make types explicit.** *Counters:* silent interface mismatches, hallucinated signatures.
   *Why:* the type checker is the dominant error gate (~94% of compile errors are type errors) and
   catches ~15% of would-be-shipped bugs — a high-value first filter, never a correctness proof
   (logic bugs type-check). See [[TypeScript Development]].
5. **Keep history legible and append-only.** Conventional Commits + **small atomic diffs** + the
   *why* in the message (the diff already shows the *what*). *Counters:* weak localization,
   unreviewable change. *Why:* human defect-detection collapses past ~400 LOC, and a diff carries
   no intent; small, typed, machine-parseable history is bisectable and revertible. See
   [[Code Conventions]].
6. **Optimize for localizability.** Navigable, grep-able, consistently-organized code with
   intention-revealing names. *Counters:* finite attention + editing-the-wrong-thing. *Why:*
   fault-localization precision measurably gates agent repair success; agents navigate by
   grep/tree/symbol tools, and names are a comprehension input (the model reads code as text).
7. **A rules/convention artifact earns its place only if omitting it would cause a mistake.**
   Prune ruthlessly. *Counters:* context rot, irrelevant-context degradation. *Why:* a bloated
   always-loaded rules file (CLAUDE.md/AGENTS.md) makes the model ignore the rules that matter —
   the important ones drown in noise. The convention must pay rent in prevented errors.
8. **Persist memory in durable external files; re-load at session start.** *Counters:*
   statelessness. *Why:* a fresh session knows nothing it wasn't re-told; persist decisions,
   conventions, and gotchas in durable files and re-load them rather than re-deriving context.
9. **Don't trust agreement; force the counter-case, and verify behavior not proximity.**
   *Counters:* sycophancy + premature convergence + false "done." *Why:* agreement is the
   predicted failure, not a signal; "tests near the diff pass" ≠ correct — require a full
   regression run and a behavioral check before trusting a fix. See [[Writing Tests]].

## Superseded

_(none yet — when an invariant is reversed, move it here with a one-line pointer to its replacement.)_

---
## Related
[[Good Code in the AI Age]] · [[Code Conventions]] · [[Writing Tests]] · [[Writing Documentation]]
