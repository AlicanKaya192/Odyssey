Write the function `log_entry(row, probability, version, month)` that builds the line written into the prediction log:

- If the probability is not between 0 and 1 (both ends included), return `None`: a broken prediction shouldn't enter the log.
- Otherwise return the dictionary `{"id": ..., "month": ..., "model_version": ..., "churn_probability": ...}`; the probability rounded to three digits, the ID `row["id"]`.

**Expected output:**

```
id C7
month 2026-05
model_version 3
churn_probability 0.901
None
```
