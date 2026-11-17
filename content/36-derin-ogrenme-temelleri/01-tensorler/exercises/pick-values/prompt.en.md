`pick(rows, limit)` should build a tensor from the table and return two lists:
the first column and the elements greater than `limit` (row by row, left to
right).

**Expected output:**

```
[[1, 8, 5], [9, 8, 7]]
[[1, 8, 5], []]
```
