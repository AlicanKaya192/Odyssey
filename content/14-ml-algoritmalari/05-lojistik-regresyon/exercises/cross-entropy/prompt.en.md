Write the function `cross_entropy(y, p)`: the log loss
`−mean(y log p + (1 − y) log(1 − p))`. To avoid `log(0)`, first
`p = np.clip(p, 1e-12, 1 - 1e-12)`. Return `round(..., 4)`.

No `log_loss`.

**Expected output:**

```
0.2798
4.6052
0.0
```
