`sample_stats(mu, logvar, n, seed)` should draw `n` codes with the
reparameterization trick: `std = np.exp(0.5 * logvar)`,
`z = mu + std * rng.normal(size=(n, len(mu)))`, with the generator
`np.random.default_rng(seed)`. Return a single list holding first the mean
of every dimension, then its standard deviation; every number a `float`
rounded to 2 places.

**Expected output:**

```
[1.5, -0.5, 0.37, 1.0]
[0.01, 1.66]
```
