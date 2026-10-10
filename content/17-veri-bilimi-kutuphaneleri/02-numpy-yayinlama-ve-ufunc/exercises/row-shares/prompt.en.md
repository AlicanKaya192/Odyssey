`row_shares(matrix)` should divide each row by its own total; the result is
a nested list rounded to 3 places. The starter code leaves the total with
shape `(n,)`: on some tables it errors, on square tables it silently divides
along the wrong axis. Use `keepdims=True`.

**Expected output:**

```
[[0.25, 0.75], [0.5, 0.5]]
```
