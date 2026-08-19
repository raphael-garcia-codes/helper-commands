# Dependency Auditor Checklist

Use this checklist before running scanners, interpreting findings, or proposing dependency changes.

## Ecosystem Inventory

- [ ] Node manifests were checked: `package.json`, workspace files, and lockfiles.
- [ ] Python manifests were checked: `pyproject.toml`, `requirements*.txt`, `uv.lock`, `poetry.lock`, or `Pipfile.lock`.
- [ ] Go manifests were checked: `go.mod` and `go.sum`.
- [ ] Rust manifests were checked: `Cargo.toml` and `Cargo.lock`.
- [ ] Java/JVM manifests were checked when present: `pom.xml`, `build.gradle`, or `gradle.lockfile`.
- [ ] Containers were checked: `Dockerfile`, compose files, image build workflows, and base images.
- [ ] Monorepo packages under `apps/`, `packages/`, `services/`, or similar folders were included.
- [ ] Lockfiles were treated as the source of what actually installs.
- [ ] Generated or vendored dependency trees were excluded unless they ship.
- [ ] The package manager in use was identified before choosing commands.

## Scanner Selection

- [ ] Node uses the project package manager: `npm audit`, `pnpm audit`, `yarn npm audit`, or equivalent.
- [ ] Python uses `pip-audit` or an ecosystem-native scanner that can read the actual dependency set.
- [ ] Go uses `govulncheck ./...` when code reachability matters.
- [ ] Rust uses `cargo audit` or the project's existing advisory workflow.
- [ ] Containers use `trivy fs`, `trivy image`, or an existing image scanner.
- [ ] Multi-ecosystem repos use OSV-Scanner, Trivy, or a combination rather than one ecosystem tool.
- [ ] Scanner output format is machine-readable when possible.
- [ ] Scanner limitations are captured: no reachability, registry-only data, dev dependency ambiguity, or missing lockfile.

## Finding Classification

- [ ] Direct dependencies are separated from transitive dependencies.
- [ ] Runtime dependencies are separated from dev/test/build-only dependencies.
- [ ] Production-reachable findings are separated from non-shipping code paths.
- [ ] Severity is recorded but not used as the only priority signal.
- [ ] Exploitability, reachability, and exposed surface are considered.
- [ ] Fixed version availability is checked.
- [ ] No-fix findings include mitigation or exception guidance.
- [ ] Duplicate advisories for the same root package are deduplicated.
- [ ] False positives are documented with evidence.

## Maintenance Risk

- [ ] Deprecated packages are identified.
- [ ] Archived repositories are identified.
- [ ] Packages with no release activity for a long period are flagged when they are important.
- [ ] Single-maintainer or abandoned packages are flagged when they are critical path.
- [ ] Replacement packages are evaluated for maturity, not only current CVE count.
- [ ] Unused declared dependencies are checked separately from vulnerable dependencies.
- [ ] License or policy constraints are mentioned only if the project requires them.

## Remediation Planning

- [ ] Patch and minor updates are preferred when they satisfy the advisory.
- [ ] Major updates are handed to `migration-helper` when breaking changes are likely.
- [ ] Force-fix commands require explicit user approval.
- [ ] Lockfile-only updates are allowed only when the manifest range already permits the fixed version.
- [ ] Peer dependency changes are included when required.
- [ ] Test commands or verification steps are named before applying changes.
- [ ] Security exceptions include owner, rationale, mitigation, and review date.
- [ ] Remediation is grouped by risk and blast radius, not by scanner output order.

## Report Quality

- [ ] Ecosystems detected are listed.
- [ ] Tools run are listed with important limitations.
- [ ] Findings are grouped into `Apply Now`, `Requires Migration`, and `Exceptions`.
- [ ] Each `Apply Now` item explains why the update is safe.
- [ ] Each migration item names the breaking surface.
- [ ] Each exception explains why it is acceptable for now.
- [ ] The report does not overstate safety when scans cannot prove reachability.
- [ ] The final recommendation is actionable without re-reading raw scanner JSON.

## Final Check

- [ ] The audit covers every manifest that can affect shipped software.
- [ ] Production risk is prioritized over raw advisory count.
- [ ] No major upgrade is hidden inside a simple audit fix.
- [ ] The user can choose what to apply safely now versus plan later.
