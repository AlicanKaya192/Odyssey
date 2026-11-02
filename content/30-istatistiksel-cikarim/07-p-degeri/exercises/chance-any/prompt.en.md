`chance_any(k, alpha)` should return, with 3 places, the probability that
**at least one** of `k` independent tests has `p < alpha` when there is no
difference: `1 - (1 - alpha) ** k`. The starter code writes `k * alpha`: it
gives impossible probabilities like 1 for 20 tests and 1.5 for 30.

**Expected output:**

```text
0.05
0.642
```
