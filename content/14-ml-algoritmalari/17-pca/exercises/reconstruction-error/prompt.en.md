Write the function `reconstruction_error(X, k)`: project the data onto
the first `k` components, rebuild with `Z @ Vₖᵀ + mean` and return the mean
squared difference from the original, `round(..., 4)`. If `k` is all
dimensions the error must be 0.

**Expected output:**

```
0.1251
0.0046
0.0
```
