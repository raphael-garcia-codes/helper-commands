# Load Tester Advisor Anti-Patterns

Read this before running traffic against any environment. Remove anything that makes the test unsafe, unrealistic, or impossible to interpret.

## 1. Calling Everything a Load Test

Bad signs:

- Stress, spike, and soak tests are all called "load tests".
- The report does not say which question is being answered.
- Breaking point and expected peak are mixed together.

Why it hurts:

- Different tests need different traffic shapes and verdicts.
- A stress result cannot be read as expected-peak capacity.

Do instead:

- Name the test type first.
- Align traffic shape and pass/fail metrics to that type.

## 2. Production Without Guardrails

Bad signs:

- Production is targeted because staging is incomplete.
- No explicit approval, time cap, monitoring, or abort plan exists.
- Third-party calls may charge money or trigger real customer communication.

Why it hurts:

- Load tests can become outages.
- Vendors can rate-limit or bill the system.
- Real users can receive test effects.

Do instead:

- Ask for explicit approval before any production-impacting run.
- Define duration, abort conditions, monitoring, and safe test data.

## 3. One Endpoint Hammer

Bad signs:

- The script hits one endpoint with no think time.
- The endpoint uses the same cached ID for every request.
- Results are described as user capacity.

Why it hurts:

- Real users exercise mixed paths, data variety, authentication, and pauses.
- Cache-heavy results can overstate capacity.

Do instead:

- Model a representative journey or endpoint mix.
- Include think time and varied data unless raw endpoint throughput is the actual question.

## 4. Thresholds After Results

Bad signs:

- p95, p99, and error thresholds are adjusted after the run.
- The report says "seems okay" without pre-declared pass/fail.
- The team changes success criteria to avoid rerunning.

Why it hurts:

- The test becomes a chart, not a validation.
- Stakeholders cannot trust the verdict.

Do instead:

- Define thresholds before the run.
- Mark the result as failed if the thresholds were unrealistic and rerun with corrected criteria.

## 5. Average Latency Reporting

Bad signs:

- Only average latency is reported.
- Tail latency and error rate are missing.
- Timeout behavior is ignored.

Why it hurts:

- Users feel p95 and p99 pain, not averages.
- Error spikes can hide behind acceptable mean latency.

Do instead:

- Report p95, p99, error rate, throughput, and relevant resource saturation.
- Use averages only as secondary context.

## 6. Environment Overclaiming

Bad signs:

- Staging results are presented as production capacity.
- Smaller databases, disabled services, warm caches, or different autoscaling are not mentioned.
- Local laptop results are treated as server results.

Why it hurts:

- Capacity decisions can be made from non-comparable infrastructure.
- The team may underprepare for real launch conditions.

Do instead:

- State environment differences.
- Use staging results to compare changes or find bottlenecks, not to guarantee production capacity unless parity is real.

## 7. Ignoring Side Effects

Bad signs:

- Tests call payment, email, SMS, search indexing, or AI endpoints without stubbing or approval.
- Test data creates real orders or irreversible records.
- Cleanup is not planned.

Why it hurts:

- Tests can cost money, contact users, pollute analytics, or corrupt business data.

Do instead:

- Use sandbox vendors, test tenants, idempotency keys, and cleanup plans.
- Exclude destructive flows unless the question requires them and approval is explicit.

