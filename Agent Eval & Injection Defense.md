---
description: The disciplines a planner-executor loop and a tool-using chatbot need beyond OWASP bullet points — evals as a first-class test suite, prompt-injection defense by architecture (not filters), GenAI tracing, and AI supply-chain (slopsquatting). Companion to [[Spec-Driven Build Loop]] and [[Deterministic Gates]]; this is the runtime/agent half of the harness.
---
# Agent Eval & Injection Defense

Facts tagged **[V]** = verified against primary sources (2026-06-14); **[R]** = reported / single-source / directional.

## Evals are a first-class test suite
You cannot ship a nondeterministic system without one. Treat prompts/agents like code with a test suite.

- **Tools:** promptfoo (MIT; acquired by OpenAI **9 Mar 2026**, remains open source) — declarative `promptfooconfig.yaml`, deterministic asserts (`contains`/`is-json`/regex/latency/JS) + model-graded (`llm-rubric`/`g-eval`/`factuality`), red-teaming, GitHub Action. Inspect (UK AISI, MIT; `dataset → Task → Solver → Scorer`, sandboxed). Also Braintrust, LangSmith, OpenAI Evals, DeepEval. **[V]**
- **LLM-as-judge pitfalls:** judges have biases, add latency, can be gamed; delimiters like `<output>` help but "are not a security boundary." Never judge-only — it stacks scorer stochasticity on top of the agent's. **[R]**
- **Discipline (the eval form of "agent drafts, human owns the oracle"):** target mix ≈ **60% deterministic / 30% LLM-judge / 10% human**; **baseline the current agent on a golden set before setting bars**; **block-on-regression, not block-on-absolute-threshold**; run on every PR touching prompts/agent code and fail the merge on regression. **[R]** → wire into the [[Spec-Driven Build Loop]] / [[Deterministic Gates]] gate suite.

## Prompt injection: defend by architecture, not filters
- **The exfiltration pattern to internalize:** untrusted content (a fetched page, a doctor-visit transcript, a GitHub issue) carries a hidden instruction; an agent holding both the injected instruction and a privileged tool + an exfiltration sink leaks data. Invariant Labs (now Snyk) demonstrated this via the GitHub MCP exploit and tool-poisoning (malicious instructions hidden in a tool's description). Willison: any agent that can render a markdown link/image or fetch a URL has a candidate exfiltration path. Defensive lens: **toxic-flow analysis** — flag any sequence combining untrusted input + private data + a sink. **[V]/[R]**
- **The six design patterns** (Beurer-Kellner, Fischer, Tramèr et al.; arXiv **2506.08837**, Jun 2025; code samples by ReversecLabs), in increasing permissiveness. Guiding principle, verbatim: "once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible for that input to trigger any consequential actions." **[V]**
  1. **Action-Selector** — agent picks from predefined tool calls; no tool feedback returns to it. Immune by construction.
  2. **Plan-Then-Execute** — fix the plan before touching untrusted data; tool outputs can't change the chosen actions (control-flow integrity). **This is your planner-executor split.**
  3. **LLM Map-Reduce** — isolated per-document agents feed a reduce step.
  4. **Dual LLM** (Willison) — a privileged LLM plans and uses tools but never sees untrusted content; a quarantined LLM processes untrusted text but has no tools, returning opaque variables a non-LLM substrate substitutes.
  5. **Code-Then-Execute** — agent emits a program (sandboxed DSL) enabling dataflow analysis (CaMeL is an instance).
  6. **Context-Minimization** — drop the untrusted prompt from context after it has selected the action.
- **CaMeL** (Google DeepMind, "Defeating Prompt Injections by Design," arXiv **2503.18813**): extracts control/data flow from the trusted query so untrusted data "can never impact the program flow," plus per-value capabilities enforced at tool-call time (CFI + IFC). Cite by version: v1 (Mar 2025) = 67% of tasks with provable security; v2 (24 Jun 2025) = **77% with provable security vs 84% for an undefended system** in AgentDojo. **[V]**
- **Guardrail frameworks** (NeMo Guardrails, Guardrails AI, Llama Guard, Invariant) are a **first line only**: "classifier-based detectors can never be trusted to be 100% accurate"; adaptive attacks and simple obfuscation (Base64/Unicode) bypass filters. Architecture (data-flow control + least-privilege tools + sandboxing) beats detection — the strongest, best-supported position. **[R]**
- **For a citation-grounded chatbot:** treat transcripts/retrieved docs as untrusted → Plan-Then-Execute + a quarantined summarizer + a deterministic gate between model output and any privileged action (no tool may email, delete, or fetch arbitrary URLs based on transcript content). This is [[Deterministic Gates]] as the agent's leash, grounded in the literature.

## Tracing / observability
Converge on **OpenTelemetry GenAI semantic conventions** (`gen_ai.*`); still **Development/experimental** status (May 2026) — pin `OTEL_SEMCONV_STABILITY_OPT_IN` and treat dashboards as versioned infra. Span naming `{operation} {name}` (e.g., `chat gpt-5`, `execute_tool web_search`); wrap the top-level call in `invoke_agent`, each tool call in `execute_tool`. **[V]** Backends: Langfuse (OSS, self-host, pairs tracing with prompt versioning — best for "which prompt version regressed?"), Phoenix/Arize, Helicone (proxy). For sensitive paths, use privacy-mode (disable prompt-body capture). **[R]**

## AI supply chain — slopsquatting
- "We Have a Package for You!" (USENIX Security 2025, arXiv **2406.10279**; UTSA / Oklahoma / Virginia Tech): across 576k generated programs (~2.23M package references), **19.7% of references were hallucinated**, yielding **205,474 unique** fake names; **43% repeated across all 10 identical runs** (predictable → weaponizable); 38% conflations (`express-mongoose`), 13% typos, 51% pure fabrications. Term "slopsquatting" coined by Seth Larson. Real PoC: Lanyado's empty `huggingface-cli` got ~30k downloads in 3 months (Alibaba's GraphTranslator README had recommended it). **[V]**
- **Layered defense** (no single tool suffices): (1) commit lockfiles + `--frozen-lockfile` / `npm ci` so unknown == fail-closed; (2) package allowlist + first-seen-dependency CI gate requiring human sign-off; (3) Socket.dev / Snyk / OSV registry verification (exists, registered before your project, established publisher); (4) a `CLAUDE.md` rule forbidding the agent from installing unverified packages; (5) SBOM (CycloneDX) + signed provenance (SLSA). → [[Deterministic Gates]]. **[R]**

## Frameworks to track
- **OWASP Top 10 for LLM Apps 2025** — LLM01 Prompt Injection still #1; new LLM07 System Prompt Leakage, LLM08 Vector/Embedding Weaknesses. **[V]**
- **OWASP Top 10 for Agentic Applications (2026)** — for the planner-executor loop (goal hijacking, tool misuse, rogue agents, insecure inter-agent comms). Note: name/date is "Agentic Applications **2026**," not "Agentic AI Top 10 2025." **[V]**

## Sources
- [Design Patterns for Securing LLM Agents (arXiv 2506.08837)](https://arxiv.org/abs/2506.08837) · [code samples (ReversecLabs)](https://github.com/ReversecLabs/design-patterns-for-securing-llm-agents-code-samples)
- [CaMeL — Defeating Prompt Injections by Design (arXiv 2503.18813)](https://arxiv.org/abs/2503.18813)
- [We Have a Package for You! — slopsquatting (arXiv 2406.10279)](https://arxiv.org/abs/2406.10279)
- [promptfoo](https://www.promptfoo.dev/) · [Inspect (UK AISI)](https://inspect.aisi.org.uk/) · [OTel GenAI spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/)
- [OWASP Top 10 for LLM Apps](https://genai.owasp.org/llm-top-10/) · [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

---
## Related
[[Spec-Driven Build Loop]] · [[Deterministic Gates]] · [[Invariants]] · [[Writing Tests]] · [[Convex Conventions]] · [[React Native & Expo Security]]
