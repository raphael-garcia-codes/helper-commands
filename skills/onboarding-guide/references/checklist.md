# Onboarding Guide Checklist

Use this checklist when building a factual onboarding map from the repository itself.

## Initial Scan

- [ ] Package manifests and lockfiles were identified.
- [ ] Framework fingerprints were identified from config and dependencies.
- [ ] Entry points were found: server, CLI, worker, app router, main module, or composition root.
- [ ] Top-level tree was scanned without treating generated/vendor folders as architecture.
- [ ] Config and tooling files were checked.
- [ ] CI workflows were checked when present.
- [ ] Test folders and test framework config were checked.
- [ ] Existing docs were read: README, `CLAUDE.md`, `AGENTS.md`, `agent_docs`, architecture docs.
- [ ] Scripts in package/build files were compared against README setup instructions.
- [ ] Recent commit or branch context was used only when it helps explain current work.

## Flow Trace

- [ ] At least one representative execution path was traced.
- [ ] The path starts at a real entry point.
- [ ] Input validation location is identified.
- [ ] Business/domain logic location is identified.
- [ ] Data access or external API boundary is identified.
- [ ] Error handling path is identified.
- [ ] Auth/session/permission handling is identified when relevant.
- [ ] Output/response rendering is identified.
- [ ] Tests or fixtures that exercise the flow are identified.
- [ ] Risky files in the flow are named with reasons.

## Architecture Summary

- [ ] Components are named from code, not guessed from folder names.
- [ ] Dependency direction is described.
- [ ] Shared libraries and cross-cutting modules are identified.
- [ ] Data ownership is described when a schema or persistence layer exists.
- [ ] Background jobs, queues, schedulers, or webhooks are included when present.
- [ ] External integrations are listed only when evidence exists in code/config.
- [ ] Generated files are separated from source-of-truth files.
- [ ] Unknowns are labeled instead of invented.

## Conventions Detected

- [ ] Import and module layout patterns are described with evidence.
- [ ] Error handling patterns are described with evidence.
- [ ] Testing patterns are described with evidence.
- [ ] Naming and file organization conventions are described with evidence.
- [ ] State management, data fetching, or service patterns are described when relevant.
- [ ] Confidence level is included when evidence is thin.
- [ ] One-off examples are not presented as project-wide conventions.
- [ ] Tool-enforced style is separated from human convention.

## Drift Check

- [ ] Stack versions in docs match manifests or drift is reported.
- [ ] Setup commands in docs match scripts and config.
- [ ] Architecture claims match imports and folders.
- [ ] Business-rule claims are checked against enforcement code.
- [ ] Security claims are checked against auth, middleware, and config.
- [ ] Testing claims are checked against actual test commands.
- [ ] Deploy claims are marked unknown if not visible.
- [ ] Existing docs are not overwritten silently.

## Starter Context

- [ ] New `CLAUDE.md` or `agent_docs` content is proposed only when missing.
- [ ] Starter content contains only repository-derived facts.
- [ ] Human-only knowledge uses explicit placeholders.
- [ ] Always-loaded context remains short.
- [ ] Deep details are placed in referenced files when the project structure supports it.
- [ ] Generated guidance does not conflict with existing project rules.

## Setup and Verification

- [ ] Install command is taken from lockfile/package manager evidence.
- [ ] Build, lint, test, and dev commands are listed with confidence.
- [ ] Commands not run are labeled as unverified.
- [ ] Environment variables are named only when visible in examples or config.
- [ ] Secrets are not fabricated.
- [ ] Known setup risks or missing docs are called out.

## Final Check

- [ ] The guide helps a new engineer make their first safe change.
- [ ] Claims are backed by files or explicitly marked uncertain.
- [ ] The guide adds structural understanding beyond the README.
- [ ] No business intent, SLA, compliance rule, or deploy process is invented.
