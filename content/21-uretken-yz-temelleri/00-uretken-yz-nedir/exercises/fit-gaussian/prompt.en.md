`fit_gaussian(name)` should fit a normal distribution to **all** fish of the
species and return a `{"mean": ..., "cov": ...}` dictionary. The mean is a
list rounded to 2 places; the covariance is computed with
`np.cov(..., rowvar=False)` and given as a nested list rounded to 2
places.

**Expected output:**

```
[24.04, 304.46]
[15.38, 192.76]
[192.76, 4431.61]
```
