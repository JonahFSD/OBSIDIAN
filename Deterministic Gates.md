---
description: How to wire deterministic enforcement — pre-commit, CI, agent-runtime hooks, permissions — into a repo so the agent's failure modes are blocked by mechanism, not prose. The load-bearing defense layer.
---
# Deterministic Gates

Prose rules don't bind — the documented production-DB-wipe incidents each had a written rule
against destructive commands and the agent ignored it. **Gates bind:** they run *outside* the
model, so it can't skip them. This is the load-bearing defense; the always-on rules in [[CLAUDE]]
are only a backstop. Wire these into a repo (and the agent's runtime) to make failure-mode
prevention deterministic.

Defense is three layers: **sandbox** (the agent *can't reach* what it shouldn't), **agent-runtime
gates** (block bad *actions* before they run), and **repo gates** (block bad *code* from landing).
Each gate below notes the failure cluster it covers and whether it's a hard block or advisory. The
*why* behind them — the named methodology — is [[Deterministic Methodology]].

## Sandbox — the agent can't reach what it shouldn't
The outermost layer: isolate the agent so a bad action has no blast radius. **[V]** (2026-06)
- **OS-level:** Anthropic `sandbox-runtime` — filesystem + network jail (sandbox-exec / bubblewrap + egress proxy), built into Claude Code as `/sandbox`. Caveat: an open issue notes the agent can disable it in auto-allow mode, so keep the deny side pinned.
- **Container-level:** `container-use` — an MCP server giving each agent its own container + git-worktree branch, auto-commit, and a full command log; disposable, reviewable, parallel.
- Default-deny network + egress allowlist; no prod credentials in the agent's env. This is what actually contains the destructive action a runtime gate misses.

## Repo gates — block bad code from landing

| Gate | Tool(s) | Catches (cluster) | Block? |
|---|---|---|---|
| Secret scan | gitleaks / trufflehog (pre-commit **and** CI + full-history) | hardcoded secrets (Security) | hard |
| Lint + format | ESLint / Ruff / golangci-lint + formatter (`no-empty`, bare-except, errcheck) | swallowed errors, dead code (Error handling) | hard |
| Type check (strict) | `tsc --strict`, `mypy --strict` | nonexistent symbols, unhandled null, removed APIs (API currency / Error handling) | hard |
| SAST | Semgrep / CodeQL in CI | injection, XSS, weak-crypto patterns (Security) | hard for known patterns; advisory for semantics (misses ~half) |
| Dependency scan | lockfile + `--frozen-lockfile`; `npm audit` / OSV-Scanner; Socket (`sfw`) | known-vuln + hallucinated/malicious packages (Dependencies) | hard |
| Tests + coverage gate | the project's runner + a coverage threshold in CI | regressions; forces error-branch tests (Error handling / Debugging) | hard |

**TypeScript specifics** (baseline `tsconfig` + rationale in [[TypeScript Development]]): gate
`tsc --noEmit` (`strict` + `noUncheckedIndexedAccess`, `noImplicitReturns`,
`noFallthroughCasesInSwitch`, `noImplicitOverride`, `verbatimModuleSyntax`) in CI; typed-eslint
(`no-floating-promises`, `no-misused-promises`, `switch-exhaustiveness-check`); and a committed
`@microsoft/api-extractor` `.api.md` as an **API-contract gate** (a changed public signature fails
review). These catch the function-breaking regressions agents introduce — broken branches, dropped
awaits, silent signature drift.

## Agent-runtime gates — block bad actions before they run

- **PreToolUse hook / Bash deny-list** — refuse `git reset --hard`, `push --force`, destructive
  SQL (`DROP`…), `rm -rf`, and writes to migrations, lockfiles, `.github/`, `.claude/`. Runs
  *before* the permission prompt; a blocking hook overrides an allow rule. (Destructive ops) — **hard**
- **Stop hook = tests pass** — don't let the turn end until the test script is green; forces
  verify-before-done and reproduce-then-fix. (Debugging / Error handling) — **hard**
- **Least privilege** — no production credentials in the agent's environment; run in a
  sandbox/dev-container with an egress allow-list; keep backups isolated from live data. This is
  what would have prevented the DB-wipe incidents. (Destructive ops) — **hard**
- **Human-approval (ask) gate** — require explicit approval for anything irreversible: prod data,
  migrations, deploys, publishes, force-push. Enforced by the harness, not the model's judgment. — **hard**

## Retrofit order for an existing repo

Highest-leverage, lowest-friction first; add gates incrementally so the build doesn't go red all
at once:

1. **Lockfile + `--frozen-lockfile` + `npm audit`/OSV in CI** — cheap, immediate supply-chain floor.
2. **Secret scan** (gitleaks) pre-commit + CI, and scan history once.
3. **Type-check strict + lint/format** as CI gates — promote warnings to errors a rule at a time.
4. **Tests + coverage gate.**
5. **SAST** (Semgrep / CodeQL) in CI.
6. **Agent-runtime:** PreToolUse deny-list for destructive commands + Stop-hook=tests-pass + strip prod creds.
7. **Human-approval gate** for irreversible ops.

## Representative config (verify against each tool's current docs — versions drift)

`.pre-commit-config.yaml` (secrets + lint):
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: <pin>
    hooks: [{ id: gitleaks }]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: <pin>
    hooks: [{ id: ruff }, { id: ruff-format }]
```

Agent-runtime deny + verify-before-done (Claude Code `.claude/settings.json`, representative):
```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "Bash",
      "hooks": [{ "type": "command",
        "command": "<exit non-zero on: reset --hard | push --force | DROP | rm -rf>" }] }],
    "Stop": [{ "hooks": [{ "type": "command",
        "command": "<run tests; exit non-zero to keep working>" }] }]
  }
}
```

## Sources
- [Anthropic — Claude Code best practices (hooks deterministic vs CLAUDE.md advisory)](https://code.claude.com/docs/en/best-practices)
- [Microsoft — Defense in depth for autonomous AI agents](https://www.microsoft.com/en-us/security/blog/2026/05/14/defense-in-depth-autonomous-ai-agents/)
- [Gitleaks](https://github.com/gitleaks/gitleaks) · [Semgrep](https://semgrep.dev/) · [CodeQL](https://codeql.github.com/) · [OSV-Scanner](https://github.com/google/osv-scanner) · [Socket](https://docs.socket.dev/) · [pre-commit](https://pre-commit.com/)
- [Package hallucination / slopsquatting (USENIX 2025)](https://arxiv.org/abs/2406.10279)

---
## Related
[[CLAUDE]] · [[Deterministic Methodology]] · [[Spec-Driven Build Loop]] · [[Invariants]] · [[Code Conventions]] · [[Good Code in the AI Age]] · [[Agent Eval & Injection Defense]]
