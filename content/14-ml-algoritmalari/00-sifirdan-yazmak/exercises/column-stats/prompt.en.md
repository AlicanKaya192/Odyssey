Write the function `column_stats(rows)` with NumPy: `rows` is a nested list
(rows are samples, columns are features). It returns a list of
`[mean, standard deviation]` for each column; the standard deviation is
divided by `n` (`ddof=0`), both `round(..., 3)`.

Turn it into an array with `np.array(rows)`, use `axis=0`; do not sum with a
loop.

**Expected output:**

```
55.0 11.18
3.0 0.354
```
