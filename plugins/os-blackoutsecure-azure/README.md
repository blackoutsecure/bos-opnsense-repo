# os-blackoutsecure-azure

## Overview

Planned Azure integration for OPNsense. This directory is a documentation
scaffold, not an implemented or installable plugin.

## Architecture

Follow OPNsense MVC conventions: controllers orchestrate, models validate,
views contain minimal logic, and services hold business logic.

Specific Azure APIs, authentication methods, permissions, and supported native
versions have not been selected. Do not create broad cloud credentials in
anticipation of an unspecified feature.

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

No Azure client or credential storage is implemented. Future integration must
use verified TLS, validated input, protected configuration, least privilege,
and credential redaction. Native runtime security is Not Assessed.

See [the baseline acceptance gates](../../docs/repository-baseline.md),
[SECURITY.md](SECURITY.md), and [LICENSE](LICENSE).
