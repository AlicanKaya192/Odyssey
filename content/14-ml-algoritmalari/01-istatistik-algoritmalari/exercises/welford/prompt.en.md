Write the function `welford(values)` with **Welford's algorithm**, walking
the list once: it returns the tuple `(mean, variance)`, both `round(..., 4)`;
the variance is `M2 / n`.

For each value: `n += 1`, `delta = v − mean`, `mean += delta / n`,
`m2 += delta * (v − mean)`.

**Expected output:**

```
(5.0, 4.0)
(10.0, 0.0)
```
