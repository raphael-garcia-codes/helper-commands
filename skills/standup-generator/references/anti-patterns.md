# Standup Generator Anti-Patterns

Read this before publishing a standup update. Remove anything that is unsourced, padded, misclassified, or too detailed to help the team coordinate.

## 1. Memory Over Sources

Bad signs:

- The update is written from memory when git, PR, or ticket data is available.
- PR numbers and ticket IDs are omitted even though they exist.
- Recent comments or CI failures are not checked.

Why it hurts:

- Important blockers and shipped work can be missed.
- The update becomes less trustworthy than the source systems.

Do instead:

- Gather commits, PRs, tickets, and explicitly reported context first.
- Use source identifiers when available.

## 2. Padding a Quiet Window

Bad signs:

- A quiet day becomes vague activity like "continued improvements".
- Small or unrelated actions are inflated.
- The update invents next steps to avoid saying no activity was found.

Why it hurts:

- It misleads the team about capacity and progress.
- It hides real blockers or context gaps.

Do instead:

- Say "No activity found for this window" when sources are empty.
- Ask for missing context only when the user needs a fuller update.

## 3. False No Blockers

Bad signs:

- The update says "no blockers" without checking PR comments, failed CI, or blocked tickets.
- Waiting states are hidden under "in progress".
- The blocker does not name who or what can unblock it.

Why it hurts:

- The team loses the chance to help.
- Work can remain stuck while the update sounds healthy.

Do instead:

- Lead with real blockers.
- Name the dependency: access, review, credentials, decision, failing check, or external team.

## 4. Blockers at the End

Bad signs:

- A long recap appears before the blocker.
- Risks are hidden under notes after many done items.
- The user must read everything to find what needs help.

Why it hurts:

- Standups exist to coordinate; blockers are the coordination signal.
- Important risks get missed.

Do instead:

- Put blockers first unless the team has a strict different template.
- Keep blocker wording direct and specific.

## 5. Changelog Dump

Bad signs:

- Every commit is listed.
- Mechanical commits dominate the update.
- The output is longer than the activity feed.

Why it hurts:

- Teammates need outcomes, blockers, and next steps, not raw history.
- Important work gets buried.

Do instead:

- Merge commits into outcome-focused bullets.
- Include identifiers only when they help verification or follow-up.

## 6. Inferred Intent

Bad signs:

- A branch named `auth-redesign` becomes "decided to redesign auth".
- Code movement becomes "architecture migration" without supporting evidence.
- A draft PR becomes shipped work.

Why it hurts:

- Standups can accidentally announce decisions that were never made.
- Stakeholders may plan around false status.

Do instead:

- State only what the sources prove.
- Label user-reported or inferred context separately.

## 7. Mixed Status Labels

Bad signs:

- Done work, current work, and planned work appear in one bullet.
- "Today" includes items already shipped.
- "Shipped" includes draft PRs or local commits.

Why it hurts:

- The team cannot tell what is complete, active, or next.
- Follow-up expectations become unclear.

Do instead:

- Use clear sections: Blocked, Shipped/Done, In Progress/Today, Risks/Notes.
- Keep each bullet in exactly one status.
