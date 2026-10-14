`denoise(k, sigma, seed)` should add the noise
`np.random.default_rng(seed).normal(0, sigma, X_test.shape)` to the test
images, encode and rebuild the noisy images with the first `k` PCA directions
of the training data, and return two errors:
`[noisy against clean, rebuilt against clean]`, as `float`s rounded to 4
places.

**Expected output:**

```
8 [0.0396, 0.0296]
16 [0.0396, 0.0213]
32 [0.0396, 0.0222]
```
