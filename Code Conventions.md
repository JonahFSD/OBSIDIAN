---
description: Conventions hub — Conventional Commits and per-language coding standards; links the principle and practice notes.
---
# Code Conventions

Hub for durable coding conventions and language/framework best-practice references. Each language
or stack gets its own note, linked from here, so they cluster together in the graph.

## Principles
- [[Good Code in the AI Age]] — durable LLM failure modes (the "why") + caveats.
- [[Invariants]] — the coding invariants that follow.

## Practices
- [[Writing Tests]] — test-writing heuristics.
- [[Writing Documentation]] — documentation heuristics.
- [[Deterministic Gates]] — the enforcement tooling behind the rules; wire it into a repo.

## Languages & stacks
- [[TypeScript Development]] — type system, generics, utility types, type guards, React/Node patterns, `tsconfig`, strict mode.
- [[Convex Conventions]] — validators as the boundary, query/mutation/action model, OCC as the ledger pattern, convex-test, HIPAA/BAA.
- [[React Native & Expo Security]] — Maestro/Detox testing, New Architecture/Hermes, OWASP Mobile Top 10 + MASVS, SecureStore, HIPAA for a PHI app.

## Agents & security
- [[Agent Eval & Injection Defense]] — eval-harness discipline, prompt-injection design patterns + CaMeL, GenAI tracing, slopsquatting defense, OWASP LLM/Agentic.

<!-- Add more convention notes here (e.g. Python, Go, CSS) and link them above. -->
