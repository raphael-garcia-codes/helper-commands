---
name: api-design
description: Designs or reviews API endpoints — REST or otherwise — for consistency, correct use of HTTP semantics, and alignment with this project's existing API conventions. Use when adding a new endpoint, designing an API, or reviewing an API's shape.
---

# API Design

## Process

1. Check for existing API conventions in this project first (naming pattern, error response shape, versioning, auth pattern) — a new endpoint should extend the existing contract, not introduce a new dialect.
2. Research current, real best practices for the API style/framework in use (REST conventions, GraphQL schema design, gRPC, etc.) rather than assuming — recommended patterns and framework idioms shift over time.
3. Get the fundamentals right before anything else:
   - Correct HTTP methods and status codes for the operation (not everything is a 200; know when to use 201 for created, 204 for no content, 422 for validation failures vs 400 for malformed requests, 409 for conflicts)
   - Consistent, predictable resource naming (plural nouns, no verbs in URLs)
   - A consistent error response shape across all endpoints, not ad hoc per-endpoint. If this project doesn't already have an established error format, RFC 9457 (`application/problem+json`, with `type`/`title`/`status`/`detail`/`instance` fields) is the current standard reference — machine-readable and human-readable in the same envelope, rather than inventing a bespoke shape.
   - Pagination for anything that returns a list, unless the project deliberately doesn't need it. For large or frequently-changing datasets, cursor-based pagination is the current default recommendation over offset-based, since offset pagination degrades at scale and can skip or duplicate items when rows are inserted between page requests.
4. Design for the contract, not just the current implementation — think about what happens on partial failure, what fields are actually required vs optional, and what a breaking vs non-breaking future change would look like.
5. If this project has `agent_docs/security.md`, check whether the new endpoint touches anything documented there (auth requirements, PII, rate-sensitive operations) and apply those requirements explicitly.
6. For mutating or duplicate-sensitive operations (especially create/payment-like POSTs), define authz and idempotency expectations in the contract — who may call it, and what a retried identical request returns.
7. Validate input at the boundary — don't let unvalidated data reach business logic.

## What NOT to do

- Don't introduce a new response shape or error format when the project already has an established one, even if you'd personally prefer a different pattern.
- Don't skip input validation because "the frontend already validates it" — the API boundary is the actual trust boundary.
- Don't overfit the API shape to the current frontend's exact needs if that makes the contract awkward for any other future consumer.
- Don't recommend outdated REST conventions (e.g. verbs in URLs, inconsistent pluralization) without checking what's current practice for this stack.

## Out of scope

This skill operates at the level of a single endpoint or API contract — naming, HTTP semantics, extending this project's existing conventions. A decision about system-level structure (service boundaries, data store choice, sync vs. async communication, monolith vs. microservices) is `architecture` (Upsell 1), not this skill. A new endpoint that fits existing conventions is this skill; a decision about how services should communicate at all is architecture.

## Output format

The endpoint design/implementation, plus a short note on the request/response contract (method, path, status codes, error shape) if it's a new endpoint being proposed rather than existing code being reviewed.

See the anchor install references for checklists, examples, and failure modes: `references/checklist.md`, `references/examples.md`, and `references/anti-patterns.md`.
