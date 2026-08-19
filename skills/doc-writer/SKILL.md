---
name: doc-writer
description: Writes and updates code documentation — docstrings, README sections, and inline comments for non-obvious logic. Use when the user asks to document a function, update a README, add comments, or explain code for other developers.
---

# Doc Writer

## Process

1. Determine what's actually being documented: a function/module (docstrings), a project overview (README), or a specific tricky piece of logic (inline comment) — each has a different job and shouldn't be handled the same way.
2. Read the current implementation (and relevant call sites) before writing — document observed behavior, not remembered or intended behavior.
3. For docstrings: state what the function does, its parameters, return value, and any non-obvious behavior (side effects, exceptions raised, when it returns null/None). Follow this language's documentation convention (JSDoc, docstrings, godoc, etc.) rather than inventing a format. Prioritize the **contract** over the mechanics — what a caller needs to know before using this safely (preconditions, side effects, error cases) matters more than a step-by-step narration of the implementation, which changes independently of the contract and goes stale faster.
4. For a README: lead with what the project does and how to run it — setup, install, and run commands are the highest-value section, above architecture explanations.
5. For inline comments: only comment the *why*, not the *what*. If the code is self-explanatory, it doesn't need a comment; if a line looks wrong at first glance but is deliberate (a workaround, an edge case, a non-obvious ordering requirement), that's exactly what deserves a comment.
6. Check whether existing docs elsewhere in the project already cover this — update them instead of creating a duplicate, conflicting source of truth.

## What NOT to do

- Don't write a comment that just restates the code in English (`// increment counter` above `counter++`) — this adds noise without adding information.
- Don't document implementation details likely to change soon inside a docstring meant for external consumers — that belongs in an inline comment or not at all.
- Don't write documentation that will silently go stale — prefer linking to the single source of truth (e.g. a schema file) over duplicating details that could drift out of sync.
- Don't pad a README with sections no one will read (elaborate badges, verbose philosophy) at the expense of the setup instructions someone actually needs.

## Out of scope

This skill documents specific code that already exists or was just changed — a function, a file, a README section. Analyzing an entire unfamiliar codebase to produce a structural map and a starter CLAUDE.md system is `onboarding-guide` (Upsell 1), not this skill — that's project scope, not file scope.

## Output format

The documentation itself, written directly into the target file/location — not a summary of what documentation should say.

See the anchor install references for checklists, examples, and failure modes: `references/checklist.md`, `references/examples.md`, and `references/anti-patterns.md`.
