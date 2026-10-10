`safe_sqrt(values)` should take the square root of non-negative values and
put `-1.0` in place of negative ones. Use `np.sqrt(..., where=..., out=...)`:
`out` starts as an array full of `-1.0` (`np.full`). Return the result as a
list.

**Expected output:**

```
[2.0, -1.0, 3.0, -1.0, 0.0]
```
