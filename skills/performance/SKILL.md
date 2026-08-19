---
name: performance
description: Diagnoses and fixes slow behavior using baseline measurements, profiling, and same-method before/after verification.
---

# Performance

## Hard Gate

- Measure before proposing a fix. A hunch is not evidence.
- Identify the performance domain first: backend CPU/memory/latency, frontend Core Web Vitals, database query, or async/I/O wait.
- Do not declare success without a same-method before/after number.

## Process

1. Capture baseline metric and target, including how it was measured.
2. Profile a representative path under representative data/load.
3. Interpret the profile by domain; CPU flamegraphs do not explain I/O wait or N+1 latency by themselves.
4. Rank findings by measured impact, not by code appearance.
5. Fix the highest-impact issue first, one isolated change at a time.
6. Re-measure exactly the same way and report before/after.
7. Flag behavior-changing optimizations as trade-offs, not free wins.
8. Use `load-tester-advisor` afterward if capacity under concurrency needs validation.

## References

- `references/checklist.md` — Read before measuring, profiling, or deciding which tool applies.
- `references/examples.md` — Read for profiler commands, Core Web Vitals examples, and before/after report patterns.
- `references/anti-patterns.md` — Read before caching, memoizing, indexing, or refactoring without measurement.

## Out of scope

**vs. `agent_docs/engineering-standards.md`:** that file stores static project conventions and budgets. This skill performs active diagnosis.

**vs. `debug-assistant`:** debug-assistant fixes incorrect behavior. This skill fixes correct-but-slow behavior.

**vs. `load-tester-advisor`:** load-tester-advisor simulates concurrent users. This skill profiles and improves a specific slow path.

**vs. `refactor-guide`:** refactor-guide improves structure without measured performance goals. This skill is judged by metrics.

## Output format

```md
## Performance Finding: [target]

**Baseline:** [metric + method]
**Target:** [target or N/A]

### Findings
1. [finding] — [measured impact]

### Fix Applied
[change tied to the finding]

### Result
Before: [value] -> After: [value], measured the same way.

### Trade-offs
[if any]
```
