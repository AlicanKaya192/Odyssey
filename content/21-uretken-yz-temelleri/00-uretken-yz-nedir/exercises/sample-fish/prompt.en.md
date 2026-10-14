`sample_fish(name, n, seed)` should find the mean and covariance from all fish
of the species, create a generator with `np.random.default_rng(seed)` and
produce `n` new fish with `multivariate_normal`. The result is a nested
list rounded to 1 place: each fish is `[length, weight]`.

**Expected output:**

```
[28.0, 519.5]
[33.1, 520.9]
[27.3, 460.9]
```
