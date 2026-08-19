# Architecture Anti-Patterns

Read this before publishing an ADR or architecture recommendation. Remove anything that makes the decision look more certain, larger, or more strategic than the evidence supports.

## 1. Architecture Theater

Bad signs:

- An ADR is written after the implementation is already settled.
- The document exists to satisfy process, not to preserve a real decision.
- The output uses formal sections but contains no trade-off.

Why it hurts:

- Future readers cannot tell what was actually decided.
- The ADR system becomes noise and stops being consulted.

Do instead:

- If the choice is already settled, document it as current context.
- Create an ADR only when a meaningful future choice remains open or needs ratification.

## 2. One Real Option

Bad signs:

- One preferred option is detailed and the alternatives are obvious strawmen.
- Options are named but not compared against the same drivers.
- "Do nothing" is omitted even though keeping the current design is possible.

Why it hurts:

- The recommendation cannot be challenged intelligently.
- The team may accept an expensive change without seeing the lower-risk path.

Do instead:

- Compare at least two options a reasonable team could choose.
- Include the current design when it is still viable.

## 3. Microservices by Default

Bad signs:

- A service split is proposed before bounded context, team ownership, or deployment needs are clear.
- The recommendation talks about scale without current traffic, reliability, or delivery evidence.
- Network, observability, versioning, and incident ownership are not discussed.

Why it hurts:

- The team inherits distributed-system failure modes without a matching benefit.
- Local development, testing, and rollout become harder.

Do instead:

- Consider modular monolith boundaries, workers, queues, or package separation first.
- Split services only when ownership, scaling, isolation, or lifecycle drivers justify it.

## 4. Database Category Thinking

Bad signs:

- The decision says "use NoSQL for scale" or "use Postgres because it is reliable" without access patterns.
- Query shapes, consistency needs, backup expectations, and team experience are missing.
- The database is chosen for a future hypothetical feature.

Why it hurts:

- The chosen store may fit the label but not the workload.
- Operational and migration cost can exceed the feature benefit.

Do instead:

- Start with read/write patterns, consistency requirements, data volume, retention, and recovery expectations.
- Choose the simplest store that satisfies the known workload and leaves a clear extension path.

## 5. Ignoring Migration Cost

Bad signs:

- The recommendation only describes the target state.
- Existing data, API consumers, deployment order, and rollback are absent.
- The migration is treated as a minor implementation detail.

Why it hurts:

- A technically better architecture can fail because the path to reach it is unsafe.
- Teams underestimate downtime, compatibility, and support burden.

Do instead:

- Include rollout shape, compatibility needs, and rollback constraints in consequences.
- Let migration risk influence the decision outcome.

## 6. Benefit-Only Consequences

Bad signs:

- Consequences list only positives.
- Costs are softened into vague phrases like "some complexity".
- Follow-up obligations are not named.

Why it hurts:

- Future engineers cannot see what trade-off was accepted.
- The team may forget to fund monitoring, ownership, documentation, or cleanup.

Do instead:

- Record positive, negative, and follow-up consequences.
- Be specific: "requires queue dead-letter monitoring" is better than "adds operational work".

## 7. Decision Without Drivers

Bad signs:

- The recommendation relies on taste: modern, clean, robust, enterprise-ready.
- Drivers are generic and could fit any project.
- The final choice does not reference the stated drivers.

Why it hurts:

- The decision cannot be revisited when circumstances change.
- Reviewers argue preferences instead of constraints.

Do instead:

- Name project-specific drivers and show how the chosen option wins.
- Note which driver was intentionally deprioritized.

