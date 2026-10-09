Write the function `estimate_area(n, seed)` with **Monte Carlo**: it
estimates the area under the curve `y = x²` on `0..1` (the true value is
`1/3`). The generator is `rng = random.Random(seed)`.

`n` times: first `x = rng.random()`, then `y = rng.random()`; if `y <= x * x`
the point is under the curve. The estimate: the number of points below `/ n`,
`round(..., 4)`.

**Expected output:**

```
100 0.27
10000 0.3392
1000000 0.334
```
