The workflow only has the tests and only starts by hand. Run the pipeline every month:

- Add a trigger at **03:00 UTC** on the 1st of every month (`schedule`); keep `workflow_dispatch`.
- Add a `retrain` job: it starts when `test` finishes, `ubuntu-latest`, `timeout-minutes: 30`.
- Steps in order: get the code (`actions/checkout@v4`); set up Python 3.13 (`actions/setup-python@v5`, `cache: pip`); `python -m pip install -r requirements.txt`; `python pipeline.py`; keep the report **in every case** (`actions/upload-artifact@v4`, `name: pipeline-report`, `path: report.txt`).
