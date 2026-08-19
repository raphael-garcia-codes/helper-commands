---
name: standup-generator
description: Generates grounded async or live standup updates from real commits, PRs, tickets, and explicitly reported context.
---

# Standup Generator

## Hard Gate

- Gather actual activity before writing: git, PRs, issues/tickets, and any user-reported context.
- Do not invent progress, blockers, decisions, or intent not supported by the sources.
- Lead with blockers unless an established team template clearly requires another order.

## Process

1. Determine the time window and whether the output is individual, team digest, async, or live talking points.
2. Collect commits, PRs, reviews, and ticket status changes for that window.
3. Separate sourced activity from user-reported context that is not visible in tools.
4. Write blockers first, then in-progress/shipped/next work depending on team convention.
5. Use concrete nouns, counts, PR numbers, ticket IDs, and statuses when available.
6. Keep it short: 3-5 bullets per section is a ceiling, not a goal.
7. For team digests, preserve attribution or structure by board/status if that is how the team works.

## References

- `references/checklist.md` — Read before collecting sources or choosing async vs. live format.
- `references/examples.md` — Read for blockers-first, team digest, and specific-vs-vague examples.
- `references/anti-patterns.md` — Read when activity is sparse or the update risks sounding padded.

## Out of scope

**vs. `commit-writer`:** this skill reads commit history to write status. It does not create commits.

**vs. `pr-writer`:** this skill may mention PRs as progress. It does not write PR titles/descriptions for review.

## Output format

```md
**Blocked:** [specific blocker or None]

**Shipped / Done:**
- [specific sourced item]

**In Progress / Today:**
- [specific next item]

**Risks / Notes:**
- [only if real]
```
