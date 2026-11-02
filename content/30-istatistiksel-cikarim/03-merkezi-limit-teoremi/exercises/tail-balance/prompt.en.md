At which size do spend (`spend`) means turn into a bell? For `n` = 30 and
`n` = 2000 (the same `rng`, 30 first) draw 2000 sample means each:
`rng.choice(y, size=(2000, n)).mean(axis=1)`. `se = sigma / np.sqrt(n)`. On
each line write `n`, the share **below** `mu - 1.96 * se` and the share
**above** `mu + 1.96 * se` (3 places). For a bell shape both are near
0.025.

**Expected output:**

```text
30 0.0 0.046
2000 0.02 0.029
```
