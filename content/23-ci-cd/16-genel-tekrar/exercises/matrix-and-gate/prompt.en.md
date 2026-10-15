Spread the `test` job over two operating systems and two Python versions, then add a gate:

- Matrix: `os: [ubuntu-latest, windows-latest]`, `python: ["3.12", "3.13"]`; remove 3.12 on Windows (`exclude`). `fail-fast: false`. The machine is `${{ matrix.os }}`.
- `setup-python`: `python-version: ${{ matrix.python }}`, `cache: pip`.
- A `ci-ok` job: depends on `test`, `if: always()`, `ubuntu-latest`; the first step is `exit 1`, only if `needs.*.result` holds `'failure'` or `'cancelled'`; the second step is an `echo`.
