---
name: test-generator
description: Writes tests for existing code, covering realistic edge cases and following this project's testing conventions. Use when the user asks to add tests, improve test coverage, or write tests for a specific function or file.
---

# Test Generator

## Process

1. Check `agent_docs/engineering-standards.md` and CLAUDE.md's Testing/Commands section for this project's test framework, conventions, and how tests are run — don't assume a default that may not match.
2. Read the code being tested closely enough to understand its actual behavior and contracts, not just its signature — tests written from the signature alone tend to test the happy path only.
3. Test through the public interface, not internal implementation details. A well-named test reads like a spec of a capability ("user can check out with an expired coupon") and should survive a refactor that doesn't change behavior — if renaming a private variable breaks the test, it was testing the wrong layer.
4. Cover, in priority order:
   - The core expected behavior (the reason the function exists).
   - Realistic edge cases: empty/null input, boundary values, the failure paths the code explicitly handles.
   - Regression cases, if this is testing a bug fix — the exact scenario that used to fail.
5. Prefer real behavior over mocks where practical. Mock external dependencies (network, database, time) that would make the test slow or flaky, not internal logic that's cheap to exercise directly — over-mocking hides real bugs.
6. Control non-deterministic values explicitly — injected/mocked timestamps, seeded random values, fixed UUIDs — rather than letting a test depend on real time or randomness. This is one of the most common causes of tests that pass locally and fail intermittently in CI.
7. Name tests so a failure is understandable from the test name alone, without needing to read the assertion.
8. Run the tests after writing them and confirm they actually pass against the current code (and, for a bug-fix regression test, that they'd fail against the old code).

## What NOT to do

- Don't write tests that only assert a function was called (mock-checking) when testing the actual output is possible and more meaningful.
- Don't pad coverage with trivial tests (e.g. testing that a constant equals itself) — coverage percentage isn't the goal, catching real breakage is. A large number of low-value tests ("test explosion") slows down the whole suite without improving defect detection — fewer, well-targeted tests beat many shallow ones.
- Don't skip the failure/edge cases because the happy path is what's easy to write.
- Don't leave tests you wrote unrun — always execute them before considering the task done.

## Out of scope

This skill writes tests for functional correctness — does the code do the right thing. Testing behavior and capacity under simulated concurrent traffic is `load-tester-advisor` (Upsell 1), not this skill — a load test assumes the functional tests already pass; it isn't a substitute for them.

## Output format

The test file itself, plus a short summary: what's covered, what edge cases were included, and any gap you couldn't cover with a note on why (e.g. requires a live integration you don't have access to).

See the anchor install references for checklists, examples, and failure modes: `references/checklist.md`, `references/examples.md`, and `references/anti-patterns.md`.
