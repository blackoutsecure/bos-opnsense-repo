# Repository Baseline

## Overview

This feature establishes a development-only FreeBSD and OPNsense lab. It
provides repository instructions, plugin documentation scaffolds, offline
contracts, and GitHub Actions integration. It does not implement plugin
behavior or publish deployable artifacts.

## Architecture

Native source belongs under `plugins/`; package build and repository tooling
belongs under `packages/` and `scripts/`. The three initial plugin directories
contain documentation and licenses only.

The offline validator reads repository policy and plugin documentation using
the Python standard library. It does not execute plugin code, install software,
call GitHub, contact Azure or Cloudflare, or read signing keys.

The validation workflow runs the validator and its tests on Linux-hosted
Python 3.11 and 3.14. The separate security caller uses the hub's existing
security gates and organization policy without reducing their severity.

The canonical managed gatekeeper handles authorized manual operations and
managed-file reconciliation. Existing Gatekeeper credentials authorize
dispatches; existing Gatewall credentials perform purpose-scoped repository
automation. The baseline does not add App permissions or credential scope.

The published hub's `main` action tree still uses the nested layout while its
security workflow expects development action paths. This lab therefore
explicitly selects `hub_ref: dev` for development validation. This is not a
production-runtime promotion. Recheck the promoted runtime before adding a
stable-branch caller.

## Installation

Clone the `dev` branch onto a development host with Python 3.11 or later and
run:

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

No third-party Python runtime dependencies are needed. On FreeBSD, obtain
development tools through `pkg`; do not modify a production firewall's base
runtime for these checks.

There are no valid plugin installation commands yet.

## Upgrade path

1. Review changes to instructions, repository contracts, and workflow pins.
2. Run offline validation and all tests.
3. Require the GitHub Actions validation and security checks to complete.
4. Merge reviewed changes into `dev`.
5. Keep publication off until the native acceptance requirements below have
   been satisfied.

For a future package release, identify the supported FreeBSD ABI and OPNsense
versions, implement migrations, validate on disposable native instances, and
record the build and signature-verification evidence. Package and metadata
publication must form a consistent, recoverable update.

## Rollback path

For repository changes, create a reverting commit and rerun validation. Do not
rewrite published history or move released tags.

For future native releases, retain previously verified packages and signed
repository metadata, preserve a protected configuration backup, and test
restoring the previous plugin and service state. A configuration backup may
contain secrets and must not enter this repository.

No native rollback has been exercised by this baseline.

## Security review

### Trust boundaries

- Pull-request code runs without persistent checkout credentials or deployment
  secrets in the repository-contract job.
- Required plugin documentation must be regular, non-empty UTF-8 files.
  Plugin-directory and required-document symlinks are rejected.
- Repository policy rejects duplicate JSON keys, malformed objects, disabled
  security gates, and delivery stages that are not explicitly off.
- The existing hub security workflow retains its policy gates and uses its
  existing purpose-scoped audit credential.
- Signing and external publication are not implemented, so no credentials
  for those operations are introduced.

Ignore rules and offline contracts are not secret scanners or native security
audits. Native runtime security is **Not Assessed**.

### Native acceptance requirements

Before the first installable release:

1. Select supported OPNsense releases, FreeBSD versions, architectures, and ABIs.
2. Build using official OPNsense plugin and FreeBSD package conventions.
3. Exercise MVC validation, service lifecycle, networking, and error reporting.
4. Verify TLS certificate validation and credential redaction.
5. Test clean installation, configuration migration, upgrade, and rollback.
6. Sign packages and repository metadata with isolated signing credentials.
7. Verify signatures using an independently configured client trust path.
8. Review dependency licenses and retained notices.
9. Implement least-privilege R2 and GitHub Release publication and Pages
   documentation deployment without exposing signing keys.
10. Replace the baseline no-publication guard with those actual release gates.

All native acceptance requirements are currently **Not Assessed**.

## References

- [OPNsense development documentation](https://docs.opnsense.org/development.html)
- [OPNsense MVC example](https://docs.opnsense.org/development/examples/helloworld.html)
- [Official OPNsense plugins](https://github.com/opnsense/plugins)
- [FreeBSD Ports Handbook](https://docs.freebsd.org/en/books/porters-handbook/)
- [Cloudflare R2 documentation](https://developers.cloudflare.com/r2/)
- [Cloudflare Pages documentation](https://developers.cloudflare.com/pages/)
