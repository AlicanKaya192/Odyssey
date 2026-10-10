`pdp_values(column, points)` should return the partial dependence averages of the
given column on the test data (`grid_resolution=points`, rounded to integers).
The starter code fails on an integer column like `floor`; turn the column
into `float` first.

**Expected output:**

```
[106, 124, 159, 163, 163]
[118, 158, 157, 115]
```
