# Changelog

## Unreleased

### Added

- Repository-wide FreeBSD and OPNsense agent policy.
- Development lab structure and documentation-only scaffolds for the Azure,
  Cloudflare, and observability plugins.
- Standard-library-only offline checks and failure-path tests.
- GitHub Actions validation and development-runtime hub integration.
- Explicit readiness, upgrade, rollback, and security-review requirements.

### Changed

- Consolidated agent policy in [AGENTS.md](AGENTS.md) and removed the redundant
  Copilot instruction wrapper without weakening repository validation.
- Shortened the public README and removed redundant local dotfile settings,
  unused lockfile attributes, and unnecessary comments.
- Read repository policy once using the shared required-file validation.
- Limited symlink checks to the checkout boundary while retaining rejection
  of symlinked roots, required directories, and documents.
- Expanded regression coverage for filesystem errors and every publication
  stage and required security gate.

No installable plugin, package, production release, or deployment is included.
