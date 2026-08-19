# Commit Writer Examples

Use these examples to calibrate grouping, message specificity, and when a body is useful.

## Example 1: Mixed Working Tree

### Input

`git status` shows:

- `src/auth/logout.ts`
- `src/auth/logout.test.ts`
- `src/payments/webhook.ts`
- `src/payments/webhook.test.ts`
- `.prettierrc`
- many formatted files under `src/`
- `README.md`

Diff facts:

- Logout now clears the refresh-token cookie on server-side logout.
- Payment webhook now ignores duplicate provider events by idempotency key.
- `.prettierrc` changed quote style and touched many files.
- `README.md` fixes a setup typo unrelated to auth or payments.

### Weak Output

```text
update files
```

### Why This Is Weak

- It hides four separate reasons for change.
- It cannot be used for release notes or debugging history.
- It makes revert risk higher because unrelated changes are bundled.

### Strong Output

````md
## Proposed Commits

### 1. Clear logout session state
**Files:** `src/auth/logout.ts`, `src/auth/logout.test.ts`

```text
fix(auth): clear refresh cookie on logout
```

### 2. Make payment webhooks idempotent
**Files:** `src/payments/webhook.ts`, `src/payments/webhook.test.ts`

```text
fix(payments): ignore duplicate webhook events

Prevents provider retries from applying the same payment transition more than once.
```

### 3. Apply formatter configuration
**Files:** `.prettierrc`, formatted source files

```text
style: apply updated prettier quote style
```

### 4. Fix setup documentation typo
**Files:** `README.md`

```text
docs: fix setup command typo
```

Approve all, or tell me which message/group to adjust before I commit.
````

### Why This Is Strong

- Tests stay with the runtime changes they prove.
- Formatting churn is isolated from behavior.
- The payment body explains the risk that is not obvious from the subject alone.
- The user can approve or adjust before history changes.

## Example 2: Breaking Configuration Change

### Input

A diff removes the fallback that used `development` when `APP_ENV` was unset. The app now fails startup unless `APP_ENV` is explicitly set. Deployments and local setup must change.

### Weak Output

```text
refactor(config): clean up environment handling
```

### Why This Is Weak

- It says `refactor` even though behavior changes.
- It hides the deployment action required from users.
- It gives no warning to release tooling that reads commit metadata.

### Strong Output

```text
fix(config)!: require explicit app environment

Failing fast prevents deployments from silently booting with development settings when `APP_ENV` is missing.

BREAKING CHANGE: `APP_ENV` must be set before startup. Local scripts and deployments need to provide `development`, `staging`, or `production` explicitly.
```

### Why This Is Strong

- The `!` makes the breaking surface visible.
- The body explains the safety reason for the behavior change.
- The footer tells operators exactly what must change.

## Example 3: Small Clean Commit

### Input

Diff changes one validation branch so expired refresh tokens are rejected with the same auth error used elsewhere. A focused regression test is included.

### Strong Output

```text
fix(auth): reject expired refresh tokens
```

### Why This Is Strong

- The subject names the user-visible bug.
- No body is needed because the diff and test explain the fix.
- The scope matches a real project area.

## Type Calibration

Use:

- `feat(api): add cursor pagination to invoices` when callers receive a new capability.
- `fix(api): preserve invoice filters during pagination` when behavior was wrong.
- `refactor(api): share invoice query builder` when output is intentionally unchanged.
- `perf(api): batch invoice total lookup` when the change is meant to improve measured performance.
- `build(deps): update vite to 6.1.0` when dependency tooling changes.

The subject should explain intent without requiring the reader to open the diff.
