The batch prediction workflow only starts by hand and doesn't produce the scores. Complete it:

- It should run every night at **02:00 UTC** (`schedule`); keep `workflow_dispatch`.
- Add `timeout-minutes: 20` to the `score` job.
- After the setup, run `python score.py` and keep the result: `actions/upload-artifact@v4`, `name: scores`, `path: scores.csv`.
