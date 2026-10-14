The starter code prepares 2000 points from the ring (`x0`), the cluster
centres and the lesson's noise schedule. `noisy_near(t, seed)` should build
the noisy state at step `t`:
`eps = np.random.default_rng(seed).normal(size=x0.shape)`,
`xt = sqrt(alpha_bar[t]) * x0 + sqrt(1 - alpha_bar[t]) * eps`. Return
`[share of points whose distance to the nearest centre is below 0.3,
standard deviation of all values of xt]`; the share rounded to 3 places, the
deviation to 2, as `float`s.

**Expected output:**

```
0 [0.993, 1.41]
29 [0.109, 1.3]
99 [0.041, 1.01]
```
