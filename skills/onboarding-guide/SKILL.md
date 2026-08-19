---
name: onboarding-guide
description: Builds a factual onboarding map from the codebase itself and, when missing, proposes starter CLAUDE.md plus agent_docs context.
---

# Onboarding Guide

## Hard Gate

- Analyze the codebase first; do not interview for facts the repository can reveal.
- Trace at least one real request or execution flow before writing conclusions.
- Never overwrite an existing CLAUDE.md or agent_docs system silently; compare and report drift.

## Process

1. Gather manifests, framework fingerprints, entry points, top-level tree, config, CI, and test structure in parallel.
2. Trace one representative flow from entry point to validation, business logic, data access, and response/output.
3. Infer conventions from real code and recent history, with confidence levels when evidence is thin.
4. If CLAUDE.md/agent_docs already exist, read them and flag drift against the current code.
5. If they do not exist, create a lean starter system with only facts detected from code plus explicit placeholders for human-only knowledge.
6. Produce a human-facing onboarding guide with architecture, data flow, key files, setup, and detected conventions.

## References

- `references/checklist.md` — Read before the initial scan and before deciding whether docs are factual enough.
- `references/examples.md` — Read for key-file tables, drift reports, and starter context examples.
- `references/anti-patterns.md` — Read when tempted to infer business intent or generate generic project docs.

## Out of scope

**vs. `doc-writer`:** doc-writer documents a specific file, function, or feature. This skill maps the whole project.

**vs. the kit's interview-driven CLAUDE.md template:** that process uses the human as the source of truth. This skill uses the codebase as the source of truth for unfamiliar projects.

**vs. `architecture`:** this skill describes what exists. `architecture` decides between future options.

## Output format

```md
# Onboarding Guide — [project]

## What this project does
[2-3 factual sentences]

## Architecture overview
[components and dependency direction]

## Data flow
[traced request/flow]

## Key files
| File | Why it matters | Risk if changed carelessly |
|---|---|---|

## Conventions detected
[pattern + evidence + confidence]

## Setup
[commands verified or caveated]

## CLAUDE.md system
[existing/drift/generated/placeholders]
```
