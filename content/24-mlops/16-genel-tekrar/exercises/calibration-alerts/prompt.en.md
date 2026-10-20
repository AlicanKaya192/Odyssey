Write the function `calibration_alerts(rows, limit)` that joins monitoring and concept drift:

- Every row is `[month, expected, actual]`.
- Return, in order, the months where the absolute difference between expected and actual is greater than `limit`.

**Expected output:**

```
[4, 6]
[6]
[0, 3, 4, 6]
```
