**The order in a red run**

1. Which job, which step failed?
2. The **first** error line in the log (the "exit code 1" at the end is
   the result, not the cause).
3. Reproduce it locally with the same versions and the same command.
4. If it does not reproduce, look at the differences (table below).
5. If it still cannot be found, detailed logs: `ACTIONS_STEP_DEBUG` =
   `true`, start the run again with "debug logging".

**Preparing the pipeline for debugging**

```yaml
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: test-report
          path: report.xml
```

| Part | What it gives |
|---|---|
| `timeout-minutes` | A hanging test job does not wait for hours (default 360) |
| `--junitxml` | A test report a machine can read |
| `if: failure()` + artifact | The report is kept only on failure |

**"It works on my machine" differences**

| Difference | Symptom |
|---|---|
| Upper and lower case in file names on Linux | `FileNotFoundError: data.csv` |
| UTC clock | Date tests fail close to midnight |
| Unpinned package | A test that passed yesterday fails today with no code change |
| A file created by hand | `FileNotFoundError` in the pipeline |
| Line endings (`\r\n` / `\n`) | A text comparison fails |

**Quarantine**

```yaml
  quarantine:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q -m flaky
```

- The main job with `-m "not flaky"`, the quarantine with `-m flaky`.
- The mark in `pyproject.toml`: `markers = ["flaky: known flaky tests"]`.
- Every test in quarantine has an owner and a deadline.
- The re-run button is not a fix.
