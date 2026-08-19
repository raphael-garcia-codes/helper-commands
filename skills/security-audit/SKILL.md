---
name: security-audit
description: Use when the user asks for a security review or audit, mentions a vulnerability or exploit, is implementing or touching authentication, authorization, payments, or PII, or asks "is this safe" or "can this be exploited." Also use proactively when reviewing code that handles user input, secrets, or sensitive data, even if not explicitly requested.
---

# Security Audit

## Process

1. Check `agent_docs/security.md` first — it documents this project's actual security posture and known-sensitive areas (auth approach, secrets handling, PII/payment data). An audit that ignores documented context risks flagging non-issues and missing what actually matters here.
2. Research current, real vulnerability classes and mitigations for this project's specific stack — don't rely on a generic, memorized checklist. Risks differ meaningfully between a Node/Express API, a Django app, a serverless function, and a mobile client; what's the standard mitigation this year may differ from a couple of years ago.
3. Prioritize by what's actually reachable and dangerous in this codebase, not a mechanical pass through every OWASP category regardless of relevance:
   - Authentication/authorization bypass or privilege escalation
   - Injection (SQL, command, template) in the actual data layer this project uses
   - Secrets or credentials committed to the repo or logged
   - Unvalidated input reaching a sensitive sink (file system, shell, database, external request)
   - Sensitive data (PII, payment info) exposed in logs, error messages, or responses
4. Before labeling anything Critical, verify it isn't already mitigated by framework defaults, middleware, ORM parameterization, or existing guards — false Criticals erode trust in the audit.
5. For each finding, explain the actual exploit path — not just "this could be a vulnerability" — and give a concrete fix, not a generic recommendation to "sanitize input."
6. Distinguish real, exploitable findings from defense-in-depth suggestions; label which is which so the user can prioritize.

## What NOT to do

- Don't produce a generic OWASP Top 10 checklist disconnected from what this codebase actually does — a mobile app and a payment API have different real risk profiles.
- Don't flag theoretical vulnerabilities with no realistic exploit path as if they were equivalent to exploitable ones.
- Don't recommend a specific security library or pattern without checking it's still current — security tooling and recommended versions change, and outdated advice here is actively harmful.
- Don't skip explaining *why* something is exploitable — "add input validation" without the actual attack scenario doesn't help the user understand the risk.

## Out of scope

This skill covers vulnerabilities in this project's own first-party code — auth logic, injection risks, secrets handling, unvalidated input. It does not scan third-party dependencies for known CVEs, license issues, or unmaintained packages — that's `dependency-auditor` (Upsell 1). If a request is really "check my dependencies for vulnerabilities" or references `package.json`/`requirements.txt` directly, use `dependency-auditor` instead.

## Output format

```
## Critical (exploitable now)
- [file:line] — vulnerability — exploit path — fix

## Should address
- [file:line] — risk — fix

## Defense in depth (optional hardening)
- [file:line] — suggestion
```

See the anchor install references for checklists, examples, and failure modes: `references/checklist.md`, `references/examples.md`, and `references/anti-patterns.md`.
