`share_interval(k, n)` should return the 95% **Wilson** interval as
`[low, high]` with 4 places for a sample where `k` out of `n` people bought
(`proportion_confint(..., method="wilson")`). The starter code uses Wald
(`"normal"`): with `k = 0` the interval collapses to a single point.

**Expected output:**

```text
[0.1027, 0.1692]
[0.0, 0.1611]
```
