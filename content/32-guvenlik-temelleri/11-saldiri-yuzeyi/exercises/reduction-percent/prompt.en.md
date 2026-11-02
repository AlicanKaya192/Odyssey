`reduction_percent(before, after)` should return by what percentage the
surface score shrank, with `round(..., 1)`: `(before - after) / before *
100`.

If `before` is zero, the division cannot be done; return `0.0` then.

**Expected output:**

```
18.8
0.0
0.0
75.0
```
