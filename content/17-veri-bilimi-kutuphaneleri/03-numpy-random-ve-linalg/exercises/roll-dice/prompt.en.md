`roll(seed, n)` should build a generator with `np.random.default_rng(seed)`,
roll `n` dice (`integers(1, 7, size=n)`) and return a list. The starter code
uses the global `np.random.seed`; switch it to its own generator.

**Expected output:**

```
[1, 5, 4, 3, 3] True
```
