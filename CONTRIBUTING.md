# Contributing to genro-pages

Follow the shared [project policies](CLAUDE.md).

## Setup and checks

Install `.[dev,docs]` in a Python 3.11+ environment. Run Ruff, pytest and the
Sphinx documentation build before submitting changes. Mypy is advisory.
The current seed has no behavioral tests; pytest exit code 5 is expected only
until the first test is added. Introduce meaningful contract tests alongside
implementation, and use tests/x/ for implementation-specific checks.

Use develop as the base for working branches. Keep changes focused and do not
commit temporary files, local configuration, credentials or dependency trees.
Write code, comments and documentation in English. New public APIs and
architectural changes must be discussed before implementation.

## Local Git hooks

The initial repository has the shared pre-commit, commit-msg and attribution
cleanup hooks installed. Future clones in the same sibling layout can install
shared hooks from ../../subproject_setup/hooks/ and the cleanup hook from
../../scripts/install-claude-cleanup-hook.sh after reading those scripts.
Ruff is a blocking pre-commit check; mypy is advisory.

## License

Contributions use the repository's Apache License 2.0.
