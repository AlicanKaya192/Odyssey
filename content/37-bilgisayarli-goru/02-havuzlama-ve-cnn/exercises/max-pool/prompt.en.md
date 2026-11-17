`max_pool(fmap, size)` should split the nested list into non-overlapping
`size × size` squares and keep the largest value of each (stride = `size`).
Rows and columns that do not fit at the end are dropped. Do not use
PyTorch.

**Expected output:**

```
[[6, 2], [2, 9]]
[[5]]
```
