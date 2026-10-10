`as_matrix(values, cols)` should turn the list into a matrix with `cols`
columns (`reshape(-1, cols)`) and return it as a nested list. If the item
count does not fit (`ValueError`), return the text `"error"`.

**Expected output:**

```
[[1, 2], [3, 4], [5, 6]]
error
```
