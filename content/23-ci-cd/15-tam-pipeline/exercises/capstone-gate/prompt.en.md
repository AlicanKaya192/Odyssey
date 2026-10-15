Add two jobs:

- `build`: when `test` finishes, `ubuntu-latest`. Get the code, set up Python 3.13, `python -m pip install build`, `python -m build`, then `actions/upload-artifact@v4` with `name: dist`, `path: dist/`.
- `ci-ok`: depends on `lint`, `test` and `build`, `if: always()`, `ubuntu-latest`. The first step is `exit 1`, only if `needs.*.result` holds `'failure'` or `'cancelled'`; the second step is an `echo`.
