# os-blackoutsecure-cloudflare

## Overview

Planned Cloudflare integration for OPNsense. This directory is a documentation
scaffold, not an implemented or installable plugin.

## Architecture

Follow OPNsense MVC conventions: controllers orchestrate, models validate,
views contain minimal logic, and services hold business logic.

Specific Cloudflare APIs, zone or account scopes, and supported native versions
have not been selected. Prefer Pages, R2, CDN, and Workers for the relevant
hosting and automation tasks; do not provision equivalent custom infrastructure.

## Installation

Not available. No package manifest, service, or executable implementation is
provided.

## Upgrade path

Not Assessed. Implement and test configuration migrations before the first
release.

## Rollback path

Not Assessed. Test recovery on a disposable native OPNsense instance before
publishing an artifact.

## Security review

No Cloudflare client or token storage is implemented. Future integration must
use verified TLS, validated input, protected configuration, least-privilege
tokens, and credential redaction. Native runtime security is Not Assessed.

See [the baseline acceptance gates](../../docs/repository-baseline.md),
[SECURITY.md](SECURITY.md), and [LICENSE](LICENSE).
