`fit_line(xs, ys)` should find the line `y ≈ a + b x` with least squares
and return `[a, b]` rounded to 3 places. Build a matrix `X` whose first column
is 1 and second column is `xs` (`np.column_stack`) and use
`np.linalg.lstsq(X, ys, rcond=None)`.

**Expected output:**

```
[0.15, 1.94]
```
