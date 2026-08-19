---
name: pr-writer
description: Writes pull request titles and descriptions from the actual diff and commit history. Use when the user asks to open a PR, write a PR description, or prepare changes for review.
---

# PR Writer

## Process

1. Read the actual diff (`git diff main...HEAD` or equivalent) and the commit history for this branch — don't write from memory of the conversation, since the conversation and the diff can drift apart.
2. Check this project's PR conventions: look for a `.github/pull_request_template.md`, and check CLAUDE.md's PR & Commit Rules or Workflow Rules section for format expectations (title format, required sections, linked issues).
3. Write a title that states what changed, following this project's commit/PR convention if one exists (e.g. Conventional Commits style) — not a generic restatement of the branch name.
4. Write a description covering:
   - **What** changed and **why** — the why matters more; a reviewer can read the diff for what.
   - **How to test/verify** — concrete steps, not "tested locally."
   - **Anything a reviewer should pay special attention to** — a risky change, a deliberate trade-off, something intentionally left out of scope.
   Keep the full description roughly 200–400 words. Shorter tends to leave reviewers without enough context; longer buries the details that matter — if the change genuinely needs more, that's a signal the PR itself may be too large to review well.
5. If the diff touches a business rule documented in `agent_docs/business-rules.md`, note that explicitly so the reviewer knows to check it carefully.
6. If the branch has messy or WIP-style commits, summarize the net change rather than narrating the commit-by-commit history.

## What NOT to do

- Don't write a PR description before reading the actual diff — a description based on what you remember discussing often misses what actually got written.
- Don't pad the description with a restated checklist of files changed; that's redundant with the diff view itself.
- Don't claim testing was done that wasn't — if tests weren't run, say what verification is still needed instead.
- Don't write in first person as if you personally made the decision ("I decided to...") — write as a neutral description of the change.

## Out of scope

This skill writes a PR title and description from commits that already exist on a branch, once it's ready for review. Writing the commit messages themselves, before anything is pushed, is `commit-writer` (Upsell 1), not this skill.

## Output format

```
## Title
[title]

## Description
### What & Why
...

### How to Test
...

### Notes for Reviewers
...
```

Omit the Notes section if there's genuinely nothing to flag.

**Example title:** `feat(billing): add prorated refunds for mid-cycle downgrades`

See the anchor install references for checklists, examples, and failure modes: `references/checklist.md`, `references/examples.md`, and `references/anti-patterns.md`.
