Write the function `pegasos_step(x, yi, w, b, lam, t)`: `lr = 1 / (lam · t)`.
If `yi (x·w + b) < 1`, `w = (1 − lr·lam) w + lr·yi·x` and `b += lr·yi`;
otherwise only `w = (1 − lr·lam) w`. Return the tuple `(w list, b)` with values
`round(..., 4)`.

**Expected output:**

```
[10.0, 20.0] 10.0
[5.0, 10.0] 10.0
```
