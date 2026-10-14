The repository has `cart.py`, its tests (`test_cart.py`) and `requirements.txt`.

Complete the workflow:

- Run on both the `push` and the `pull_request` event: `on: [push, pull_request]`
- After downloading the code, install Python **3.13** (`actions/setup-python@v5`, with `python-version: "3.13"` under `with:`)
- Install the dependencies with `pip install -r requirements.txt`
- Run the tests with `python -m pytest`
