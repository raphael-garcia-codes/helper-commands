# Load Tester Advisor Examples

Use these examples to calibrate realistic traffic, thresholds, and result reporting.

## Example 1: Checkout Load Test

### Input

A team wants to know if staging can handle the expected launch peak:

- Target: staging checkout API.
- Expected peak: 25 requests per second for product browsing and 3 requests per second for order creation.
- User journey: list products, view product, create order for test SKU.
- Thresholds requested by product: p95 below 700ms, error rate below 1%.
- Production must not be targeted.

### Weak Output

```text
Run 100 users against /api/orders for 10 minutes and see if it is fast.
```

### Why This Is Weak

- It tests one endpoint instead of the real journey mix.
- It defines no pass/fail threshold.
- It uses vague "users" without arrival rate or think time.
- It does not mention environment safety.

### Strong Output

````md
## Load Test Plan: staging checkout

**Test type:** load
**Tool:** k6 — existing team uses JavaScript and k6 thresholds give clear pass/fail output.
**Target environment:** staging only; do not run against production.
**Traffic shape:** ramp to expected peak, hold for 10 minutes, include browse-heavy mix and short think time.

### Thresholds
- p95 latency: < 700ms
- p99 latency: < 1500ms
- Error rate: < 1%
- Order creation checks: status is 201 for valid test SKU

### k6 sketch
```
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 30 },
    { duration: '10m', target: 30 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<700', 'p(99)<1500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const product = http.get(`${__ENV.BASE_URL}/api/products`);
  check(product, { 'products ok': (r) => r.status === 200 });
  sleep(Math.random() * 2 + 1);

  const detail = http.get(`${__ENV.BASE_URL}/api/products/test-sku`);
  check(detail, { 'detail ok': (r) => r.status === 200 });
  sleep(Math.random() * 2 + 1);

  if (Math.random() < 0.1) {
    const order = http.post(`${__ENV.BASE_URL}/api/orders`, JSON.stringify({ sku: 'test-sku' }), {
      headers: { 'Content-Type': 'application/json' },
    });
    check(order, { 'order created': (r) => r.status === 201 });
  }
}
```

### Run
`BASE_URL=https://staging.example.com k6 run --out json=results.json checkout-load.js`
````

### Why This Is Strong

- It answers expected peak traffic, not a random concurrency number.
- It includes thresholds before the run.
- It uses varied behavior and think time.
- It keeps the run scoped to staging.

## Example 2: Spike Test With Abort Plan

### Input

The API normally receives 50 requests per minute, but a marketing email may create a short burst. The team wants to verify recovery after a sudden jump. Staging is production-like except it has smaller database capacity.

### Strong Output

````md
## Load Test Plan: marketing burst recovery

**Test type:** spike
**Tool:** Artillery — simple arrival-rate phases are enough for this HTTP scenario.
**Target environment:** staging; database capacity is smaller than production, so do not claim final production capacity.
**Abort plan:** stop immediately if error rate exceeds 10% for two consecutive minutes or DB connections exceed 90%.

### Traffic shape
- 2 minutes warm-up at 50 requests/minute.
- 1 minute spike at 500 requests/minute.
- 5 minutes recovery at 50 requests/minute.

### Thresholds
- p95 latency during steady state: < 600ms
- p95 latency during recovery: back under 600ms within 3 minutes
- Error rate: < 2% outside the spike minute

### Artillery sketch
```
config:
  target: "https://staging.example.com"
  phases:
    - duration: 120
      arrivalRate: 1
    - duration: 60
      arrivalRate: 8
    - duration: 300
      arrivalRate: 1
  ensure:
    p95: 600
    maxErrorRate: 2
scenarios:
  - flow:
      - get:
          url: "/api/products"
      - think: 1
      - get:
          url: "/api/products/test-sku"
```

### Report shape
| Metric | Threshold | Observed | Verdict |
|---|---|---|---|
| Recovery p95 | < 600ms within 3m | [value] | [pass/fail] |
| Error rate | < 2% outside spike | [value] | [pass/fail] |

**Recommendation:** If recovery misses the threshold, hand the slow path to `performance` with DB connection and queue-depth graphs.
````

