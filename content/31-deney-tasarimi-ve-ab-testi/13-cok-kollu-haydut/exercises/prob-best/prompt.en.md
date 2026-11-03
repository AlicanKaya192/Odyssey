`prob_best(k, n, draws=20000, seed=0)` should return each arm's probability
of being best as a list with 3 places. The starter code builds the Beta
distribution's parameters wrong: they should be `1 + k` and `1 + n - k`.

**Expected output:**

```text
[0.044, 0.413, 0.543]
```
