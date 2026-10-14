`pick_counts(probs, n, seed)` should pick a category `n` times from the
probability list and return how many times each category was picked, as a
list. Build the cumulative sum with `np.cumsum` and pick with
`np.searchsorted(cum, u, side="right")`; the uniform numbers are
`np.random.default_rng(seed).random(n)`. Count with
`np.bincount(..., minlength=len(probs))` and return with `tolist()`.

**Expected output:**

```
[471, 313, 216]
[44, 6]
```
