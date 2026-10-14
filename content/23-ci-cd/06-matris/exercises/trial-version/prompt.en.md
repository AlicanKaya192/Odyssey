Also try Python 3.15, which is not out yet, but the pipeline should not turn red if that job fails:

- Add a new combination with `include`: `python-version` `"3.15"`, `experimental` `true`.
- Write `continue-on-error: ${{ matrix.experimental == true }}` on the job (in the same column as `runs-on`).
- When a job fails, the others should not be cancelled: `fail-fast` off.
