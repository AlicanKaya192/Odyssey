Write the function `estimate_pi(n, seed)`: build `r = random.Random(seed)`;
take a point `n` times with `x, y = r.random(), r.random()` and count those
with `x * x + y * y <= 1`. Return `4 * inside / n` with `round(..., 3)`. The
order of calls matters: first `x`, then `y`.

**Expected output:**

```
3.128
3.142
```
