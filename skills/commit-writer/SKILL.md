---
name: commit-writer
description: Writes accurate commit messages and proposes atomic commit grouping from the real working tree state.
---

# Commit Writer

## Hard Gate

- Read `git status`, staged diff, unstaged diff, and recent commit history before writing a message.
- Do not commit or push unless the user explicitly asks and confirms the proposed grouping.
- If there are no changes, say so; do not invent a commit.

## Process

1. Identify this project's existing commit convention from `CLAUDE.md`, rules files, and recent `git log` before defaulting to Conventional Commits.
2. Group files by logical change, not by convenience. Separate unrelated formatting, docs, fixes, and features.
3. Use Conventional Commits only when no stronger local convention exists: `type(scope): description`.
4. Write the subject in imperative present tense, lowercase after the type, with no trailing period.
5. Add a body only when the diff does not explain the reason, risk, or business-rule impact.
6. Mark breaking changes with `!` and/or a `BREAKING CHANGE:` footer.
7. Present proposed commit groups for approval before running any history-changing command.

## References

- `references/checklist.md` — Read before proposing commit groups or when the diff mixes multiple concerns.
- `references/examples.md` — Read when choosing a type/scope/body or documenting a breaking change.
- `references/anti-patterns.md` — Read before committing when the diff is noisy, partly generated, or includes unrelated changes.

## Out of scope

**vs. `pr-writer`:** this skill writes local commit messages before the branch is ready for review. `pr-writer` summarizes an existing branch against its base for reviewers.

**vs. `standup-generator`:** standup-generator consumes commit and PR history to write a status update; it does not create git history.

## Output format

```md
## Proposed Commits

### 1. [short label]
**Files:** [paths]

```
type(scope): description

[body only if useful]
```

### 2. [short label]
**Files:** [paths]

```
type: description
```

Approve all, or tell me which message/group to adjust before I commit.
```
