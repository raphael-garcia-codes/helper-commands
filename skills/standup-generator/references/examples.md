# Standup Generator Examples

Use these examples to calibrate grounded updates, blocker-first ordering, and concise detail.

## Example 1: Individual Async Update

### Input

Sources for yesterday:

- Git commits:
  - `fix(payments): ignore duplicate webhook events`
  - `test(payments): cover duplicate provider deliveries`
- PR #142 merged: "Make payment webhooks idempotent".
- PR #143 opened: "Add retry dashboard widgets".
- CI failed on PR #143 because staging API credentials are missing.
- User says they also helped review PR #141 for checkout copy.

### Weak Output

```text
Yesterday I worked on payments and dashboards. Today I will keep going. No blockers.
```

### Why This Is Weak

- It hides the real blocker.
- It omits PR numbers and concrete outcomes.
- It mixes sourced and user-reported activity.
- It says "no blockers" despite CI being blocked.

### Strong Output

```md
**Blocked:** PR #143 retry dashboard validation is waiting on staging API credentials.

**Shipped / Done:**
- Merged PR #142: made payment webhooks idempotent.
- Added regression coverage for duplicate provider event delivery.
- Reviewed PR #141 checkout copy updates (reported by user).

**In Progress / Today:**
- Continue PR #143 retry dashboard widgets once staging credentials are available.
- Re-run CI and validate webhook retry metrics after credentials are added.

**Risks / Notes:**
- Dashboard work can continue locally, but end-to-end validation depends on staging access.
```

### Why This Is Strong

- Blocker is first and names what can unblock it.
- Completed and in-progress work are separated.
- PR numbers make the update verifiable.
- User-reported context is labeled.

## Example 2: Team Digest

### Input

Sources for a team daily update:

- Ana: Ticket AUTH-22 moved to blocked; waiting for security review.
- Gabriel: PR #142 merged for webhook idempotency; PR #143 opened for retry dashboard.
- Bruno: PR #145 merged for checkout copy updates.
- Carla: ORDER-31 has 3 of 5 export test cases complete.
- No deploy happened yesterday.

### Strong Output

```md
## Team Standup — 2026-07-12

### Blockers
- Ana: AUTH-22 is blocked pending security review.
- Gabriel: PR #143 staging validation is waiting on API credentials.

### Shipped / Done
- Gabriel: PR #142 merged — payment webhook idempotency.
- Bruno: PR #145 merged — checkout copy updates.

### In Progress / Today
- Gabriel: continue retry dashboard widgets and rerun validation once staging is unblocked.
- Carla: finish ORDER-31 export tests; 3 of 5 cases are complete.

### Notes
- No deploy recorded for the window.
```

### Why This Is Strong

- It preserves attribution.
- It avoids listing every commit.
- It includes a useful "no deploy" note because deploy status was part of the source context.
- It does not invent a team-wide conclusion.

## Example 3: Sparse Activity

### Input

No commits, no PRs, and no ticket changes were found for the requested window. The user did not provide extra context.

### Strong Output

```md
**Blocked:** None found in available sources.

**Shipped / Done:**
- No activity found for this window.

**In Progress / Today:**
- No sourced next work available.
```

### Why This Is Strong

- It does not pad a quiet day.
- It distinguishes "none found" from a proven absence of work.
- It keeps the update short.

## Specificity Calibration

Prefer:

- "Merged PR #142: made payment webhooks idempotent."
- "Completed 3 of 5 checkout endpoints; refund and admin override remain."
- "Blocked on staging database access from DevOps."

Avoid:

- "Worked on the API."
- "Made progress on tests."
- "Waiting on some stuff."
- "No blockers" when source access was incomplete.
