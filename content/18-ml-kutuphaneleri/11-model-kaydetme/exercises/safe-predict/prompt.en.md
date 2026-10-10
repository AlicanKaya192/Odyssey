`safe_predict(rows)` builds a DataFrame from a list of dictionaries and returns the
positive class probabilities (3 places). The keys in the incoming
dictionaries may be in any order; the model expects the training order
(`COLUMNS`). The starter code passes it unordered and gets an error.

**Expected output:**

```
[0.978, 0.021]
```
