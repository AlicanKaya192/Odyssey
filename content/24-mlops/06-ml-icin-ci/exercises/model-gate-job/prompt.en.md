The pipeline only has the code tests. Add a `model-gate` job:

- It should start when `test` finishes; the machine is `ubuntu-latest`.
- Steps in order: get the code (`actions/checkout@v4`); set up Python 3.13 (`actions/setup-python@v5`, `cache: pip`); `python -m pip install -r requirements.txt`; `python train.py`; `python check_quality.py`.
