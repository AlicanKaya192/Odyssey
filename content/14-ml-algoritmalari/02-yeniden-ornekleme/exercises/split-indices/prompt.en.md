Write the function `split_indices(n, test_size, seed)`: shuffle the indices
with `np.random.default_rng(seed).permutation(n)`; the first
`int(n * test_size)` are the test, the rest the training. It returns the tuple
`(train, test)` as lists (`.tolist()`).

**Expected output:**

```
[0, 1, 2, 5, 9, 6, 3]
[8, 4, 7]
```
