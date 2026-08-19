# Performance Anti-Patterns

Read this before publishing a performance fix or recommendation. Remove anything that is not backed by measurement or that makes attribution impossible.

## 1. Optimization Before Measurement

Bad signs:

- The fix is proposed from intuition.
- No baseline metric exists.
- The report says a path "looks slow" without timing or profiling.

Why it hurts:

- Work may target code that is not the bottleneck.
- The team cannot prove whether the change helped.

Do instead:

- Capture a baseline metric and measurement method first.
- Profile the representative path before choosing a fix.

## 2. Wrong Profiler, Wrong Conclusion

Bad signs:

- A CPU flamegraph is used to dismiss I/O wait.
- A database problem is diagnosed only from application code.
- Frontend performance is judged only by backend response time.

Why it hurts:

- Each tool sees only part of the system.
- Bottlenecks can move across CPU, database, network, rendering, and queues.

Do instead:

- Identify the performance domain first.
- Use tools that can observe that domain.

## 3. Cache as First Reflex

Bad signs:

- Cache is proposed before checking N+1 queries, pagination, batching, or query plans.
- Invalidation, stale data, memory, and tenant isolation are not discussed.
- Cache success is assumed without hit-rate evidence.

Why it hurts:

- Cache can hide the real problem while adding correctness risk.
- Stale data bugs are often worse than the original slowness.

Do instead:

- Fix avoidable repeated work first.
- Add cache only when data freshness and invalidation rules are clear.

## 4. Index Without Plan

Bad signs:

- An index is added because a query "filters by that column".
- `EXPLAIN ANALYZE` or engine equivalent was not read.
- Write overhead and storage cost are ignored.

Why it hurts:

- The database may not use the index.
- Extra indexes can slow writes and migrations.

Do instead:

- Read the actual query plan.
- Match the index to filter, join, and sort shape.

## 5. Average Latency Claim

Bad signs:

- The result reports only average latency.
- Tail latency, timeout rate, and error rate are missing.
- User-facing performance is declared improved from mean values.

Why it hurts:

- Averages hide the slow requests users feel.
- Error spikes can make average latency look better by failing early.

Do instead:

- Report p95/p99 and error rate for user-facing paths.
- Include average only as supporting detail.

## 6. Multi-Fix Attribution Loss

Bad signs:

- Three optimizations land at once.
- The report cannot say which change produced the improvement.
- A regression cannot be isolated.

Why it hurts:

- Future tuning becomes guesswork.
- Rollback may remove useful and harmful changes together.

Do instead:

- Change one high-impact thing at a time when practical.
- Re-measure after each meaningful optimization.

## 7. Success Without Same-Method Verification

Bad signs:

- The conclusion says "should be faster".
- Before and after used different data, load, or tools without caveats.
- No regression checks were run.

Why it hurts:

- The improvement may be measurement noise.
- Behavior may be faster because it is doing less work incorrectly.

Do instead:

- Measure before and after with the same method.
- Report caveats and validate correctness on the optimized path.
