Write the function `bootstrap(n, seed)`: draw `n` indices from `0..n−1`
**with replacement**: `np.random.default_rng(seed).integers(0, n, n)`. Return
the list.

**Expected output:**

```
[6, 5, 4, 2, 2, 0, 0, 0]
[2, 2, 3, 4, 0]
```
