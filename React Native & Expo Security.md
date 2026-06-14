---
description: Mobile-stack conventions for React Native / Expo — testing (Maestro/Detox, no Playwright), the New Architecture / Hermes baseline, OWASP Mobile Top 10 2024 + MASVS, secure storage and device hardening, and HIPAA for a PHI/visit-recording app. The mobile companion to [[Convex Conventions]] (backend) and [[Agent Eval & Injection Defense]] (the chatbot). Web-React conventions (Next server/client, Playwright) do not transfer.
---
# React Native & Expo Security

Facts tagged **[V]** = verified against primary sources (2026-06-14); **[R]** = reported / single-source / directional (treat numbers as directional).

## Architecture baseline (New Architecture / Hermes)
- The New Architecture (Fabric renderer + TurboModules + JSI) is the default since **RN 0.76**; the old bridge was retired in **0.82**; **Hermes V1** shipped as the default JS engine in **0.84**. Expo **SDK 52+** ships New Arch on by default for managed apps; ~83% of SDK 54 EAS builds use it (Jan 2026). **[V]**
- Why it matters: native-module compatibility and performance profiling differ; set EAS build profiles accordingly.

## Testing (Playwright does not apply)
- Playwright only works against `react-native-web` / WebViews — irrelevant to native flows. **[V]**
- **Unit/component:** Jest + React Native Testing Library (the RTL analog — same queries, native renderer). Vitest is fine for pure logic and Convex functions, but Jest remains the RN default. Test behavior, not implementation ([[Writing Tests]] #1). **[V]/[R]**
- **E2E — Maestro vs Detox:**
  - **Maestro** — black-box, YAML flows via the accessibility layer, zero in-app deps, first-class Expo/EAS support (`.maestro/` flows, `eas.json` `e2e-test` profile); flakiness <1%. **Start here** for an Expo app shipping fast. **[V]/[R]**
  - **Detox** — gray-box, in-process, synchronizes with the JS thread so steps wait until the app is idle; flakiness <2% but RN/Xcode-version-coupled, can block RN upgrades, and has no first-party Expo support. Reach for it only if you need gray-box sync for animation/network-heavy flows. **[V]/[R]**
  - Use `testID` selectors, not visible text, in either. **[V]**

## Mobile security — OWASP Mobile Top 10 (2024) + MASVS, not the web list
- **OWASP Mobile Top 10 2024** (first major refresh since 2016): **M1 = Improper Credential Usage** (#1), **M2 = Inadequate Supply Chain Security** — note the supply-chain theme recurs in [[Agent Eval & Injection Defense]]. **[V]**
- **MASVS v2.1.0 (Jan 2024)** dropped the L1/L2/R verification levels (gone since v2.0.0), replaced by **MAS Testing Profiles** in MASWE. Any doc or RFP still saying "MASVS Level 2" is stale. Control groups: MASVS-STORAGE, -AUTH, -CRYPTO, etc. **[V]**

## Secure storage + device hardening
- `expo-secure-store` → Keychain (iOS) / Keystore (Android), hardware-backed where available, "encrypted at the OS level, not in JavaScript." Use for **tokens/small secrets only** — not a database; large/offline data belongs elsewhere. Exclude it from Android Auto Backup. **[V]/[R]**
- **Ban in review/CI** (these are [[Deterministic Gates]] candidates — lint / secret-scan / grep rules): base64 "encoding as encryption"; AsyncStorage with a key prefix for secrets; persisting a Redux tree containing PHI; shipping tokens/PHI to Sentry/Crashlytics.
- Add: TLS + certificate/SSL pinning; jailbreak/root detection (revoke tokens on detection); biometric gating for PHI access via `expo-local-authentication`; deep-link hygiene — deep links are **not** secure, never pass PHI in them. **[R]**

## HIPAA for a visit-recording app
For an app that records visits, transcribes, summarizes, and runs a citation-grounded chatbot over PHI:
- Encrypt PHI at rest (AES-256), keys in Keychain/Keystore (hardware-backed), never in source or AsyncStorage; unique IVs, key rotation, KMS/HSM for key-wrapping. **[R]**
- Encrypt in transit (TLS); short-lived access tokens + refresh-token rotation; OIDC + PKCE; MFA; re-auth for sensitive actions. **[R]**
- Audit-log every PHI access (who/what/when/where/why) with correlation IDs but **exclude PHI payloads from logs**. **[R]**
- **BAAs with every vendor that touches PHI** — hosting, transcription, logging, crash reporting, LLM/summarization. This is the decisive architectural question, not a checkbox. **[V]** Convex's BAA covers the backend ([[Convex Conventions]]).
- On-device vs cloud transcription: on-device keeps PHI off third-party servers and **shrinks BAA scope**; cloud is higher-quality but needs a signed BAA + minimum-necessary payloads. **Default to on-device** for the raw audio→text step where quality permits. **[R]**
- **Hard gate:** no real PHI in the system until every BAA is signed (mirrors [[Convex Conventions]]).

## Sources
- [OWASP Mobile Top 10 (2024)](https://owasp.org/www-project-mobile-top-10/) · [OWASP MASVS](https://mas.owasp.org/MASVS/)
- [Expo — React Native's New Architecture](https://docs.expo.dev/guides/new-architecture/) · [expo-secure-store](https://docs.expo.dev/versions/latest/sdk/securestore/) · [expo-local-authentication](https://docs.expo.dev/versions/latest/sdk/local-authentication/)
- [Maestro docs](https://docs.maestro.dev/) · [Detox docs](https://wix.github.io/Detox/) · [React Native Testing Library](https://callstack.github.io/react-native-testing-library/)

---
## Related
[[Convex Conventions]] · [[Agent Eval & Injection Defense]] · [[Deterministic Gates]] · [[Invariants]] · [[Writing Tests]] · [[Code Conventions]]
