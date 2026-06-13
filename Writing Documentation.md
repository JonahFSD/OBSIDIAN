---
description: Heuristics for writing good documentation, with an AI-age lens. Each entry — heuristic → failure it prevents → confidence → source. Unifying rule — minimize what the reader (human or agent) must process to act, and keep it from drifting.
---
# Writing Documentation

Heuristics for writing good documentation. Unifying rule: *minimize what the reader (human or
agent) must process to act correctly, and keep it from drifting from reality.* Each entry:
heuristic → the failure it prevents → (confidence) → source.

1. **Sort each page into one Diátaxis mode — tutorial / how-to / reference / explanation — and
   don't mix.** Prevents a page that teaches, instructs, describes, and explains at once and serves
   none. (high) — [Diátaxis](https://diataxis.fr/start-here/)
2. **Organize around the reader's task, not the system's structure** (reference is the deliberate
   exception). Prevents docs that force you to understand the architecture before you can find
   anything. (high) — [Google developer-docs style](https://developers.google.com/style/highlights)
3. **Stale docs are worse than none — keep a small, fresh set and trim aggressively ("bonsai").**
   Prevents actively misleading readers who trust docs as the source of truth. (high) —
   [Adopting minimalism in your docs](https://opensource.com/article/17/10/adopting-minimalism-your-docs)
4. **Keep docs in-repo and change them in the same PR as the code (docs-as-code).** Prevents
   drift — the root cause of staleness. (high) — [What is Docs as Code](https://konghq.com/blog/learning-center/what-is-docs-as-code)
5. **Make examples runnable and test them in CI (doctests).** Prevents examples silently rotting
   after a refactor until a user copies a broken one. (high) — [Python doctest](https://docs.python.org/3/library/doctest.html)
6. **Lead API/reference docs with worked usage examples.** Prevents the #1 developer obstacle
   (signatures with no data types / formats / request bodies); examples measurably cut mistakes.
   (med-high) — [Effectiveness of Usage Examples in REST API docs](https://homepages.ecs.vuw.ac.nz/~craig/publications/vlhcc2017-sohan.pdf)
7. **Comments explain WHY, not WHAT — and prefer self-explanatory code, because comments drift.**
   Prevents redundant noise and lost rationale; code-comment inconsistency is pervasive. (med) —
   [Code Tells You How, Comments Tell You Why](https://blog.codinghorror.com/code-tells-you-how-comments-tell-you-why/)
8. **Record significant decisions as short decision notes (context / decision / consequences).**
   Prevents future engineers unknowingly defeating earlier decisions for lack of rationale.
   (med-high) — [Documenting Architecture Decisions (Nygard)](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
9. **A README is an orientation map (what / run / contribute / license), not a manual — push depth
   elsewhere.** Prevents both too-thin (can't start) and too-bloated (unread). (med) —
   [Make a README](https://www.makeareadme.com/)
10. **Lint prose and check links in CI.** Prevents broken links and style drift accumulating
    unnoticed. (med) — [Docs-as-code best practices](https://hyperlint.com/blog/5-critical-documentation-best-practices-for-docs-as-code/)
11. **Agent context files (AGENTS.md/CLAUDE.md): only non-inferable conventions; skip directory
    maps.** Prevents context bloat — a controlled study found LLM-generated context files *lowered*
    task success ~2–3% and raised cost >20%; human-written ones helped only ~4%. (med) —
    [Evaluating AGENTS.md (arXiv 2602.11988)](https://arxiv.org/pdf/2602.11988v1)
12. **Optimize agent-facing docs for signal density, not volume — more context degrades accuracy
    ("context rot").** Prevents stuffing the window with whole doc sets the model must search.
    (med-high) — [Context rot](https://redis.io/blog/context-rot/)

---
## Related
[[Invariants]] · [[Good Code in the AI Age]] · [[Code Conventions]] · [[TypeScript Development]]
