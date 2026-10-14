`rejection_stats(n, seed)` should draw samples from the density
$f(x) = 6x(1-x)$ on $[0, 1]$ by rejection sampling. From the same generator
(`np.random.default_rng(seed)`) first produce `n` values of `x`, then `n`
heights (`random(n) * 1.5`); keep those whose height is below
`6 * x * (1 - x)`. Return `[acceptance rate, mean of the kept values]`, both
`float`s rounded to 3 places.

**Expected output:**

```
[0.664, 0.502]
[0.73, 0.482]
```
