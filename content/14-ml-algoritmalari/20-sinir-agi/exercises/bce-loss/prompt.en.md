Write the function `bce_loss(y, p)`: `−mean(y log p + (1 − y) log(1 − p))`;
first clip `p` to `[1e-12, 1 − 1e-12]` (`np.clip`), return
`round(..., 4)`.

**Expected output:**

```
0.2798
0.0
```
