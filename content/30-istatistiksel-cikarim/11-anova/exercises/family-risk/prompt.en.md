`family_risk(k, alpha)` should return the number of pairs for `k` groups and,
if those pairs were independent, the probability of at least one false
alarm: `[pairs, risk]`. The number of pairs is `k * (k - 1) // 2`, the risk
`1 - (1 - alpha) ** pairs` (3 places). The starter code takes the number of
pairs to be the number of groups and the risk to be `alpha`.

**Expected output:**

```text
[6, 0.265]
[45, 0.901]
```
