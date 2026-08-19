---
name: refactor-guide
description: Use when the user asks to refactor, clean up, simplify, restructure, or improve existing code without adding new functionality. Also use when code has grown hard to follow, has duplication, or a function/file is doing too much and needs to be split.
---

# Refactor Guide

## Process

1. Confirm the scope: a refactor changes structure, not behavior. If the user's request actually includes new functionality or a behavior change, flag that distinction — it changes the risk profile and how to verify success.
2. **Establish a safety net before changing anything.** If tests exist for the code being refactored, run them first to confirm a clean baseline. If no tests exist for this code, say so and recommend adding characterization tests first for anything non-trivial — refactoring without a safety net is how silent regressions happen.
3. Identify the actual problem being solved (duplication, unclear responsibility, a function doing too much, tangled dependencies) rather than refactoring for its own sake — every refactor should have a concrete "this is better because—". A useful target: prefer deep modules — a lot of real behavior sitting behind a small, clear interface — over shallow ones with a large interface and little behavior behind it; if a refactor makes the interface bigger without the module doing meaningfully more, that's a sign it's moving in the wrong direction.
4. Make the change in small, verifiable steps rather than one large rewrite — each step should leave the code in a working state, runnable and testable. Check the size of the actual diff against the stated scope: if a refactor described as small or focused ends up touching a large number of files or lines, that's a signal the change has drifted beyond its intended scope, not a sign of thoroughness — pause and confirm the expanded scope was intentional before continuing.
5. After each step (or at the end, for a small refactor), run the existing tests and confirm they still pass with no behavior change.
6. If the refactor reveals a bug in the original code, don't fix it silently inside the refactor — flag it separately so it's a visible, reviewable decision rather than a hidden side effect.

## What NOT to do

- Don't refactor and change behavior in the same pass — that conflates two different kinds of risk and makes it hard to isolate what broke if something does.
- Don't do a large-scale rewrite when a series of small, verifiable steps would reach the same result more safely.
- Don't refactor code with no tests and no plan to verify it still works — "it looks equivalent" is not verification.
- Don't over-engineer the result — a refactor should make the code simpler and clearer, not introduce abstraction layers the codebase doesn't need yet.

## Out of scope

If the goal is to fix broken behavior, that's debugging, not refactoring — use debug-assistant instead. If the goal is to add new functionality, that's a feature — use feature-planner first, then implement. If the change is driven by a version, framework, or platform upgrade that changes the external contract on purpose, that's a migration, not a refactor — use `migration-helper` (Upsell 1) instead, since it plans compatibility and rollback in a way this skill's process doesn't.

## Output format

The refactored code, plus a short before/after note: what structural problem this addresses, what was verified (tests run, behavior confirmed unchanged), and anything flagged but deliberately left out of scope.

See the anchor install references for checklists, examples, and failure modes: `references/checklist.md`, `references/examples.md`, and `references/anti-patterns.md`.
