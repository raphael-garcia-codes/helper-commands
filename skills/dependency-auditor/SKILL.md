---
name: dependency-auditor
description: Audits third-party dependencies for CVEs, maintenance risk, unused packages, and safe remediation paths.
---

# Dependency Auditor

## Hard Gate

- Detect every ecosystem present before scanning; do not stop at the first manifest.
- Use ecosystem-native scanners plus OSV-Scanner or Trivy when the project spans ecosystems or ships containers.
- Do not apply force upgrades or major-version bumps without explicit user approval.

## Process

1. Inventory package manifests and lockfiles for Node, Python, Go, Rust, containers, and monorepos.
2. Run the native scanner for each ecosystem and capture whether it has reachability analysis.
3. Distinguish direct, transitive, dev-only, and production-reachable findings.
4. Check maintenance status separately from CVEs: deprecated, archived, abandoned, single-maintainer risk, or stale releases.
5. Identify unused declared dependencies before proposing upgrades.
6. Apply safe patch/minor updates only when the project allows it and tests can verify the result.
7. Hand off major-version migrations with breaking-change notes to `migration-helper`.

## References

- `references/checklist.md` — Read before running scanners or deciding which tool applies to the project.
- `references/examples.md` — Read for command examples and report structure.
- `references/anti-patterns.md` — Read before using auto-fix, force flags, or severity-only prioritization.

## Out of scope

**vs. `security-audit`:** security-audit reviews first-party application code for vulnerabilities. This skill reviews third-party dependency risk.

**vs. `migration-helper`:** this skill may identify a major-version upgrade requirement; `migration-helper` plans and executes the breaking migration.

## Output format

```md
## Dependency Audit Report

### Ecosystems detected
[Node / Python / Go / Rust / containers / ...]

### Findings
- Critical: N
- High: N
- No fix available: N
- Maintenance risks: N
- Unused dependencies: N

### Apply Now
1. [package] [from] -> [to] — [why safe]

### Requires Migration
1. [package] [from] -> [major] — hand off to `migration-helper` because [breaking surface]

### Exceptions
1. [CVE/package] — [no fix / not reachable / dev-only], review by [date]
```
