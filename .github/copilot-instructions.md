# Copilot Instructions

Read and follow [AGENTS.md](../AGENTS.md) before making changes. It is the
canonical repository-wide policy for the Blackout Secure OPNsense Lab.

Apply that policy to all code, configuration, documentation, and automation:

- Target FreeBSD and OPNsense first. Prefer `pkg`, `rc.d`, FreeBSD networking,
  and the OPNsense MVC framework. Do not assume Linux package managers,
  `systemd`, `rpm`, or `apt` exist.
- Follow official OPNsense plugin conventions: thin orchestration controllers,
  validation-only models, minimal view logic, and business logic in services.
- Use secure defaults, TLS, input validation, secure configuration storage,
  and least privilege. Never disable certificate validation, store plaintext
  secrets, log credentials, or commit secrets.
- Prefer Cloudflare Pages for documentation, R2 for packages, CDN for downloads,
  and Workers for automation over equivalent custom infrastructure.
- Use GitHub Actions for builds, validation, testing, and releases. Publish
  artifacts to Cloudflare R2 and GitHub Releases, and documentation to
  Cloudflare Pages.
- Keep the `packages/`, `plugins/`, `docs/`, `examples/`, and `scripts/` layout.
  Every plugin must contain README, CHANGELOG, SECURITY, and LICENSE files.
- Document every new feature's overview, architecture, installation, upgrade
  path, rollback path, and security review.
- Generate production-ready, FreeBSD-compatible, OPNsense-compatible code.
  Prioritize security, stability, maintainability, compatibility, then
  performance. When uncertain, prefer FreeBSD-native solutions.

Run the offline checks documented in [AGENTS.md](../AGENTS.md). Read
[the repository baseline](../docs/repository-baseline.md) before extending
the scaffolds. Do not describe planned plugins or unassessed native behavior
as implemented, tested, or production-ready.
