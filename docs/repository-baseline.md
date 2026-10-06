# Repository Baseline

## Overview

This feature establishes a FreeBSD and OPNsense development lab. It
provides repository instructions, plugin documentation scaffolds, offline
contracts, and GitHub Actions integration. It does not implement plugin
behavior or publish deployable artifacts.

`dev` is the default development branch. Protected `main` contains the verified
repository baseline only; it does not establish a supported plugin or package
release. Promote repository changes through reviewed pull requests and keep
native artifact publication off until the acceptance requirements are met.

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

At pinned hub release `v0.0.22`, the
[action tree](https://github.com/blackoutsecure/bos-automation-hub/tree/b2e4faaa36c4d482737243a97415edc046ddde57/.github/actions/shared)
uses `.github/actions/shared/`, while the
[security workflow](https://github.com/blackoutsecure/bos-automation-hub/blob/b2e4faaa36c4d482737243a97415edc046ddde57/.github/workflows/bos-universal-security.yml)
checks out and invokes `.github/actions/universal-config` without `shared/`.
The lab therefore explicitly selects `hub_ref: dev` for action/config
checkouts on both lab branches while keeping the workflow definition pinned.
This is not a production-runtime promotion. Review the pinned workflow and
its checkout ref together before switching to promoted action/config sources
or enabling artifact publication.

## GitHub readiness

The repository's GitHub settings complement the offline contracts:

- `dev` is the default branch and rejects force pushes, branch deletion, and
  merge commits. Administrators must follow these protections.
- The active `OPNsense dev review and CI` ruleset requires a code-owner review,
  resolution of review conversations, an up-to-date branch, both
  repository-contract matrix checks, and `security (dev) / Security summary`.
  Only the existing Gatewall App is exempt from this review/check ruleset,
  preserving its managed fast-forward sync commits. It is not exempt from
  the independent history protections. No App permissions or secrets are added.
- `main` requires a code-owner review, resolution of review
  conversations, an up-to-date branch, both repository-contract matrix checks,
  and `security (main) / Security summary`. Never bypass these requirements.
- Actions tokens default to read-only access and cannot approve PR reviews.
  Existing workflows request any required write permissions per job.
- Dependency graph/review, Dependabot alerts and security updates, secret
  scanning and push protection, non-provider patterns and validity checks,
  extended Python CodeQL analysis, and private reporting are enabled.
- Squash or rebase merges preserve linear history. Merged short-lived branches
  are deleted automatically; the protected long-lived branches are retained.

The pinned hub release passes `gate.pr_title_types` directly to the semantic
PR-title action, which expects a multiline string rather than CSV. The
repository explicitly configures all eleven existing conventional types in
that format. An offline regression test checks the entries; the live PR title
job verifies the integration.

The gatekeeper workflow remains hub-owned. Dependabot changes to its pins must
be incorporated into the canonical hub template and then synchronized, not
merged only into this repository where the next sync would overwrite them.

The current posture scanner reads classic branch protection rather than the
effective ruleset combination. It can therefore report PS021/PS023 for `dev`
despite the active review/check ruleset. Verify that ruleset and GitHub's
effective branch rules when reviewing these findings; do not disable the
security gate or weaken the actual protections to silence them.

These are repository controls, not native release evidence. GitHub settings
and credential validity require live verification; the offline validator
neither configures settings nor verifies stored secrets.

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
