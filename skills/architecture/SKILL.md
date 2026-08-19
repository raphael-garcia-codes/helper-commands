---
name: architecture
description: Evaluates system-level technical decisions and records the result as an ADR when the decision is significant enough to preserve.
---

# Architecture

## Hard Gate

- The request must be a still-open architecture decision, not an explanation of existing architecture.
- Read existing architecture context first: `agent_docs/architecture.md`, ADR folders such as `docs/adr/` or `docs/decisions/`, and any stack-specific rules.
- If the choice is low-risk, cheap to reverse, and affects only one local implementation detail, do not create a full ADR; provide a short note instead.

## Process

1. Define the decision question in one sentence and list the forces that make it non-trivial.
2. Research current options before recommending anything; do not assert framework, database, or cloud capabilities from memory when version/date matters.
3. Compare at least two real options using decision drivers that matter to this project: risk, reversibility, operational load, cost, security, performance, team familiarity, and blast radius.
4. Use the Nygard ADR shape with MADR-style Decision Drivers and Considered Options when the decision passes the significance gate.
5. Record the accepted trade-off honestly, including negative consequences and follow-up work.
6. Add a Mermaid component, sequence, or deployment diagram only when it clarifies structure that prose cannot explain quickly.
7. Store the ADR in the project's existing decision location. If none exists, propose `docs/decisions/0001-<title>.md` and ask before creating a new convention.

## References

- `references/checklist.md` — Read when deciding whether the choice deserves an ADR or when choosing the ADR sections.
- `references/examples.md` — Read when you need a concrete ADR structure or diagram pattern.
- `references/anti-patterns.md` — Read when the request smells like architecture theater, preemptive microservices, or a one-option decision.

## Out of scope

**vs. `agent_docs/architecture.md`:** that file holds settled permanent architecture context. This skill produces a new decision artifact; it may suggest a follow-up update, but it does not rewrite permanent context silently.

**vs. `onboarding-guide`:** onboarding-guide explains the existing system. This skill chooses between future options.

**vs. `api-design`:** api-design handles one endpoint or API contract. This skill handles system-level boundaries, storage, communication style, and deployment architecture.

**vs. `feature-planner`:** feature-planner breaks down implementation after the direction is clear. This skill decides the direction.

## Output format

```md
## ADR: [decision title]

**Status:** Proposed | Accepted | Superseded by ADR-XXXX
**Decision question:** [one sentence]

### Context
[Current constraints and why the decision matters]

### Decision Drivers
- [driver]

### Considered Options
1. [Option] — pros / cons
2. [Option] — pros / cons

### Decision Outcome
Chosen: [option], because [reasoning tied to drivers].

### Consequences
- Positive: ...
- Negative: ...
- Follow-up: ...
```
