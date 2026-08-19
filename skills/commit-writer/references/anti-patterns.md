# Commit Writer Anti-Patterns

Read this before proposing or creating commits. Remove anything that makes history less accurate, less reversible, or less trustworthy.

## 1. Writing From Memory

Bad signs:

- The message is based on the conversation instead of `git diff`.
- Staged and unstaged changes were not both reviewed.
- Untracked files are ignored.

Why it hurts:

- Commit history can claim a change that is not actually in the diff.
- Important user edits can be accidentally omitted or bundled.

Do instead:

- Inspect status, staged diff, unstaged diff, untracked files, and recent history first.
- Say when the working tree has unrelated changes you will not include.

## 2. Staged Equals Logical

Bad signs:

- Everything currently staged becomes one commit.
- Formatting churn, docs typos, and behavior fixes share a subject.
- The message is broad because the group is broad.

Why it hurts:

- Reverts become risky.
- Reviewers cannot tell which files are necessary for which behavior.

Do instead:

- Regroup by reason for change.
- Keep runtime code with its direct tests, and split unrelated concerns.

## 3. Vague Subject

Bad signs:

- `update files`
- `misc fixes`
- `changes`
- `work on api`

Why it hurts:

- The log stops being useful for debugging, release notes, and bisecting.
- The next engineer must open the diff to understand intent.

Do instead:

- Name the behavior or project area changed.
- Prefer `fix(auth): reject expired refresh tokens` over `fix auth`.

## 4. Fake Scope

Bad signs:

- `chore(misc): update stuff`
- `fix(general): handle error`
- A scope is invented only to satisfy a template.

Why it hurts:

- Fake scopes make filtering and release notes worse.
- They imply ownership that does not exist.

Do instead:

- Use a real module, package, feature, or domain.
- Omit the scope when no precise scope exists.

## 5. Body as Diff Summary

Bad signs:

- The body lists every file touched.
- The body repeats the subject in longer words.
- It explains what changed but not why.

Why it hurts:

- Long messages add noise without preserving intent.
- The useful reason gets buried.

Do instead:

- Use a body only for context, risk, rollout, or business reason.
- Let the diff explain mechanical details.

## 6. Hidden Breaking Change

Bad signs:

- A public API, CLI, config, schema, or environment requirement changes under `refactor` or `chore`.
- No `!` or `BREAKING CHANGE:` footer appears.
- The required user action is missing.

Why it hurts:

- Releases can ship without migration notes.
- Operators and users discover required changes at runtime.

Do instead:

- Mark the commit as breaking using the project's convention.
- Explain exactly what users or deployments must change.

## 7. Committing Without Approval

Bad signs:

- `git commit` runs immediately after writing a message.
- The user asked for a message but not for a commit.
- Proposed grouping is skipped.

Why it hurts:

- History changes before the user approves the boundary.
- User-owned work can be captured unintentionally.

Do instead:

- Present proposed groups and messages first.
- Commit or push only after explicit user approval.
