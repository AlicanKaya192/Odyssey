`batch_sizes(n, batch_size, drop_last)` should build a `TensorDataset` of `n`
numbers, walk over it with a `DataLoader` and return the size of each batch as a
list.

**Expected output:**

```
[4, 4, 2]
[4, 4]
```
