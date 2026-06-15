---
description: The named methodologies behind [[Deterministic Gates]] — the established vocabulary for "constrain a stochastic model with deterministic structure." The deterministic-harness instinct isn't novel; it's the LLM-era reinvention of high-integrity software engineering. Use these names to search prior art. Theory companion to [[Good Code in the AI Age]]; enforcement lives in [[Deterministic Gates]].
---
# Deterministic Methodology

Facts tagged **[V]** = verified against primary sources (2026-06-14).

The instinct — the model is stochastic, so make the *boundary* deterministic (stochastic cell, deterministic membrane) — has a 30-year lineage. Naming it lets you stand on existing work instead of re-deriving it. Umbrella: **neurosymbolic**; the software-engineering methodology: **Correctness by Construction** + **Design by Contract**.

## The lineage, by layer
- **Neurosymbolic AI** — the umbrella: a stochastic neural core wrapped by a symbolic layer of deterministic rules enforced *outside* the model. This is "stochastic cell, deterministic membrane" in the literature. **[V]**
- **Correctness by Construction (CbC)** — high-integrity SE (Praxis/Altran, SPARK/Ada). Use methods that make whole error classes *impossible to introduce*, rather than testing them out afterward. = the "prefer impossibility to detection" rung of [[Spec-Driven Build Loop]]. **[V]**
- **Design by Contract (DbC)** — Bertrand Meyer (Eiffel). Pre/postconditions + invariants as binding obligations at every component boundary. = "contracts at the seams." LLM bridge: Agent Behavioral Contracts (arXiv 2602.22302); SymbolicAI's DbC contract layer (arXiv 2508.03665). **[V]**
- **Make illegal states unrepresentable / Parse, don't validate** — Yaron Minsky / Alexis King. Encode invariants in types; parse untrusted input at the boundary into a type that can't represent an invalid value. = by-construction at the type level ([[Invariants]] #4). **[V]**
- **Workflows vs Agents** — Anthropic, *Building Effective Agents*. Orchestrate through predefined deterministic code paths; call the model only at the decision points you chose. = the planner-executor split. **[V]**
- **Constrained decoding / structured generation** — logit-masking so invalid tokens are unemittable (100% schema compliance). = illegal states made unrepresentable at *generation* time. **[V]**
- **Flow engineering** — AlphaCodium (Qodo). A deterministic, test-anchored loop *around* the model beats a smarter prompt or model. = iterate-until-green. **[V]**

**One sentence:** the harness = CbC/DbC discipline enforced by a neurosymbolic membrane, with constrained decoding at the output and flow engineering in the loop. Not novel — that's the good news; these terms are the search keys for prior art.

## Prior-art tools (2026-06 snapshot — for searching, not a maintained list; expect rot)
No single repo does it all; it's three layers (see [[Deterministic Gates]]). By layer:
- **Contracts / typed boundaries:** BAML (typed LLM functions, TS + Python), DSPy assertions, SymbolicAI (DbC), Instructor / Guardrails AI.
- **Constrained decoding:** Outlines, XGrammar (default backend in vLLM/SGLang), llguidance.
- **Verified codegen:** Clover (consistency-checks code ↔ doc ↔ spec via Dafny; zero false positives).
- **Runtime enforcement:** AgentSpec (trigger→predicate→enforcement DSL), Invariant (trace-relational rules, MCP proxy — see [[Agent Eval & Injection Defense]]).
- **Orchestration:** LangGraph (state graph), Temporal (durable execution; LLM quarantined as an activity).
- **CLI-agent harness:** Anthropic sandbox-runtime / `/sandbox`, container-use (isolated container per agent), TDD-Guard (blocks code before a failing test exists).

## Sources
- [Correctness by Construction (Chapman)](https://samate.nist.gov/SSATTM_Content/papers/Correctness%20by%20Construction%20-%20Chapman.pdf) · [Agent Behavioral Contracts (arXiv 2602.22302)](https://arxiv.org/abs/2602.22302) · [Parse, Don't Validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)
- [Building Effective Agents (Anthropic)](https://www.anthropic.com/research/building-effective-agents) · [Grammar-Aligned Decoding (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/2bdc2267c3d7d01523e2e17ac0a754f3-Paper-Conference.pdf) · [AlphaCodium (arXiv 2401.08500)](https://arxiv.org/abs/2401.08500)
- [CaMeL (arXiv 2503.18813)](https://arxiv.org/abs/2503.18813) · [Clover (arXiv 2310.17807)](https://arxiv.org/abs/2310.17807) · [AgentSpec (arXiv 2503.18666)](https://arxiv.org/abs/2503.18666)

---
## Related
[[Deterministic Gates]] · [[Spec-Driven Build Loop]] · [[Good Code in the AI Age]] · [[Invariants]] · [[Agent Eval & Injection Defense]]
