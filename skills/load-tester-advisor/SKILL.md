---
name: load-tester-advisor
description: Plans load, stress, spike, or soak tests with realistic traffic, explicit thresholds, and production safety gates.
---

# Load Tester Advisor

## Hard Gate

- Classify the test type before writing a script: load, stress, spike, or soak.
- Never target production without explicit confirmation, a time cap, monitoring, and an abort plan.
- Define pass/fail thresholds before the run; raw metrics without thresholds are not a test result.

## Process

1. Identify the real question: expected peak, breaking point, sudden burst, or long-duration stability.
2. Choose the tool from language, protocol, team experience, and existing test assets; do not default blindly.
3. Confirm the target environment and state whether it is production-like.
4. Model realistic traffic: ramp pattern, arrival rate or VUs, think time, data variety, and endpoint mix.
5. Set p95/p99 latency and error-rate thresholds before running.
6. Run with a hard duration cap and capture structured results.
7. Report pass/fail against thresholds and identify the breaking point for stress tests.
8. If bottlenecks appear, hand root-cause diagnosis to `performance`.

## References

- `references/checklist.md` — Read before selecting the test type, tool, target environment, or thresholds.
- `references/examples.md` — Read for concrete k6, Artillery, Locust, and report examples.
- `references/anti-patterns.md` — Read before running against production or interpreting concurrency numbers.

## Out of scope

**vs. `performance`:** this skill simulates concurrent traffic and identifies capacity limits. `performance` diagnoses and fixes a specific slow path.

**vs. `test-generator`:** test-generator proves functional correctness. This skill measures behavior under load after correctness is already trusted.

## Output format

```md
## Load Test Plan: [target]

**Test type:** [load | stress | spike | soak]
**Tool:** [tool] — [reason]
**Target environment:** [environment and caveats]
**Traffic shape:** [ramp, VUs/arrival rate, endpoint mix, think time]

### Thresholds
- p95 latency: [value]
- p99 latency: [value]
- Error rate: [value]

### Results
| Metric | Threshold | Observed | Verdict |
|---|---|---|---|

**Breaking point:** [for stress test]
**Recommendation:** [next action]
```
