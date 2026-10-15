Prepare the `test` job for debugging:

- If it hangs it should stop after 15 minutes: `timeout-minutes: 15`.
- pytest should write the results to a file: `python -m pytest -q --junitxml=report.xml`.
- The last step should keep the report **only if the tests fail**: `actions/upload-artifact@v4`, `name: test-report`, `path: report.xml`.
