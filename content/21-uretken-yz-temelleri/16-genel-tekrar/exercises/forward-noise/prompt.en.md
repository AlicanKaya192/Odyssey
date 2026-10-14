`noisy(x0, eps, alpha_bar)` should apply diffusion's one-step noise formula
(05): `sqrt(alpha_bar) * x0 + sqrt(1 - alpha_bar) * eps`. The result is a list
with every number rounded to 3 places.

**Expected output:**

```
[1.1, -1.3]
```
