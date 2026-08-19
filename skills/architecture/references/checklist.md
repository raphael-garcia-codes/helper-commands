# Architecture Checklist

Use this checklist after `SKILL.md` when deciding whether to create an ADR and when shaping the decision record.

## Scope Gate

- [ ] The request is about a still-open decision, not a summary of existing architecture.
- [ ] The decision question can be written in one sentence.
- [ ] The choice affects more than one local implementation detail.
- [ ] The decision has meaningful risk if reversed later.
- [ ] The decision affects a quality attribute: security, reliability, performance, scalability, cost, operability, or maintainability.
- [ ] The decision changes a boundary between components, services, packages, teams, or data owners.
- [ ] The decision introduces or removes a durable dependency: datastore, protocol, vendor, queue, framework, runtime, or hosting model.
- [ ] Stakeholders outside the current implementer would care about the outcome.
- [ ] If the choice is cheap to reverse, a short implementation note is enough.

## Context Discovery

- [ ] Existing ADRs or decision records were read before proposing a new decision.
- [ ] `agent_docs/architecture.md` or equivalent permanent architecture context was checked when present.
- [ ] Current code structure was inspected instead of relying on repository names.
- [ ] Relevant runtime, framework, database, and cloud versions were confirmed.
- [ ] Existing constraints were separated from preferences.
- [ ] Current pain points were tied to evidence: incidents, metrics, team workflow, cost, or known defects.
- [ ] Assumptions that need human confirmation are explicitly labeled.
- [ ] The decision does not silently contradict an accepted ADR.

## Decision Drivers

- [ ] Drivers are specific to this project, not generic "scalable" or "modern" claims.
- [ ] Drivers are ordered when some matter more than others.
- [ ] Reversibility is included when rollout risk is material.
- [ ] Operational ownership is included when a new service, datastore, queue, or vendor is proposed.
- [ ] Security and compliance constraints are included when data boundaries or auth behavior change.
- [ ] Cost is included when vendor, infrastructure, storage, or traffic volume changes.
- [ ] Team familiarity is included when the chosen option requires new skills.
- [ ] Performance is included only when there is a concrete throughput, latency, or resource concern.

## Options

- [ ] At least two real options are compared.
- [ ] Each option is something a reasonable team could choose.
- [ ] The current approach is included when keeping it is viable.
- [ ] Strawman options are removed.
- [ ] Pros and cons are tied to the decision drivers.
- [ ] Migration cost is described for options that require moving existing code or data.
- [ ] Operational burden is described for options that add deployables or infrastructure.
- [ ] Unknowns are called out instead of being hidden.

## Recommendation

- [ ] The chosen option is named clearly.
- [ ] The reason references the strongest drivers.
- [ ] The rejected options are not dismissed with vague language.
- [ ] The decision is explicit about what will not be done.
- [ ] The recommendation includes the smallest viable rollout path.
- [ ] The ADR records both positive and negative consequences.
- [ ] Follow-up work is concrete and owned by implementation, verification, or operations.
- [ ] If external facts may expire, the ADR includes a date or verification note.

## Diagram Use

- [ ] A diagram is included only when it clarifies structure faster than prose.
- [ ] Component diagrams show ownership and dependency direction.
- [ ] Sequence diagrams show cross-boundary request, event, or retry flow.
- [ ] Deployment diagrams show runtime placement only when deployment is part of the decision.
- [ ] Diagrams avoid decorative detail that does not affect the decision.
- [ ] Diagram labels match terms used in the ADR.

## ADR Hygiene

- [ ] The title is decision-shaped: `Use X for Y`, not `Architecture notes`.
- [ ] Status is one of the project's existing statuses or a simple `Proposed` / `Accepted`.
- [ ] Storage location follows the project convention.
- [ ] If no convention exists, a new ADR folder is proposed before creating it.
- [ ] Superseded decisions are linked when applicable.
- [ ] The ADR can be understood without reading the chat that produced it.
- [ ] The ADR does not include unrelated implementation tickets.

## Final Check

- [ ] A future engineer can see why this choice was made.
- [ ] A future engineer can see what trade-off was accepted.
- [ ] A future engineer can tell when the decision should be revisited.
- [ ] The output is useful even if the recommendation is rejected.
