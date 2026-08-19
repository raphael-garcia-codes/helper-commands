# Migration Helper Checklist

Use this checklist before planning or executing schema, data, framework, library, runtime, platform, or contract migrations.

## Classification

- [ ] Migration type is named: schema/data, framework/library, runtime/platform, or service/API contract.
- [ ] Current version or state is confirmed.
- [ ] Target version or state is confirmed.
- [ ] The breaking surface is named before changes begin.
- [ ] The affected owners, consumers, or deployables are known.
- [ ] The migration is separate from unrelated feature or refactor work.
- [ ] If this is only behavior-preserving cleanup, hand off to `refactor-guide`.
- [ ] If this is only a safe patch/minor dependency update, hand off to `dependency-auditor`.

## Evidence Before Change

- [ ] Official migration guide or changelog was read.
- [ ] Known breaking changes were listed.
- [ ] Codemod availability was checked.
- [ ] Current tests covering affected behavior were identified.
- [ ] Test gaps were documented before changing code.
- [ ] Rollback point is clear for each stage.
- [ ] Verification command or manual check is defined for each stage.
- [ ] Local reproduction or baseline is captured when possible.

## Database Safety

- [ ] No database operation runs without explicit user permission.
- [ ] Database URL and environment are confirmed with the user before any DB action.
- [ ] Local environment is confirmed before local DB operations.
- [ ] Generated SQL is reviewed before execution.
- [ ] Additive changes happen before destructive changes.
- [ ] Column/table renames use expand-and-contract when existing data or code may depend on them.
- [ ] Backfills are batched for large tables.
- [ ] Lock risk is considered for indexes, constraints, type changes, and defaults.
- [ ] Non-blocking DDL is used when the database supports it.
- [ ] Contract/removal happens in a later stage after reads and writes have moved.
- [ ] Rollback accounts for data already moved, not just code revert.

## Framework and Library Upgrades

- [ ] Upgrade path follows official supported hops.
- [ ] Multiple major versions are not skipped unless the official guide supports it.
- [ ] Peer dependencies and plugins are upgraded together when required.
- [ ] Codemods are run before manual edits when official codemods exist.
- [ ] Codemod output is reviewed rather than trusted blindly.
- [ ] Breaking APIs are fixed by category where possible.
- [ ] Compatibility shims are temporary and have a removal stage.
- [ ] The upgrade is not mixed with unrelated modernization.

## Runtime and Platform Migrations

- [ ] Runtime minimums are checked against deployment targets.
- [ ] Container base image changes are scanned or verified when security matters.
- [ ] CI, local dev, and production runtime versions are aligned or caveated.
- [ ] Native dependencies and build tooling compatibility are checked.
- [ ] Environment variable changes are documented as breaking when required.
- [ ] Rollout order covers CI, staging, and production separately.
- [ ] Observability is available during rollout.

## Contract Migrations

- [ ] Consumers of API, event, CLI, or file contract changes are identified.
- [ ] New fields or endpoints are added before old ones are removed.
- [ ] Versioning, feature flags, or compatibility windows are planned when needed.
- [ ] Producers and consumers have an agreed deployment order.
- [ ] Contract tests or compatibility checks are included when available.
- [ ] Deprecation and removal timing are explicit.

## Stage Plan

- [ ] Each stage has one primary change.
- [ ] Each stage has rollback instructions.
- [ ] Each stage has verification steps.
- [ ] Each stage can be reviewed independently.
- [ ] High-risk stages are not batched for convenience.
- [ ] User permission is requested before DB, production, or irreversible actions.
- [ ] The final contract/removal stage happens only after compatibility is verified.

## Final Check

- [ ] The plan explains how to move forward safely.
- [ ] The plan explains how to stop safely.
- [ ] The plan names what cannot be rolled back cleanly.
- [ ] The migration leaves no permanent shim or dual-write path without a follow-up.
