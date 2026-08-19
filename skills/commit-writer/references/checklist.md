# Commit Writer Checklist

Use this checklist before proposing commit groups, commit messages, or any history-changing command.

## Required Evidence

- [ ] `git status` was reviewed for staged, unstaged, and untracked files.
- [ ] Staged diff was reviewed, not only file names.
- [ ] Unstaged diff was reviewed so accidental omissions are visible.
- [ ] Untracked files were classified as relevant, generated, local-only, or unknown.
- [ ] Recent commit history was checked for project style.
- [ ] Repository guidance was checked when present: `CLAUDE.md`, `AGENTS.md`, rules, contribution docs, or release docs.
- [ ] Lockfiles and generated files were understood before including them.
- [ ] Secrets, `.env`, credentials, local databases, and machine-specific files were excluded unless the user explicitly requested and accepted the risk.
- [ ] The message is based on the diff, not on chat memory.

## Commit Grouping

- [ ] Each proposed commit has one reason to exist.
- [ ] Runtime code and its direct tests stay together when the tests prove that change.
- [ ] Migration files stay with the code they require when they cannot work independently.
- [ ] Documentation stays with code only when it documents that exact behavior change.
- [ ] Feature work is separated from bug fixes when either can be reverted independently.
- [ ] Formatting-only churn is separated from meaningful behavior changes.
- [ ] Dependency or build-system changes are separated unless required by the same logical fix.
- [ ] Generated artifacts are grouped with the generator/config change that produced them.
- [ ] Unrelated README typos, comments, or cleanup are not bundled into product changes.
- [ ] Files are not grouped merely because they are already staged together.

## Message Style

- [ ] Local convention wins over Conventional Commits.
- [ ] If no local convention exists, use `type(scope): description`.
- [ ] Subject uses imperative present tense: `fix`, `add`, `remove`, `rename`, `update`.
- [ ] Subject is lowercase after the type unless a proper noun is required.
- [ ] Subject has no trailing period.
- [ ] Scope is a real module, package, feature, or domain.
- [ ] Scope is omitted when no meaningful scope exists.
- [ ] Body is included only when it explains why, risk, rollout, or business impact.
- [ ] Body does not restate the diff file by file.
- [ ] Footer is used for breaking changes, issue links, or required metadata when the project expects it.

## Type Selection

- [ ] `feat` is used for a new user-visible or API-visible capability.
- [ ] `fix` is used for a bug or regression correction.
- [ ] `docs` is used for documentation-only changes.
- [ ] `test` is used for adding or correcting tests without changing runtime behavior.
- [ ] `refactor` is used for behavior-preserving structure changes.
- [ ] `perf` is used only for measured or intentionally performance-focused improvements.
- [ ] `build` is used for dependencies, package managers, bundlers, or build config.
- [ ] `ci` is used for CI workflows and automation.
- [ ] `chore` is reserved for maintenance that does not fit a more precise type.
- [ ] `style` is used only if the project uses it for formatting-only changes.

## Breaking Changes

- [ ] External API behavior changes are marked breaking.
- [ ] CLI flags, output shape, exit codes, or config requirements are marked breaking.
- [ ] Persisted data shape or migration expectations are marked breaking when users must act.
- [ ] Environment/runtime minimums are marked breaking when deployments must change.
- [ ] The subject uses `!` when the project accepts Conventional Commits.
- [ ] `BREAKING CHANGE:` footer explains the required user action.
- [ ] Breaking changes are not hidden in a normal `refactor` or `chore` commit.

## Approval and Execution

- [ ] Proposed commit groups are shown before committing.
- [ ] The user explicitly approved committing before any `git commit` command.
- [ ] The user explicitly approved pushing before any `git push` command.
- [ ] If hooks modify files, the new diff is reviewed before continuing.
- [ ] If a commit fails, the issue is fixed and a new commit attempt is made.
- [ ] The final status is checked after committing.

## Final Check

- [ ] The message would still make sense in six months.
- [ ] The subject describes the intent, not just the touched file.
- [ ] Reverting one proposed commit would not accidentally revert unrelated work.
- [ ] The grouping respects user changes already present in the working tree.
