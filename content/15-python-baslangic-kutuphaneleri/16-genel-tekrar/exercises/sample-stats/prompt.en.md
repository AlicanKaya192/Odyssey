Write the function `sample_stats(seed, n)`: with `random.Random(seed)`,
draw `n` values from a normal distribution with mean 100 and standard
deviation 15 (`gauss`) and return the tuple `(mean, sample standard
deviation, share above 130)`; the first two `round(..., 1)`, the share
`round(..., 3)`.

**Expected output:**

```
(99.8, 15.1, 0.017)
(97.8, 16.7, 0.1)
```
