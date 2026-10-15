The pipeline has only `lint`. Add a `test` job:

- It should start when `lint` finishes; the machine is `ubuntu-latest`, `timeout-minutes: 15`.
- Matrix: `python: ["3.12", "3.13"]`, `fail-fast: false`.
- Steps: get the code; `actions/setup-python@v5` (`python-version: ${{ matrix.python }}`, `cache: pip`); `python -m pip install -r requirements-dev.txt`; `python -m pytest -q --cov=tempconv --cov-fail-under=90`.
