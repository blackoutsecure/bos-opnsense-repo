# Blackout Secure OPNsense Lab

Copyright (c) 2026 Blackout Secure | Apache License 2.0

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)
[![Made by BlackoutSecure](https://img.shields.io/badge/made%20by-BlackoutSecure-1f1f1f)](https://github.com/blackoutsecure)

FreeBSD and OPNsense development laboratory for plugins, packages, integration
testing, signed package repositories, and Cloudflare-hosted documentation.

## Overview

This repository currently contains a secure development baseline, plugin
documentation scaffolds, and offline repository checks. It does **not** contain
installable plugins, built packages, a signing service, or live deployments.

| Component | Current state |
| --- | --- |
| Repository contract checks | Implemented; not a native build |
| `os-blackoutsecure-azure` | Planned documentation scaffold |
| `os-blackoutsecure-cloudflare` | Planned documentation scaffold |
| `os-blackoutsecure-observability` | Planned documentation scaffold |
| FreeBSD builds and package signing | Not Assessed |
| OPNsense installation, upgrade, and rollback | Not Assessed |
| R2, CDN, Workers, and Pages publication | Not Assessed |

Security, stability, maintainability, compatibility, and performance are the
priorities, in that order. FreeBSD and OPNsense are the primary targets; Azure,
Cloudflare, and Linux companion hosts are secondary integration targets.

## Architecture

| Directory | Purpose |
| --- | --- |
| [packages/](packages/README.md) | Native package and repository publishing standards |
| [plugins/](plugins/README.md) | OPNsense plugin documentation scaffolds |
| [docs/](docs/README.md) | Architecture, readiness, and operating procedures |
| [examples/](examples/README.md) | Rules for safe, non-secret examples |
| [scripts/](scripts/README.md) | Standard-library-only offline validation |
| [tests/](tests/test_validate_repository.py) | Repository contract and failure-path tests |

Controllers orchestrate; models validate; views contain minimal logic; services
hold business logic. Follow the official
[OPNsense development documentation](https://docs.opnsense.org/development.html)
and [plugin repository](https://github.com/opnsense/plugins).

## Installation

There is nothing to install on a firewall yet. Use an isolated development host
or jail, not a production OPNsense system, for repository work.

Clone the development branch and run the offline checks with Python 3.11 or later:

```sh
git clone --branch dev https://github.com/blackoutsecure/bos-opnsense-repo.git
cd bos-opnsense-repo
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

On a FreeBSD development host, use `pkg` if Python must be installed. Do not
replace the Python runtime supplied by a production OPNsense installation.
The validator has no third-party runtime dependencies or network requirements.

## CI/CD

GitHub Actions runs offline checks on Python 3.11 and 3.14 and calls the hub's
universal security gate. Linux-hosted contract checks do not certify FreeBSD
packages or OPNsense behavior.

The hub-managed gatekeeper is the front door for authorized manual maintenance
and managed-file synchronization. Configure it through
[bos-universal-config.json](.github/bos-universal-config.json), not by editing
the managed workflow. Existing organization Apps are reused; no new credentials
are provisioned by this baseline.

Secret scanning, secret-scanning push protection, extended Python CodeQL
analysis, and private vulnerability reporting are enabled for this public
repository. These checks supplement, rather than replace, native validation.

The security caller is pinned to hub release `v0.0.22` and deliberately selects
`hub_ref: dev` for the development action layout. `dev` remains the default
development branch. `main` holds the verified repository baseline and is
protected by reviews, required checks, and conversation resolution. It is not
a released plugin or package. No version tag or product release is created.

All delivery stages remain off. Future artifacts must publish to Cloudflare R2
and GitHub Releases; documentation must publish to Cloudflare Pages. Prefer the
Cloudflare CDN and Workers over equivalent custom infrastructure.

## Upgrade and rollback

Repository upgrades happen through reviewed commits on `dev`. Use a reverting
commit for a repository rollback; never move a released version tag.
Update protected `main` through a pull request only, after its repository
contract and `security (main) / Security summary` checks pass.

Plugin and package upgrades and rollback are **Not Assessed**. Before the first
release, select supported OPNsense and FreeBSD versions and ABIs, implement
native build and signing gates, and test installation, upgrade, service
recovery, and rollback on disposable native lab instances.

See [the baseline operating procedure](docs/repository-baseline.md) for the
architecture, readiness gates, upgrade procedure, and rollback procedure.

## Security review

The baseline has no plugin endpoints, external API clients, package-signing
keys, or deployment credentials. Repository checks reject malformed policy,
unsafe plugin documentation paths, disabled security controls, and accidental
delivery enablement.

This is a baseline hardening record, not a certification of future plugin code.
Native runtime security and deployment behavior remain Not Assessed. Follow
[SECURITY.md](SECURITY.md) for private vulnerability reporting and
[CONTRIBUTING.md](CONTRIBUTING.md) for contribution requirements.

## License

This repository uses the organization-standard [Apache License 2.0](LICENSE).
Each plugin scaffold includes its own copy. Third-party licenses and notices
must be reviewed before dependencies are redistributed.

<!-- >>> managed-file-sync:security_readme_pointer >>> -->
## Security & secrets

This repository is built with Blackout Secure's reusable GitHub Actions
workflows. If you fork or self-host these workflows and need to provision
your own credentials (GitHub App vs. PAT guidance, secret tiers, Docker
Hub/Cloudflare/Balena setup walkthroughs), see the
["Secrets pipelining strategy"](https://github.com/blackoutsecure/bos-automation-hub#secrets-pipelining-strategy)
section of `bos-automation-hub`. To report a vulnerability, see
[SECURITY.md](https://github.com/blackoutsecure/.github/blob/main/SECURITY.md).
<!-- <<< managed-file-sync:security_readme_pointer <<< -->
