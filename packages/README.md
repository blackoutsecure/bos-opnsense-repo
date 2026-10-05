# Packages and Repository Publishing

Package build, signing, metadata generation, and publication are planned.
There are no package artifacts or installable repositories yet.

## Intended architecture

Build with official OPNsense plugin conventions and FreeBSD-native tooling.
Use `pkg` repository metadata and explicitly selected native versions,
architectures, and ABIs. Do not substitute Linux package formats or service
management.

Publish verified artifacts to Cloudflare R2 and GitHub Releases. Serve
downloads over TLS through the Cloudflare CDN. Prefer Workers for automation
where a Cloudflare service provides the required behavior.

Keep signing separate from publication. Never put a signing private key in a
package, public bucket, source repository, or build log.

## Release requirements

A future pipeline must build and test natively, verify signatures through a
client trust path, publish consistent signed repository metadata, retain
rollback artifacts, and document dependency licenses.

Installation, upgrade, rollback, and security validation remain
**Not Assessed**. See [the baseline readiness gates](../docs/repository-baseline.md)
before implementing delivery.
