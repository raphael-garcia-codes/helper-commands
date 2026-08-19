# Onboarding Guide Anti-Patterns

Read this before publishing an onboarding guide. Remove anything that is guessed, generic, stale, or too bulky to help a new contributor make a safe first change.

## 1. Folder-Name Architecture

Bad signs:

- The guide is written from top-level folders only.
- No real request, command, or execution flow is traced.
- A folder named `services` is assumed to contain domain logic without reading it.

Why it hurts:

- Folder names often lie or drift over time.
- New contributors need to know how code actually runs.

Do instead:

- Trace at least one real flow from entry point to output.
- Describe architecture from imports, calls, config, and tests.

## 2. README Repetition

Bad signs:

- The guide repeats setup commands and project description only.
- It adds no risk map, conventions, or flow explanation.
- It copies stale docs without checking them.

Why it hurts:

- The onboarding guide becomes a longer README.
- Agents and humans still lack safe-change context.

Do instead:

- Add structure the README usually does not contain: key files, dependency direction, conventions, and drift.
- Link or summarize setup only after verifying it against scripts.

## 3. Invented Business Context

Bad signs:

- The guide explains why a rule exists when code only shows that it exists.
- SLAs, compliance obligations, deploy targets, or product goals are guessed.
- Marketing language replaces evidence.

Why it hurts:

- Future agents may preserve fake requirements.
- Real business rules become harder to distinguish from assumptions.

Do instead:

- State the enforced behavior and cite evidence.
- Use `[NEEDS INPUT]` for human-only intent.

## 4. Silent Doc Overwrite

Bad signs:

- Existing `CLAUDE.md`, `AGENTS.md`, or `agent_docs` are replaced without comparison.
- Stale claims are removed without reporting drift.
- The guide ignores conflicting existing docs.

Why it hurts:

- Human-authored context can be lost.
- Drift disappears instead of being corrected deliberately.

Do instead:

- Compare existing docs with code.
- Report drift and ask before replacing established context.

## 5. Generated Files as Source of Truth

Bad signs:

- Build outputs, generated clients, vendored code, or lockfile internals are treated as primary architecture.
- The guide follows generated code instead of the schema or generator.
- Large generated folders dominate the key-file list.

Why it hurts:

- Contributors edit the wrong files.
- The real source of truth stays hidden.

Do instead:

- Identify generated files and point to their generator or source schema.
- Exclude vendor/build output from architecture conclusions.

## 6. Overconfident Convention Claims

Bad signs:

- One example becomes "the project standard".
- The guide says "always" or "never" without evidence.
- Confidence is not qualified when the codebase is small or inconsistent.

Why it hurts:

- New contributors overfit to accidental patterns.
- Inconsistent areas get documented as intentional.

Do instead:

- Say "detected in these files" and include confidence when evidence is thin.
- Distinguish enforced tooling from inferred human convention.

## 7. Always-Loaded Bloat

Bad signs:

- A huge guide is proposed as always-loaded agent context.
- Detailed setup logs, dependency lists, or long walkthroughs are placed in `CLAUDE.md`.
- No separation exists between quick rules and deep reference.

Why it hurts:

- Agents waste context on information that is rarely needed.
- Important rules become harder to find.

Do instead:

- Keep always-loaded context short.
- Move deeper maps into referenced `agent_docs` files when the project supports that structure.
