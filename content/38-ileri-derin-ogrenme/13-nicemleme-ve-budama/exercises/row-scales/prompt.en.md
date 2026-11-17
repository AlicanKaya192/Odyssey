`row_scales(weight)` should compute the scales of per-channel quantisation:
for every row, that row's largest absolute value / 127. Return a list with 4
places.

**Expected output:**

```
[0.001, 0.1]
```
