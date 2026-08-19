# Performance Examples

Use these examples to calibrate measurement-first diagnosis and same-method verification.

## Example 1: Backend Checkout Latency

### Input

Users report checkout is slow. A staging run shows:

- p95 checkout latency: 1.8s.
- `POST /checkout` can include up to 35 line items.
- Profiling shows `getInventoryForSku` called sequentially per line item.
- Each inventory lookup waits on a remote service.
- A batch endpoint exists but is not used.

### Weak Output

```text
Add caching to inventory lookups. It should make checkout faster.
```

### Why This Is Weak

- It proposes a fix before tying it to the measured bottleneck.
- It adds cache invalidation risk without proving repeated reads are the issue.
- It has no before/after verification plan.

### Strong Output

```md
## Performance Finding: checkout inventory lookup

**Baseline:** p95 checkout latency 1.8s from the staging checkout script.
**Target:** p95 below 800ms.

### Findings
1. `getInventoryForSku` is called sequentially for up to 35 line items.
2. Profile and timing spans show inventory waits contribute about 1.1s of wall-clock latency.
3. The remote inventory service already exposes a batch lookup endpoint.

### Fix Applied
Replace per-item inventory lookup with one batch lookup by SKU list, preserving the existing out-of-stock behavior and error handling.

### Result
Before: p95 1.8s -> After: p95 620ms, measured with the same staging checkout script and the same cart fixture.

### Trade-offs
- Larger single inventory request payload.
- Failure now affects the whole batch call, so existing checkout error handling must remain consistent.
```

### Why This Is Strong

- It measures before changing code.
- The fix targets the largest measured contributor.
- Verification uses the same method and fixture.
- Trade-offs are explicit.

## Example 2: Database Query Regression

### Input

An admin page slowed down after adding filters. Facts:

- The endpoint still returns correct data.
- Query time grew from 80ms to 2.4s for a tenant with 500k orders.
- `EXPLAIN ANALYZE` shows sequential scan on `orders` when filtering by `tenant_id`, `created_at`, and `status`.
- Existing index covers only `tenant_id`.

### Strong Output

```md
## Performance Finding: admin order filter query

**Baseline:** query time 2.4s for tenant fixture with 500k orders, measured with `EXPLAIN ANALYZE`.
**Target:** under 250ms for the same fixture.

### Findings
1. The filtered admin query performs a sequential scan over `orders`.
2. The existing `tenant_id` index does not support the combined filter and sort shape.
3. Most time is spent in database scan and sort, not application serialization.

### Fix Applied
Add a composite index matching the query shape: tenant filter, status filter, and created-at sort. Review the database engine's index order rules before applying.

### Result
Before: 2.4s -> After: 140ms, measured with the same `EXPLAIN ANALYZE` query and tenant fixture.

### Trade-offs
- Additional write overhead on order inserts/updates.
- Additional index storage.
```

### Why This Is Strong

- It uses the database plan rather than guessing.
- It names the query shape the index must support.
- It reports write/storage trade-offs.

## Profiler Command Patterns

Choose the profiler for the suspected domain:

```bash
npx 0x -- node server.js
npx autocannon -c 50 -d 30 http://localhost:3000/api/slow-endpoint
py-spy record -o profile.svg --pid <PID> --duration 30
python -m cProfile -o profile.pstats script.py
memray run script.py
curl -s http://localhost:6060/debug/pprof/profile?seconds=30 -o cpu.pb.gz
go tool pprof -http=:0 cpu.pb.gz
```

Do not run every tool. Pick the tool that can falsify the current bottleneck hypothesis.
