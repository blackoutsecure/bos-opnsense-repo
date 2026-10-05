# Contributing

Read [AGENTS.md](AGENTS.md) and
[the baseline operating procedure](docs/repository-baseline.md) first.

## Development

Work on `dev` or a feature branch targeting `dev`. Use conventional-commit
titles for pull requests. Do not create a stable release or move a version tag
as part of routine development.
Updates to protected `main` require a pull request, passing checks, review,
and resolved conversations. A baseline on `main` is not a package release.

Use an isolated FreeBSD development host or OPNsense lab instance. Prefer
`pkg`, `rc.d`, FreeBSD networking, and the OPNsense MVC framework. Never assume
`apt`, `rpm`, or `systemd` exists on the target.

Python validation tooling is standard-library-only and targets Python 3.11
and later. Run from the repository root:

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

GitHub Actions additionally runs the hub's lint, security, and compliance
checks. A metadata-only check is not a FreeBSD or OPNsense test.

## Plugin requirements

Use `plugins/os-blackoutsecure-<name>/` for first-party plugin work. Each plugin
must contain non-empty `README.md`, `CHANGELOG.md`, `SECURITY.md`, and `LICENSE`
files, with no symlink replacing those required files.

Do not add a dummy package manifest, placeholder service, or installation
command that makes a documentation scaffold appear functional. When
implementing a plugin, follow official OPNsense layout and build conventions,
keep controllers thin, and put business logic in services.

## Feature acceptance

Every feature must document its overview, architecture, installation, upgrade
path, rollback path, and security review. Select supported native platform
versions and ABIs before claiming compatibility.

Native tests must cover configuration validation, service lifecycle, failure
handling, secret redaction, TLS certificate verification, installation,
upgrade, and rollback. Package release work additionally needs a signing and
signature-verification design.

The baseline validator intentionally rejects enabled delivery stages. Replace
that starter guard with real, fail-closed native build and signing gates in
the same reviewed change that introduces publication; do not merely relax it.

## Dependencies and automation

Review licenses and redistribution requirements before adding dependencies.
Use SHA pins and truthful version comments for action dependencies.

The hub-managed gatekeeper is maintained centrally. Change its behavior
through [repository configuration](.github/bos-universal-config.json) rather
than editing the workflow. Do not weaken security controls to get green CI.
