The starter code trains the lesson's network for 3000 steps (`net`).
`generate(n, seed)` should write the reverse process:
`rng = np.random.default_rng(seed)`, `x = rng.normal(size=(n, 2))`; for `t`
from 99 to 0: `eps_hat = forward(features(x, np.full(n, t)), net)[-1]`, the
reverse-step formula, and if `t` is not 0 add
`np.sqrt(betas[t]) * rng.normal(size=x.shape)`. At the end return, with
`mode_report(x)`, `[number of clusters with at least 2% of n, share near a
cluster]`; the share a `float` rounded to 3 places.

**Expected output:**

```
[8, 0.615]
```
