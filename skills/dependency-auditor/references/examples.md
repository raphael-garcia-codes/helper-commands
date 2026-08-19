# Dependency Auditor Examples

Use these examples to calibrate scanner coverage, prioritization, and remediation language.

## Example 1: Mixed Node and Container Project

### Input

Repository facts:

- `package.json` and `package-lock.json` at the root.
- `Dockerfile` builds the Node app on `node:20-alpine`.
- `npm audit --json` reports:
  - `axios` high severity, direct runtime dependency, fixed in `1.6.8`.
  - `webpack-dev-server` moderate severity, dev dependency, not in production image.
  - `old-parser` no CVE, deprecated package, direct runtime dependency.
- `trivy fs .` reports critical CVE in the base image package set.
- Tests are available through `npm test`.

### Weak Output

```text
Run npm audit fix. There are some vulnerabilities. Also update Docker.
```

### Why This Is Weak

- It ignores the container finding.
- It treats dev-only and runtime issues the same.
- It does not say which update is safe.
- It recommends an auto-fix without checking whether it can introduce breaking changes.

### Strong Output

```md
## Dependency Audit Report

### Ecosystems detected
- Node: `package.json`, `package-lock.json`
- Container: `Dockerfile` using `node:20-alpine`

### Tools run
- `npm audit --json`
- `trivy fs .`

### Findings
- High runtime dependency: `axios` direct dependency has a fix in `1.6.8`.
- Critical container base-image package: reported by Trivy through the current `node:20-alpine` image.
- Moderate dev-only dependency: `webpack-dev-server`, not copied into the production image.
- Maintenance risk: `old-parser` is deprecated and still used at runtime.

### Apply Now
1. `axios` `1.6.0` -> `1.6.8` — patch update within the existing major version; run `npm test` after lockfile update.
2. Refresh the `node:20-alpine` base image digest or move to the latest patched `20-alpine` tag, then rebuild and rerun `trivy image`.

### Requires Follow-up
1. Replace `old-parser` — no CVE, but it is deprecated and runtime-reachable. Treat as maintenance risk, not emergency security work.

### Exception
1. `webpack-dev-server` advisory — dev-only and not present in the production image. Recheck during the next dependency maintenance window.
```

### Why This Is Strong

- It covers both application and container dependencies.
- It separates runtime risk from dev-only advisories.
- It distinguishes CVEs from maintenance risk.
- It gives safe next steps and verification.

## Example 2: Major Upgrade Required

### Input

Repository facts:

- Express `4.x` is direct runtime dependency.
- Scanner reports a high advisory fixed only in Express `5.x`.
- The app has custom error-handling middleware.
- Express 5 changes promise rejection and route matching behavior.

### Strong Output

```md
## Dependency Audit Report

### Ecosystems detected
- Node: `package.json`, `pnpm-lock.yaml`

### Findings
- High: `express` `4.x` advisory has no safe patch within the current major range.
- Production reachability: direct runtime dependency used by the HTTP server.
- Breaking surface: middleware error handling, route matching, and async handler behavior can change in Express 5.

### Apply Now
No safe patch/minor update is available within the current major version.

### Requires Migration
1. `express` `4.x` -> `5.x` — hand off to `migration-helper`.
   - Read the official Express 5 migration guide.
   - Add focused tests around custom error middleware and route patterns before upgrading.
   - Upgrade on a dedicated branch, not as part of a broad audit fix.

### Exception Until Migration
1. Track the advisory with owner and review date.
2. Confirm whether exposed endpoints use the vulnerable path.
3. Document any compensating controls until the migration lands.
```

### Why This Is Strong

- It does not hide a major migration inside `audit fix`.
- It names the breaking surface before changing versions.
- It gives the user a safe decision boundary.

## Command Patterns

Use commands that match the detected ecosystem:

```bash
npm audit --json
pnpm audit --json
pip-audit -r requirements.txt --format json
govulncheck ./...
cargo audit
osv-scanner --lockfile=package-lock.json
trivy fs --severity HIGH,CRITICAL .
trivy image --severity HIGH,CRITICAL myapp:latest
```

Do not run every command blindly. Choose the commands that match real manifests and shipping artifacts.
