# Security Policy

## Supported scope

The current repository is a development baseline, not a released firewall
extension. There are no supported plugin or package releases yet. Native
FreeBSD and OPNsense runtime behavior, package signing, and hosted delivery
remain Not Assessed.

Do not install these scaffolds on a production firewall or treat an offline
contract check as a native compatibility or security certification.

## Reporting a vulnerability

Follow the organization's
[private vulnerability reporting policy](https://github.com/blackoutsecure/.github/blob/main/SECURITY.md).
Use this repository's enabled
[private reporting channel](https://github.com/blackoutsecure/bos-opnsense-repo/security/advisories/new).
Do not put credentials, private keys, configuration backups, customer data,
or unredacted exploit details in public issues.

## Required controls

- Verify TLS certificates for every external connection.
- Validate configuration, API inputs, filesystem paths, and subprocess arguments.
- Store sensitive configuration using the supported OPNsense mechanisms with
  appropriate access controls. Review configuration exports and backups for
  secret exposure.
- Never place tokens or signing keys in source, generated packages, examples,
  command-line arguments, or logs.
- Keep signing, package publication, documentation deployment, and firewall
  administration credentials separate and least-privilege.
- Require native tests, signature verification, dependency-license review,
  and tested rollback before publishing an installable artifact.

The ignore rules reduce accidental staging; they are not a substitute for
secret scanning or access controls. The hub's security gates remain enabled.
