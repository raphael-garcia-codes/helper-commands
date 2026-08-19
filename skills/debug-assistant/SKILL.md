---
name: debug-assistant
description: Use when the user reports a bug, pastes an error message or stack trace, says something works in one environment but not another, asks why something is broken, or a test is failing unexpectedly. Also use for "this used to work" or intermittent/flaky failures.
---

# Debug Assistant

## Process

1. **Reproduce first.** Don't start reading code or proposing fixes before you can reliably trigger the failure. Ask for the exact steps, input, or command if they weren't given. This is a hard gate: no fix is proposed before this step is complete.
2. **Write a failing test that captures the bug**, if this project has a test suite (check `agent_docs/engineering-standards.md` and the Testing/Commands sections of CLAUDE.md for how). This is not optional busywork — it's what proves the fix actually works and prevents the bug from silently coming back.
3. **Isolate before diagnosing.** Narrow down where the failure originates (which function, which layer, which input) before forming a theory about the cause. Add logging or use a debugger rather than guessing from the stack trace alone when the cause isn't obvious.
4. **Generate multiple hypotheses before testing any of them.** List 2-4 plausible causes rather than committing to the first idea that seems right, and rank them by how likely they are and how cheap they are to rule out. Test the cheapest-to-check, most-likely one first — but keep the others in mind if it doesn't pan out.
5. **Diagnose the root cause, not the symptom.** If the fix is "add a null check here," ask why the value was null in the first place — that's often where the real bug is.
6. **Fix, then run the failing test** to confirm it now passes, and run the broader test suite to confirm nothing else broke.
7. **Report what you found and why it happened**, not just what changed — this is what stops the same class of bug from recurring elsewhere in the codebase.

## What NOT to do

- Don't propose a fix before reproducing the issue — a plausible-looking fix for an unreproduced bug is a guess, not a fix.
- Don't jump to the first hypothesis that comes to mind and start changing code — form and rank a few candidate causes first, or a quick patch risks masking the real bug instead of fixing it.
- Don't suppress an error (broad try/catch, ignoring a failed assertion) instead of addressing why it happens.
- Don't fix only the reported instance if the same root cause likely affects other call sites — flag those, at minimum.
- Don't skip writing the reproducing test because "it's obviously fixed now" — that confidence is exactly how regressions come back later.

## Out of scope

If the fix requires restructuring working code rather than correcting broken code, that's a refactor, not a bug fix — use refactor-guide instead once the immediate failure is resolved. If the code returns the right result but too slowly, that's not a bug — use `performance` (Upsell 1) instead, which diagnoses via measurement rather than reproduction.

## Output format

Report: what was reproduced, root cause, what changed, and the test that proves it. If you couldn't reproduce it, say so explicitly and describe what you'd need (logs, exact input, environment details) to continue.

See the anchor install references for checklists, examples, and failure modes: `references/checklist.md`, `references/examples.md`, and `references/anti-patterns.md`.
