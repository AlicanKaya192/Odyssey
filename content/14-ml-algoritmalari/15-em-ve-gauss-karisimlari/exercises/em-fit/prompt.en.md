Write the function `em_fit(xs, weights, mus, variances, iters)`: `iters`
times the E step (responsibilities) and the M step (share, mean, variance).
At the end return the lists `(shares, means, variances)` with
`.round(3).tolist()`. `normal_pdf` is given.

**Expected output:**

```
[0.5, 0.5]
[-0.06, 5.04]
[0.53, 0.77]
```
