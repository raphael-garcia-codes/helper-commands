---
name: migration-helper
description: Plans and executes database, framework, library, or platform migrations through staged, reversible steps.
---

# Migration Helper

## Hard Gate

- Classify the migration type before changing anything: schema/data, framework/library, runtime/platform, or service contract.
- Confirm tests or another safety net cover the affected behavior before execution.
- Never run database migrations, queries, or production-impacting operations without explicit user permission and environment confirmation.

## Process

1. Read current and target versions, official migration guides, changelogs, and codemod availability.
2. For schema/data changes, inspect row counts and lock risk before choosing an approach.
3. Plan expand -> migrate/backfill -> contract for data migrations unless downtime is explicitly acceptable.
4. For framework/library upgrades, move one or two major versions at a time and run official codemods first.
5. Write rollback and verification for each stage before executing it.
6. Execute one stage at a time and verify before moving on.
7. Keep migration work separate from unrelated refactors or feature changes.
8. Hand pure behavior-preserving restructure to `refactor-guide` if no version/contract boundary changes.

## References

- `references/checklist.md` — Read before planning stages, touching schema, or selecting upgrade hops.
- `references/examples.md` — Read for expand-contract, non-blocking DDL, codemod, and rollback examples.
- `references/anti-patterns.md` — Read before destructive schema changes, skipped major versions, or mixed-scope migrations.

## Out of scope

**vs. `refactor-guide`:** refactor-guide preserves external behavior and contracts. This skill changes a schema, version, platform, or contract and needs staged compatibility.

**vs. `dependency-auditor`:** dependency-auditor flags outdated/vulnerable packages and may apply safe patch/minor updates. This skill handles breaking major migrations.

## Output format

```md
## Migration Plan: [from] -> [to]

**Type:** [schema/data | framework/library | platform/runtime | contract]
**Compatibility surface checked:** [versions, guides, row counts, codemods, contracts]
**Safety net:** [tests/backup/rollback readiness]

### Stage 1 — [name]
- Change:
- Rollback:
- Verification:

### Stage 2 — [name]
- Change:
- Rollback:
- Verification:

### Permission Needed
[Only include when a DB operation, production action, or irreversible step is required.]
```
