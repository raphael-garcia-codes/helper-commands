# Migration Helper Examples

Use these examples to calibrate staged planning, rollback realism, and permission boundaries.

## Example 1: Rename a Production Column

### Input

The app stores users in a `users` table. Code currently reads and writes `user_name`. Product wants the field renamed to `username`. The table has production data and multiple application instances. Downtime is not acceptable.

### Weak Output

```text
Rename `user_name` to `username` in the migration and update all code references.
```

### Why This Is Weak

- It performs a destructive contract change in one deploy.
- It assumes all application instances switch at the same time.
- It gives no rollback path after data shape changes.
- It ignores lock and backfill risk.

### Strong Output

```md
## Migration Plan: `users.user_name` -> `users.username`

**Type:** schema/data
**Compatibility surface checked:** application reads, writes, serializers, tests, and generated SQL.
**Safety net:** targeted user profile tests plus staged deploy verification.

### Permission Needed
Before any database operation, confirm the target database URL and environment. Do not run this on production without explicit approval.

### Stage 1 — Expand schema
- Change: add nullable `username` column while keeping `user_name`.
- Rollback: drop `username` if no application code has started using it.
- Verification: inspect schema and confirm existing reads still use `user_name`.

### Stage 2 — Dual-write
- Change: update code to write both `user_name` and `username`; reads still prefer `user_name`.
- Rollback: revert code; the extra column remains harmless.
- Verification: create/update a test user and confirm both fields are populated.

### Stage 3 — Backfill
- Change: copy `user_name` into `username` in batches.
- Rollback: stop the backfill; do not clear `username` unless the copied data is known to be wrong.
- Verification: compare counts where `user_name` is not null and `username` is null.

### Stage 4 — Switch reads
- Change: read from `username`, with temporary fallback to `user_name` during rollout.
- Rollback: restore reads from `user_name`.
- Verification: profile and API tests pass with records created before and after the backfill.

### Stage 5 — Contract
- Change: stop writing `user_name`, remove fallback, and drop `user_name` in a later migration after rollout is verified.
- Rollback: restore fallback before dropping the old column; after drop, rollback requires a restore or reverse migration from `username`.
- Verification: no code references `user_name`; schema and tests confirm final state.
```

### Why This Is Strong

- It separates expand, migrate, and contract stages.
- It does not run database work without permission and environment confirmation.
- It treats rollback differently before and after destructive steps.
- It supports rolling deploys.

## Example 2: Framework Major Upgrade

### Input

A Next.js app needs to move from version 13 to 15. The app uses custom middleware, server components, image config, and a few deprecated APIs. Tests include typecheck, unit tests, and one Playwright smoke path.

### Strong Output

```md
## Migration Plan: Next.js 13 -> 15

**Type:** framework/library
**Compatibility surface checked:** official Next.js 14 and 15 migration guides, React peer requirements, middleware behavior, image config, and server component usage.
**Safety net:** typecheck, unit tests, build, and Playwright smoke path.

### Stage 1 — Prepare on current version
- Change: remove deprecated APIs that already have compatible replacements in Next.js 13.
- Rollback: revert the cleanup commit.
- Verification: typecheck, unit tests, and build.

### Stage 2 — Upgrade to Next.js 14
- Change: update Next.js and required peer dependencies, run official codemods, review codemod output.
- Rollback: revert dependency and codemod commits.
- Verification: typecheck, unit tests, build, and smoke path.

### Stage 3 — Fix 14-specific breakage
- Change: address middleware and config changes by category.
- Rollback: revert category commits individually.
- Verification: affected route tests and smoke path.

### Stage 4 — Upgrade to Next.js 15
- Change: update dependencies, run official codemods, resolve remaining breaking APIs.
- Rollback: revert the version-hop commit before adding unrelated changes.
- Verification: full suite, production build, smoke path, and key runtime logs.

### Stage 5 — Remove temporary compatibility code
- Change: delete shims added only for the migration.
- Rollback: restore shim commit if any late path still depends on it.
- Verification: same suite as Stage 4.
```

### Why This Is Strong

- It moves one major version at a time.
- It runs official codemods before hand-editing everything.
- It keeps cleanup and upgrade work reviewable.
- It has verification after every stage.

## SQL Pattern Examples

Use database-specific non-blocking operations when available:

```sql
CREATE INDEX CONCURRENTLY idx_orders_customer_id ON orders(customer_id);

ALTER TABLE orders ADD CONSTRAINT orders_customer_id_nn CHECK (customer_id IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_customer_id_nn;
ALTER TABLE orders ALTER COLUMN customer_id SET NOT NULL;
```

These are examples to review, not commands to run blindly. Always confirm the database engine, target environment, and permission before execution.
