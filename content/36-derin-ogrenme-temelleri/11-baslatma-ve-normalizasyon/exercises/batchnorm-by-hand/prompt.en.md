`by_hand(x)` should do by hand what `nn.BatchNorm1d` does in training mode:
subtract each column's mean and divide by `sqrt(variance + 1e-5)`. The variance is
biased (`unbiased=False`). If it is right, `check_batchnorm` prints `True`.

**Expected output:**

```
True
```
