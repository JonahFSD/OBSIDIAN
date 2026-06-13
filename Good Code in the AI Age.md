---
type: concept
created: 2026-06-12
status: active
description: Global invariants for writing good code in the AI age — practices that earn their weight because they counter durable LLM failure modes and raise the signal density of a limited, attention-imperfect context window. Grounded in primary research.
---
# Good Code in the AI Age

**Thesis.** Treat code and everything around it (commits, types, tests, docs, structure) as a
**high-signal, low-noise context for a forgetful, attention-limited, easily-distracted,
non-persistent reader that cannot reliably check its own work.** A practice **earns its weight**
if and only if it either (a) raises signal density / lowers noise in a finite context, or
(b) produces an **external, deterministic, machine-readable verification signal the model cannot
fake.** Everything below is justified by failure modes that trace to the architecture or training
of LLMs — so they're durable across model versions, not prompt hacks. A practice earns its weight
only when it pays for the context it costs.

## The durable failure modes (the "always true" substrate)

- **Finite, decaying attention.** Effective context is a *fraction* of the advertised window;
  accuracy sags for tokens in the middle ("lost in the middle") and degrades as length grows
  ("context rot") — even on trivial tasks. Mechanistic: softmax attention mass must sum to 1, so
  every added token bleeds attention off the relevant ones.
- **Irrelevant/contradictory context actively degrades reasoning** — not just dilution. A single
  distractor measurably lowers accuracy; distractors compound.
- **Stale parametric knowledge.** Training cutoff is frozen, so models hallucinate non-existent
  packages (persistently and reproducibly — hence exploitable) and emit deprecated APIs.
- **Cannot reliably self-verify.** Models show low self-awareness of their own errors and ship
  confident-but-wrong changes; ~30% of "passing" SWE-bench patches differ from the human fix.
- **Sycophancy.** RLHF makes models favor agreeing with the user over being correct.
- **Premature convergence.** Agents lock onto the first plausible approach and under-explore.
- **Statelessness.** No memory persists across sessions; context must be re-loaded every time.

## The invariants

1. **Make the context smaller and denser than feels necessary.** *Counters:* finite attention,
   context rot. *Why always true:* attention is a fixed budget; effective << advertised. *Cost/
   payoff:* costs editorial discipline; large payoff — omission is a feature, not a loss.
2. **Put verification outside the model.** Types, a pre-existing human test suite, static
   analysis, a reproducible build — signals it can't fake. *Counters:* no self-verification.
   *Why:* the model can't introspect correctness but *can* react to a concrete failure report.
   *Payoff:* the single highest-evidence lever here.
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
   no intent; small, typed, machine-parseable history is bisectable and revertible. The entry
   point for this whole topic — see [[Code Conventions]].
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
   regression run and a behavioral check before trusting a fix.

## Skeptic's corner (don't oversell)

- The exact *shape/magnitude* of "lost in the middle" is contested and benchmark-dependent; the
  **direction** (length and middle-position hurt) is robust. Treat "X% drop at position N" as
  model-specific, not a constant.
- **Agent-*written* tests are weak verification** — used as print-style observation, not real
  oracles. The lift in invariant 2 comes from *pre-existing human tests as a target*, not from an
  agent inventing its own. "Agents should just TDD themselves" is partly hype.
- **Docstrings help only ~1–3%** in controlled studies — write them for humans/intent, don't
  expect magic for agent correctness.
- "AI is degrading code quality" macro stats are vendor analyses, not peer-reviewed — low confidence.

## Sources

- [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Lost in the Middle (Liu et al., TACL 2024)](https://arxiv.org/abs/2307.03172)
- [Context Rot (Chroma, 2025)](https://research.trychroma.com/context-rot)
- [NoLiMa: long-context beyond literal matching (ICML 2025)](https://arxiv.org/abs/2502.05167) · [RULER (2024)](https://arxiv.org/abs/2404.06654)
- [LLMs Can Be Easily Distracted by Irrelevant Context (Shi et al., ICML 2023)](https://arxiv.org/abs/2302.00093)
- [Towards Understanding Sycophancy in LMs (Anthropic)](https://arxiv.org/abs/2310.13548)
- [We Have a Package for You! — package hallucination (USENIX Security 2025)](https://arxiv.org/abs/2406.10279)
- [LLMs Meet Library Evolution — deprecated APIs (ICSE 2025)](https://arxiv.org/abs/2406.09834)
- [Are "Solved Issues" in SWE-bench Really Solved Correctly? (2025)](https://arxiv.org/abs/2503.15223)
- [Type-Constrained Code Generation (2025)](https://arxiv.org/abs/2504.09246) · [To Type or Not to Type (Gao, Bird, Barr)](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/09/gao2017javascript.pdf)
- [Code Review at Cisco / SmartBear (diff-size vs defect detection)](https://static0.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Claude Code best practices](https://code.claude.com/docs/en/best-practices)

---
## Related
[[Code Conventions]] · [[TypeScript Development]]
