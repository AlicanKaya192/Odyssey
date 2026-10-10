`fit_decay(t, y)` should fit the model `a * exp(-k * t)` to the measurements
with `curve_fit`. The starting guess is `p0=[max(y), 0.1]`. Return `[a, k,
half_life]`: `a` and `k` with 3 places, the half-life `ln(2) / k` with 2
places.

**Expected output:**

```
[80.203, 0.349, 1.98]
```
