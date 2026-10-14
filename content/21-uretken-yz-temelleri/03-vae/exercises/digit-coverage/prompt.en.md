The starter code prepares the lesson's VAE (`P`) and the judge (`judge`).
`coverage(n, seed)` should draw `n` 2-dimensional codes from the standard
normal (`np.random.default_rng(seed).normal(size=(n, 2))`), turn them into
images with `decode(z, P)[1]` and return two values: the number of digits
that have at least 5% of `n` images according to the judge's prediction
(an `int`) and the share of images the judge is more than 90% sure about
(a `float` rounded to 3 places).

**Expected output:**

```
[10, 0.333]
[10, 0.332]
```
