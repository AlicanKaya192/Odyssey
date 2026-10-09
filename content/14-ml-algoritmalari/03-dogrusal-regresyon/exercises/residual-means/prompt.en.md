Write the function `residual_means(x, y, parts)`: sort by `x`, fit a line
(intercept + slope, `lstsq`), split the residuals (`y − ŷ`) into `parts` parts
with `np.array_split` and return each part's mean, `round(..., 2)`, as a
list.

**Expected output:**

```
[3.0, -6.0, 3.0]
```
