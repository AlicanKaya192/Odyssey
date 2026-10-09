Write the function `gnb_predict(X, y, Xq)`: for each class the prior, mean and
variance (`+ 1e-9 · the largest variance`); for each query return the class with
the largest log prior + Gaussian log-likelihood (a list of `int`s).

No `GaussianNB`.

**Expected output:**

```
[0, 1, 0]
```
