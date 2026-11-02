`t_multiplier(level, n)` should return, with 3 places, the t multiplier for
a mean's interval at confidence `level` with a sample of `n`:
`stats.t.ppf((1 + level) / 2, df=n - 1)`. The starter code gives the normal
distribution's multiplier and never uses `n`.

**Expected output:**

```text
2.776
1.984
2.861
```
