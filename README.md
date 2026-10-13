# Blackout Secure OPNsense Lab

Copyright (c) 2026 Blackout Secure | Apache License 2.0

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)
[![Made by BlackoutSecure](https://img.shields.io/badge/made%20by-BlackoutSecure-1f1f1f)](https://github.com/blackoutsecure)

Development workspace for FreeBSD packages and OPNsense plugins.

**This is a documentation and validation baseline, not an installable plugin
or package repository.** There are no built packages, signing services, or
live deployments.

## Status

The [Azure, Cloudflare, and observability plugin scaffolds](plugins/README.md)
contain documentation and licenses only. FreeBSD builds, package signing,
OPNsense installation, upgrades, rollback, and hosted publication are
**Not Assessed**.

Do not install these scaffolds on a production firewall.

## Validate a checkout

Use Python 3.11 or later on a development host:

```sh
git clone --branch dev https://github.com/blackoutsecure/bos-opnsense-repo.git
cd bos-opnsense-repo
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

The [offline validator and tests](scripts/README.md) use only the Python
standard library and need no network or credentials. CI runs the checks on
Python 3.11 and 3.14 alongside the hub's universal security gate. These checks
do not certify native packages or firewall behavior.

On FreeBSD, install development tools through `pkg`; do not replace a
production OPNsense system's Python runtime.

## Development

Work through reviewed changes on `dev`. Protected `main` holds the repository
baseline, not a released plugin. Publication remains disabled until native
builds, signing, installation, upgrade, and rollback have been validated.

- [Contributing](CONTRIBUTING.md): development and plugin requirements.
- [Repository baseline](docs/repository-baseline.md): architecture, automation,
  release-readiness gates, and recovery procedures.
- [Package publishing](packages/README.md): native build and hosting requirements.
- [Security policy](SECURITY.md): private vulnerability reporting.

Configure hub integration through
[bos-universal-config.json](.github/bos-universal-config.json); do not hand-edit
hub-managed workflows or blocks.

## License

[Apache License 2.0](LICENSE). Review third-party licenses and notices before
redistributing dependencies.

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
