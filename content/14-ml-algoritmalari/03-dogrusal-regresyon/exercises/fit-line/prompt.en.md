Write the function `fit_line(x, y)`: the one-feature least squares line.
The slope is `Σ(x − x̄)(y − ȳ) / Σ(x − x̄)²`, the intercept `ȳ − slope · x̄`.
It returns the tuple `(intercept, slope)`, both `round(..., 4)`.

**Expected output:**

```
(0.05, 1.99)
(5.0, 0.0)
```
