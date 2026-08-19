# Performance Checklist

Use this checklist before diagnosing, changing, or claiming a performance improvement.

## Baseline

- [ ] The slow behavior is named precisely.
- [ ] The performance domain is identified: backend latency, CPU, memory, database, frontend, startup, bundle size, async/I/O, or throughput.
- [ ] A baseline metric is captured before proposing a fix.
- [ ] Measurement method is documented.
- [ ] Representative data is used or caveated.
- [ ] Representative load is used or caveated.
- [ ] Target or acceptable threshold is stated when available.
- [ ] p95 or p99 is used for user-facing latency, not only average.
- [ ] The baseline can be repeated after the fix.

## Tool Selection

- [ ] Node CPU uses `0x`, inspector, Clinic Flame, or existing profiling tools.
- [ ] Node async/wait uses Bubbleprof, tracing, instrumentation, or path review.
- [ ] Python CPU uses `py-spy`, `cProfile`, or the project's profiler.
- [ ] Python memory uses `memray`, `tracemalloc`, or equivalent.
- [ ] Go uses `pprof` or `go tool trace`.
- [ ] Frontend uses Core Web Vitals, performance traces, bundle analysis, or framework profiler.
- [ ] Database uses slow query logs plus `EXPLAIN ANALYZE` or engine equivalent.
- [ ] Load-related capacity questions are handed to `load-tester-advisor`.
- [ ] Tool limitations are named when measurements are synthetic or local.

## Profiling Quality

- [ ] The profiled path matches the reported slow behavior.
- [ ] Data size matches the scenario that is slow.
- [ ] Warm-up effects are considered when relevant.
- [ ] CPU bottlenecks are separated from I/O wait.
- [ ] Query time is separated from application processing time.
- [ ] Frontend render cost is separated from network and server latency.
- [ ] Memory growth is distinguished from one-time allocation.
- [ ] The profile points to a specific high-impact path.
- [ ] Findings are ranked by measured contribution, not code appearance.

## Fix Selection

- [ ] The first fix targets the largest measured contributor.
- [ ] One optimization is changed at a time when attribution matters.
- [ ] Caching is used only when stale data, invalidation, and memory cost are acceptable.
- [ ] Indexes are added only after reading the query plan.
- [ ] Memoization is added only when rerender or recomputation cost is measured.
- [ ] Batching/pagination is considered for repeated I/O or unbounded data access.
- [ ] Algorithmic fixes are considered when CPU grows with input size.
- [ ] Behavior-changing trade-offs are called out explicitly.
- [ ] The fix follows existing project patterns.

## Safety

- [ ] Production profiling has a short capture window.
- [ ] Sampling profiler is preferred for production captures.
- [ ] Profiling one instance or controlled traffic is enough for the question.
- [ ] Sensitive data is not exposed in traces or logs.
- [ ] Unbounded debug logging is not added.
- [ ] Feature behavior remains correct after optimization.
- [ ] Tests or smoke checks cover the optimized path.
- [ ] Rollback is straightforward for risky optimizations.

## Verification

- [ ] The same metric is measured before and after.
- [ ] The same method is used before and after.
- [ ] The same data/load is used before and after or the difference is documented.
- [ ] The result reports before and after values.
- [ ] The result reports percent or absolute improvement when useful.
- [ ] Regression checks are run for affected behavior.
- [ ] Remaining bottlenecks are separated from completed fixes.
- [ ] If results are inconclusive, the report says so.

## Final Report

- [ ] Baseline and target are clear.
- [ ] Findings include measured impact.
- [ ] Fix is tied directly to the finding.
- [ ] Result is stated as evidence, not expectation.
- [ ] Trade-offs are included when behavior, memory, cost, or complexity changes.
- [ ] Follow-up uses `load-tester-advisor` only if concurrency capacity remains a question.
- [ ] The report does not claim "faster" without numbers.
