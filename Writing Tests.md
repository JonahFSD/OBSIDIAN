---
type: concept
created: 2026-06-13
status: active
description: Heuristics for writing good tests, with an AI-age lens. Each entry — heuristic → failure it prevents → confidence → source. Tests are the agent's main external verification signal; see [[Invariants]] #2 and #9.
---
# Writing Tests

Heuristics for writing good tests. Tests are the agent's main *external verification signal*
([[Invariants]] #2), so a weak test doesn't just miss bugs — it certifies (and, in RL training,
rewards) broken code. Each entry: heuristic → the failure it prevents → (confidence) → source.

1. **Test observable behavior through the public API, not implementation.** Prevents brittle tests
   that break on a pure refactor and train people to fear refactoring. (high) —
   [Test Behavior, Not Implementation (Google)](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html)
2. **One behavior per test; arrange–act–assert; no control flow in test bodies.** Prevents
   "assertion roulette" and bugs hiding *in the test itself* — the most common defect in
   machine-generated tests. (high) — [SWE at Google: Testing](https://abseil.io/resources/swe-book/html/ch11.html)
3. **Small, fast, hermetic — no network / disk / shared DB / `sleep()`.** Prevents slow suites that
   get run less often and order-dependent flakes; it's also the precondition for an agent
   re-running the suite as a verification loop. (high) — [SWE at Google: Testing](https://abseil.io/resources/swe-book/html/ch11.html)
4. **A flaky test is worse than no test — fix or quarantine it; don't normalize reruns.** Prevents
   "cry-wolf" collapse (Google: ~84% of pass→fail transitions are flakes), which trains everyone
   to ignore failures. (high) — [Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)
5. **Coverage is a floor and a "what's untested?" signal — never a target; don't chase 100%.**
   Prevents Goodhart gaming (assertion-free tests that execute lines without checking) and brittle
   effort on the last 10–20%. (high) — [Write tests. Not too many. Mostly integration. (Dodds)](https://kentcdodds.com/blog/write-tests)
6. **Prefer real dependencies; use test doubles only at genuine seams (network, payments, clock).**
   Prevents over-mocking that couples to *how* collaborators are called, passing while the
   integration is actually broken. (high) — [Mocks Aren't Stubs (Fowler)](https://martinfowler.com/articles/mocksArentStubs.html)
7. **Weight toward integration tests; treat exact pyramid/trophy ratios as context, not law.**
   Prevents the "ice-cream cone" (all slow E2E) and "hourglass" (no integration) shapes. (med) —
   [Write tests. Not too many. Mostly integration. (Dodds)](https://kentcdodds.com/blog/write-tests)
8. **Be deliberate about which behaviors you promise to keep — "if you liked it, put a test on it."**
   Prevents silent regressions and over-pinning incidental behavior (Hyrum's Law). (med-high) —
   [SWE at Google: Testing](https://abseil.io/resources/swe-book/html/ch11.html) · [Hyrum's Law](https://www.hyrumslaw.com/)
9. **Use property-based / metamorphic tests where invariants are clear but an exact oracle is hard.**
   Prevents example-only blind spots. Caveat: finding good properties is the hard part. (med) —
   [Property Tests + Contracts (Hillel Wayne)](https://www.hillelwayne.com/pbt-contracts/)
10. **Mutation testing tests your tests — but filter to productive mutants and run on changed lines.**
    Prevents false security from high coverage paired with weak assertions. (med) —
    [Mutation Testing at Google](https://research.google.com/pubs/archive/46584.pdf)
11. **TDD is a useful design discipline, not an evidence-backed mandate.** Prevents over-selling —
    controlled studies on test-first ordering are inconclusive. (med) —
    [Why TDD research is inconclusive](https://arxiv.org/pdf/2007.09863)
12. **Humans own the oracle; treat agent-written tests as unverified until reviewed.** Prevents the
    agent-age failure where a wrong test certifies/rewards broken code (RLVR reward-hacking). Let
    agents draft scaffolding and inputs; a human asserts intended behavior. (med-high) —
    [LLMs Gaming Verifiers](https://arxiv.org/abs/2604.15149) · [Test smells in LLM-generated tests](https://arxiv.org/abs/2410.10628)

---
## Related
[[Invariants]] · [[Good Code in the AI Age]] · [[Code Conventions]]
