Write the function `min_max(train, test)`: scale each column so that the
training data's **minimum is 0 and maximum is 1**, and apply it to the test
data: `(x − min) / (max − min)`. If a column is constant in training
(`max == min`), that column's result is 0. Return `.round(3).tolist()`.

Test values may fall outside 0–1; that is right, do not clip.

**Expected output:**

```
[[0.25, 0.0], [1.5, 0.0], [-0.25, 0.0]]
```
