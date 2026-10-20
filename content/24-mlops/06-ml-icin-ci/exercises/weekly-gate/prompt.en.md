The gate only runs on pull requests. Since the libraries and the data can change even with no change to the code, it should also run once a week:

- Every **Monday at 06:00 UTC** (`schedule`) and by hand from the Actions tab (`workflow_dispatch`). Keep the `pull_request` trigger.
- At the end of the `model-gate` job, add a step that keeps the measurements: `actions/upload-artifact@v4`, running **in every case**, `name: metrics`, `path: metrics.json`.
