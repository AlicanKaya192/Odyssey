Write the function `gd_step(A, y, w, lr)`: the first column of `A` is 1 (the
intercept). The MSE gradient is `(2/n) Aᵀ (A w − y)`; the new weights are
`w − lr · gradient`. Return `.round(4).tolist()`.

**Expected output:**

```
[0.7333, 1.1333]
[1.0178, 1.58]
[1.1262, 1.7573]
```
