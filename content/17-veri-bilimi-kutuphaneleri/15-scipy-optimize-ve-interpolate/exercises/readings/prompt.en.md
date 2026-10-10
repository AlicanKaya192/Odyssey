`readings(hours, temps, at)` should estimate the temperature at hour `at` in
two ways: linear (`np.interp`) and a non-overshooting curve
(`interpolate.PchipInterpolator`). Return `[linear, pchip]` (2 places
each).

**Expected output:**

```
[18.5, 18.7]
[11.0, 10.31]
```
