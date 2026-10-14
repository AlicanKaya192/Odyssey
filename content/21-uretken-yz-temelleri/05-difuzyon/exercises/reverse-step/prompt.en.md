`reverse_step(x, eps_hat, t, z)` should apply one step of the reverse
process: `(x - betas[t] / sqrt(1 - alpha_bar[t]) * eps_hat) / sqrt(alphas[t])`;
if `t` is not 0, add `sqrt(betas[t]) * z` to the result (no noise at the last
step). `x`, `eps_hat` and `z` are lists of points. The result is a nested
list with every number rounded to 4 places.

**Expected output:**

```
[[0.7319, -1.2633], [2.0708, 0.1124]]
[[0.499, -1.0021]]
```
