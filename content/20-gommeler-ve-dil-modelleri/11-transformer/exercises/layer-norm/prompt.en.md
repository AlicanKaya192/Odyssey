`layer_norm(rows)` should normalise each row separately: subtract the mean,
divide by `√(variance + 0.00001)` (variance divided by the row's length). 3
places.

**Expected output:**

```
[-1.225, 0.0, 1.225]
[-0.707, -0.707, 1.414]
```
