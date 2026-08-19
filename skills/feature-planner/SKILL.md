---
name: feature-planner
description: Use before writing implementation code for any new feature, non-trivial change, or task with unclear scope. Also use when the user says "help me plan," "how should I build this," "let's design this first," or describes an idea that isn't broken into concrete steps yet.
---

# Feature Planner

## Why this comes before coding

Letting an AI session jump straight into implementation is how you get a plausible-looking change that misses the actual point, touches files it shouldn't, or solves a subtly different problem than the one intended. A short planning pass catches this before any code exists to unwind.

## Process

1. **Understand before planning.** If the request is ambiguous or the scope is unclear, ask targeted questions first — what's in scope, what's explicitly out of scope, which existing files/patterns this should follow, and what "done" looks like. Don't guess at requirements that are cheap to just ask about.
2. **Check the project's actual context first.** Read `agent_docs/business-rules.md` for any domain rule this feature must respect, and `agent_docs/architecture.md` (if present) for existing structural decisions this plan needs to fit into rather than work against.
3. **Write a short plan, not a spec document.** Cover:
   - What's being built, in one or two sentences
   - The files/areas that will change
   - The approach, broken into small steps (each step should be independently verifiable — buildable and testable on its own, not a checkpoint that only makes sense once everything else is done)
   - What's explicitly out of scope for this pass
4. **Surface trade-offs and alternatives when there's a real decision to make** — e.g. a data-modeling choice, a library choice, a decision that's expensive to reverse later. Present the options plainly rather than silently picking one.
5. **Get confirmation on the plan before implementing**, if the change is non-trivial (multiple files, a new dependency, a schema change, anything touching a documented business rule). For a small, obvious change, this step can be skipped — use judgment.
6. Once the plan is confirmed, implement it step by step, checking off each step as it's verified working rather than writing everything at once and debugging at the end.

## What NOT to do

- Don't skip straight to a wall of code for anything with real ambiguity in scope or approach — the cost of a five-minute planning pass is far lower than the cost of a wrong implementation.
- Don't write a plan so detailed it becomes a second implementation effort in prose — keep it to what's needed to confirm direction and sequence.
- Don't silently pick between genuinely different valid approaches without surfacing the choice — that's a decision the user should make, not one to make for them.
- Don't treat this as required ceremony for trivial changes (a one-line fix, a typo, a well-specified small task) — apply it where ambiguity or risk actually exists.

## Out of scope

This skill plans implementation steps once the technical direction is reasonably clear. When step 4 (surfacing trade-offs) reveals a real, unresolved fork between fundamentally different technical approaches — not just an implementation detail — that's `architecture` (Upsell 1), which evaluates and formally records the decision; bring the outcome back here for the actual step-by-step plan.

## Output format

```
## Goal
[one or two sentences]

## Approach
1. [step] — [how to verify this step]
2. [step] — [how to verify this step]
...

## Out of scope
- ...

## Open questions / trade-offs (if any)
- ...
```

See the anchor install references for checklists, examples, and failure modes: `references/checklist.md`, `references/examples.md`, and `references/anti-patterns.md`.