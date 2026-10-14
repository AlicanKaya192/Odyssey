`bootstrap(a, b, n, seed)` should take two settings' per-question correct
(1) / wrong (0) lists. With `rng = np.random.default_rng(seed)`, draw
`pick = rng.integers(0, len(a), len(a))` `n` times and compute the difference
`a[pick].sum() - b[pick].sum()`. Return `[observed difference, 5th percentile,
95th percentile]`; the percentiles with `np.percentile`, as `float`s rounded
to 1 place.

**Expected output:**

```
[2, 0.0, 4.0]
```
