`scorer.py` has a model with fixed weights: `churn_probability(row)` and `VERSION`. Write the function `score_batch(rows)` that does batch scoring:

- For every customer produce a list `[id, probability, version]`; the probability rounded to three digits, the version `VERSION`.
- Keep the customers' order.

**Expected output:**

```
['C1', 1.0, 3]
['C2', 0.01, 3]
['C3', 0.618, 3]
```
