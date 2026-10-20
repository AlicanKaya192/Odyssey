The prediction log is a list (`{"id": ..., "churn_probability": ...}`), the real outcomes a dictionary that arrives later (`{id: 0 or 1}`). Write the function `join_outcomes(log, outcomes, threshold)` and return `[correct, total]`:

- Skip the entries whose outcome hasn't arrived yet.
- If the probability is at or above `threshold`, the prediction is `1`, otherwise `0`.
- Count it as correct if the prediction equals the real outcome.

**Expected output:**

```
[2, 3]
```
