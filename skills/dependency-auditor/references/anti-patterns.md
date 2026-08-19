# Dependency Auditor Anti-Patterns

Read this before publishing an audit report or applying dependency changes. Remove anything that confuses scanner output with real project risk.

## 1. Single-Tool Tunnel Vision

Bad signs:

- Only `npm audit` is run in a repo with Python, Go, Rust, or containers.
- Container base images are ignored.
- Workspaces or nested manifests are missed.

Why it hurts:

- The report can look complete while entire shipped components were never scanned.
- Runtime risk may live outside the first manifest found.

Do instead:

- Inventory ecosystems first.
- Select scanners based on actual manifests, lockfiles, and build artifacts.

## 2. Clean Scan Equals Safe

Bad signs:

- The report says dependencies are safe because no CVEs were found.
- Deprecated, abandoned, unused, or risky packages are not reviewed.
- Scanner limitations are not mentioned.

Why it hurts:

- CVE databases do not measure maintenance health.
- Abandoned packages can become future security and compatibility liabilities.

Do instead:

- Treat CVEs, maintenance risk, and unused dependencies as separate findings.
- State what the scanner can and cannot prove.

## 3. CVSS-Only Priority

Bad signs:

- A high dev-only advisory is ranked above a medium runtime issue.
- Direct and transitive findings are mixed together.
- Reachability is ignored.

Why it hurts:

- Teams spend time where exploitability is low while reachable issues remain.
- Security work becomes noisy and loses urgency.

Do instead:

- Rank by production reachability, exploitability, directness, fixed version, and severity.
- Call out dev-only findings honestly without inflating them.

## 4. Force Fix First

Bad signs:

- `npm audit fix --force` or equivalent is recommended as the default.
- Major versions change without reading migration notes.
- Tests and rollback are not named.

Why it hurts:

- Force flags can silently introduce breaking changes.
- The audit fix can become a regression factory.

Do instead:

- Prefer minimal patch/minor updates.
- Ask approval before force flags or major upgrades.
- Hand breaking migrations to `migration-helper`.

## 5. Lockfile Blindness

Bad signs:

- Only manifests are reviewed.
- The report ignores what the lockfile actually resolves.
- Lockfile churn is committed without explaining why.

Why it hurts:

- The manifest shows intent; the lockfile shows what installs.
- Vulnerable transitive packages often live only in the lockfile.

Do instead:

- Scan and review lockfiles.
- Explain whether a fix is manifest-range compatible or requires manifest changes.

## 6. Replacement by CVE Count

Bad signs:

- A maintained package is replaced because a newer package has fewer current advisories.
- The replacement's maturity, release cadence, maintainer base, and API fit are not checked.
- Migration cost is ignored.

Why it hurts:

- A less mature replacement can introduce more risk than the original vulnerability.
- The team may trade known risk for unknown operational and maintenance risk.

Do instead:

- Prefer patched versions of existing maintained dependencies.
- Evaluate replacements like architecture decisions when they affect core behavior.

## 7. No-Fix Panic

Bad signs:

- A no-fixed-version advisory is treated as unmergeable without reachability evidence.
- The report gives no mitigation or review date.
- Exceptions are undocumented.

Why it hurts:

- Teams cannot distinguish emergency work from tracked residual risk.
- The same finding reappears with no context in every audit.

Do instead:

- Document reachability, mitigation, owner, and review date.
- Escalate only when exposure and impact justify it.

