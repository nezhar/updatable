# Security Policy

## Supported Versions

Only the latest release line receives security fixes. Older versions are not
patched, please upgrade before reporting an issue against them.

| Version | Supported          |
| ------- | ------------------ |
| 0.8.x   | :white_check_mark: |
| < 0.8   | :x:                |

Supported Python versions are the ones listed in `pyproject.toml`
(currently Python 3.10 and newer).

## Reporting a Vulnerability

Please do **not** open a public issue for security problems.

Use GitHub's private vulnerability reporting instead:
[Report a vulnerability](https://github.com/nezhar/updatable/security/advisories/new).

If you cannot use that form, send a mail to <hn@nezhar.com> with:

- a description of the issue and its impact
- the affected version of `updatable`
- steps to reproduce, ideally a minimal example

You can expect an initial response within 14 days. Once the report is
confirmed, a fix is released and the advisory is published, crediting the
reporter unless anonymity is requested.
