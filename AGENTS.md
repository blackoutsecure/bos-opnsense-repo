# Blackout Secure OPNsense Lab

## Repository Purpose

This repository is a FreeBSD and OPNsense development laboratory.

It is used to:

- Develop OPNsense plugins
- Build FreeBSD packages
- Test integrations
- Generate package repositories
- Publish Cloudflare-hosted repositories
- Publish documentation through Cloudflare Pages

## Platform Targets

Primary:

- OPNsense
- FreeBSD

Secondary:

- Azure
- Cloudflare
- Linux companion hosts

## Repository Scope

Plugins:

- os-blackoutsecure-azure
- os-blackoutsecure-cloudflare
- os-blackoutsecure-observability

Infrastructure:

- Package building
- Package signing
- Repository metadata generation
- Documentation generation

## Development Rules

Always prefer:

- FreeBSD-native implementations
- OPNsense plugin standards
- Secure defaults
- Production-quality code

Never assume:

- Linux package managers exist
- systemd exists
- rpm exists
- apt exists

Use:

- pkg
- rc.d
- FreeBSD networking
- OPNsense MVC framework

## Cloudflare Standards

Use Cloudflare when possible:

- Documentation: Cloudflare Pages
- Package hosting: Cloudflare R2
- Downloads: Cloudflare CDN
- Automation: Cloudflare Workers

Do not deploy custom infrastructure if equivalent Cloudflare services exist.

## Security Requirements

Mandatory:

- TLS everywhere
- No plaintext secrets
- Input validation
- Secure configuration storage
- Principle of least privilege

Never:

- Disable certificate validation
- Log credentials
- Commit secrets

## Package Standards

Repository structure:

```text
packages/
plugins/
docs/
examples/
scripts/
```

Each plugin must contain:

- README
- CHANGELOG
- SECURITY
- LICENSE

## CI/CD

Use GitHub Actions for:

- Package builds
- Validation
- Testing
- Release creation

Publish artifacts to:

- Cloudflare R2
- GitHub Releases

Documentation publishes to:

- Cloudflare Pages

## OPNsense Standards

Follow official OPNsense plugin conventions.

- Controllers: thin; orchestration only
- Models: validation only
- Views: minimal logic
- Services: business logic

## Documentation

Every new feature must include:

- Overview
- Architecture
- Installation
- Upgrade path
- Rollback path
- Security review

## Copilot Behavior

Generate:

- Production-ready code
- FreeBSD-compatible code
- OPNsense-compatible code
- Security-first implementations

Priorities:

1. Security
2. Stability
3. Maintainability
4. Compatibility
5. Performance

When uncertain, prefer FreeBSD-native solutions over Linux-specific implementations.

## Repository Commands

Run the offline checks from the repository root:

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

These validate repository contracts, not native package or firewall behavior.
FreeBSD builds, OPNsense installation, signing, upgrades, and rollback remain
Not Assessed until exercised on explicitly selected native platform versions.

## Automation Ownership

Configure hub integration through `.github/bos-universal-config.json`.
Do not hand-edit the hub-managed gatekeeper kicker. `dev` is the default
development branch; `main` holds a protected repository baseline, not a
released plugin. Publishing is intentionally off. Do not enable it without
native validation, a signing design, and a tested rollback path.

Read [the baseline documentation](docs/repository-baseline.md) before extending
the scaffolds. Planned plugins are not installable packages.
