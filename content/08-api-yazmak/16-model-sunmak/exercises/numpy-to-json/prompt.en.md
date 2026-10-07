`POST /predict` gives `500` on every request: NumPy values were put in the
answer.

**What to do:** make the answer convertible to JSON:

- `label`: a Python `int`
- `probabilities`: a list of the three probabilities, each `round(..., 3)`

- `5.1, 3.5, 1.4, 0.2` → `{"label": 0, "species": "setosa", "probabilities": [...]}`
