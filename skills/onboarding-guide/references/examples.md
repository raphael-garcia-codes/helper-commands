# Onboarding Guide Examples

Use these examples to calibrate factual claims, flow tracing, and drift reporting.

## Example 1: API Project Onboarding Map

### Input

Repository facts found during scan:

- `package.json` contains `dev`, `build`, `test`, and `lint` scripts.
- `src/server.ts` creates the HTTP server.
- `src/routes/orders.ts` defines order routes.
- `src/services/orderService.ts` contains order business logic.
- `src/db/schema.ts` defines tables.
- `src/middleware/auth.ts` validates bearer tokens.
- `agent_docs/security.md` says the app uses secure HTTP-only cookie sessions.
- Tests live under `src/**/__tests__`.

### Weak Output

```text
This is a modern Node API with clean architecture. It uses authentication and a database. Run npm install and start coding.
```

### Why This Is Weak

- It claims "clean architecture" without evidence.
- It misses the documented security drift.
- It does not trace a real request.
- It gives no risk map for safe changes.

### Strong Output

```md
# Onboarding Guide — Orders API

## What this project does
This repository contains a Node HTTP API for order workflows. Evidence comes from `src/server.ts`, order routes in `src/routes/orders.ts`, and order domain logic in `src/services/orderService.ts`.

## Architecture overview
- Entry point: `src/server.ts` wires middleware and routes.
- Routing layer: `src/routes/orders.ts` receives HTTP requests and delegates order operations.
- Domain/service layer: `src/services/orderService.ts` applies order workflow rules.
- Data layer: `src/db/schema.ts` defines persisted data shape.
- Auth boundary: `src/middleware/auth.ts` validates bearer tokens before protected routes.

## Data flow traced
`POST /orders` enters through `src/routes/orders.ts`, passes authentication through `src/middleware/auth.ts`, validates request data in the route layer, calls `src/services/orderService.ts`, and persists through the schema-backed database layer.

## Key files
| File | Why it matters | Risk if changed carelessly |
|---|---|---|
| `src/server.ts` | Composes middleware and routes | High — route ordering or middleware changes can affect the whole API |
| `src/middleware/auth.ts` | Auth boundary for protected requests | High — can accidentally allow or block users globally |
| `src/routes/orders.ts` | HTTP contract for order operations | High — changes affect API callers |
| `src/services/orderService.ts` | Order business rules | High — can break lifecycle or persistence assumptions |
| `src/db/schema.ts` | Source of truth for persisted data shape | High — coordinate with migrations |

## Conventions detected
- Routes delegate business behavior to services. Evidence: `src/routes/orders.ts` calls `orderService`.
- Tests live near source under `__tests__`. Evidence: `src/**/__tests__`.
- Auth uses bearer tokens. Evidence: `src/middleware/auth.ts`.

## Setup
- Install: likely `npm install` because `package-lock.json` is present.
- Test: `npm test` from `package.json`.
- Build: `npm run build` from `package.json`.
- Lint: `npm run lint` from `package.json`.

## CLAUDE.md system
Existing `agent_docs/security.md` appears stale: it says sessions use secure HTTP-only cookies, but current code in `src/middleware/auth.ts` validates bearer tokens. Drift found: auth storage/transport docs need review before agents rely on them.

## Human input needed
[NEEDS INPUT — deploy target is not visible in repository files. Confirm staging/production hosting before documenting deployment.]
```

### Why This Is Strong

- Every major claim ties back to code evidence.
- It traces one real flow.
- It reports drift instead of overwriting existing docs.
- It labels unknown deploy knowledge as human input.

## Example 2: Placeholder Instead of Invented Intent

### Input

Code in `src/middleware/rateLimit.ts` enforces `100` requests per minute per API key. No docs explain why this number exists.

### Weak Output

```text
The app has a 100 requests/minute limit to control infrastructure costs and satisfy security requirements.
```

### Why This Is Weak

- The code proves the limit, not the business reason.
- Cost and security intent are invented.
- Future agents may preserve the wrong rule for the wrong reason.

### Strong Output

```md
## Detected rule
`src/middleware/rateLimit.ts` enforces 100 requests per minute per API key.

## Human input needed
[NEEDS INPUT — the repository shows the enforced limit, but not the business reason for choosing 100 requests/minute. Confirm whether this is a product, infrastructure, abuse-prevention, or temporary limit.]
```

### Why This Is Strong

- It captures the factual code behavior.
- It refuses to invent rationale.
- It gives a precise question for the human to answer.

## Key File Table Pattern

Use risk language that helps new contributors avoid regressions:

| File | Why it matters | Risk if changed carelessly |
|---|---|---|
| `src/lib/auth.ts` | Central auth/session validation | High — can accidentally allow or block users globally |
| `src/db/schema.ts` | Source of truth for persisted data shape | High — coordinate with migrations |
| `src/components/Button.tsx` | Shared UI primitive | Medium — visual regression across many screens |
| `scripts/seed.ts` | Local/dev data setup | Low — verify fixtures still match tests |
