# Offline Validation

Run these commands from the repository root with Python 3.11 or later:

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

The validator checks required layout and files, plugin documentation, strict
JSON policy, enabled security controls, and the baseline's explicit
no-publication guard. Failure is reported on stderr with a non-zero exit code.

The tests cover both the actual repository and malformed or unsafe fixtures.
No network, package installation, credentials, or third-party Python runtime
dependencies are needed.

These checks do not build FreeBSD packages, execute OPNsense plugins, exercise
upgrade or rollback, verify signatures, or publish to Cloudflare. Those
capabilities remain **Not Assessed**.
