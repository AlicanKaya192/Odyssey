Add a `ci-ok` job so that only one name goes on the required list:

- It should depend on the `lint` and `test` jobs and run even if they fail: `if: always()`. The machine is `ubuntu-latest`.
- The first step is `exit 1`; it should run only if one of the needed jobs failed or was cancelled: `'failure'` or `'cancelled'` in `needs.*.result` (`contains(...)`).
- The second step is an `echo`.
