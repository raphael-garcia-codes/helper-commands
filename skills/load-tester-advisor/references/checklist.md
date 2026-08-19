# Load Tester Advisor Checklist

Use this checklist before writing or running load, stress, spike, or soak tests.

## Question and Test Type

- [ ] The test question is stated before choosing a tool.
- [ ] Load test is chosen when validating expected peak traffic against thresholds.
- [ ] Stress test is chosen when finding the degradation or breaking point.
- [ ] Spike test is chosen when validating sudden burst handling and recovery.
- [ ] Soak test is chosen when checking leaks, resource exhaustion, or long-duration degradation.
- [ ] The test type is named in the plan.
- [ ] Functional correctness is already trusted or separately tested.
- [ ] Success is not defined as "the script ran".

## Target Environment

- [ ] Target URL and environment are explicit.
- [ ] Production is not targeted without explicit user confirmation.
- [ ] Staging differences from production are documented.
- [ ] Data volume and service configuration are described when they affect results.
- [ ] Autoscaling, rate limits, queues, caches, and CDN behavior are noted.
- [ ] Third-party side effects are identified: payments, email, SMS, search, AI APIs, or webhooks.
- [ ] Test data can be created, isolated, or cleaned up safely.
- [ ] Authentication and tenant/account setup are realistic.

## Production Safety

- [ ] Explicit approval is recorded for any production-impacting run.
- [ ] A hard duration cap is set.
- [ ] Off-peak window is selected when production-like systems may be affected.
- [ ] Monitoring dashboards are open before the run.
- [ ] Abort condition is defined before the run.
- [ ] Abort command or kill switch is known.
- [ ] On-call or owner awareness is handled when required.
- [ ] Vendor rate limits and costs are considered.
- [ ] The test avoids destructive or revenue-impacting actions unless separately approved.

## Tool Choice

- [ ] k6 is considered for JS/TS-friendly HTTP tests with strong thresholds.
- [ ] Artillery is considered for YAML-first scenarios, WebSocket, and quick CI use.
- [ ] Locust is considered for Python teams and custom user behavior.
- [ ] Gatling is considered for JVM teams and high-throughput typed scenarios.
- [ ] JMeter is considered only when legacy protocols or existing investment justify it.
- [ ] Existing team tooling wins when it can answer the question.
- [ ] Tool limitations are named: browser realism, protocol support, distributed execution, or reporting.

## Traffic Model

- [ ] Endpoint mix reflects real usage or states the assumption.
- [ ] Arrival rate or virtual users are selected intentionally.
- [ ] Ramp-up and ramp-down are defined.
- [ ] Think time is included unless intentionally testing raw endpoint throughput.
- [ ] Data varies enough to avoid measuring only cache hits.
- [ ] Read/write ratio is realistic.
- [ ] User journeys include setup steps such as login only when they are part of the test question.
- [ ] Spike tests include recovery observation after the burst.
- [ ] Soak tests run long enough to expose the suspected leak or exhaustion mode.

## Thresholds

- [ ] p95 latency threshold is defined.
- [ ] p99 latency threshold is defined when tail latency matters.
- [ ] Error-rate threshold is defined.
- [ ] Throughput or arrival-rate target is defined.
- [ ] Resource thresholds are named when monitoring is available: CPU, memory, DB connections, queue depth.
- [ ] Thresholds are set before seeing results.
- [ ] Thresholds map to user or business expectations.
- [ ] Average latency is not the main pass/fail metric.

## Results and Reporting

- [ ] Observed values are compared against thresholds.
- [ ] Pass/fail verdict is explicit.
- [ ] Stress tests report the breaking or degradation point.
- [ ] Spike tests report recovery behavior.
- [ ] Soak tests report resource drift over time.
- [ ] Environment caveats are included.
- [ ] Raw metrics are not reported without interpretation.
- [ ] Bottlenecks are handed to `performance` when root-cause diagnosis is needed.

## Final Check

- [ ] The test can be repeated by another engineer.
- [ ] The test protects the target system.
- [ ] The result answers the original question.
- [ ] The report does not claim production capacity from a non-production environment without caveats.
