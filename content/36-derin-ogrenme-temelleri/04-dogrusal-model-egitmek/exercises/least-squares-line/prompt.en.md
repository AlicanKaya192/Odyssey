`fit_line(xs, ys)` should find the line without gradient descent, with
`torch.linalg.lstsq`: build a matrix `A` whose first column is `x` and second
column is ones. Return `[w, b]` with 3 places.

**Expected output:**

```
[2.0, 1.0]
[-1.0, 0.5]
```
