`price_interval(area, age)` should return the prediction and the **single
observation** interval for one house: `[mean, obs_low, obs_high]` (1 place).
The starter code calls `sm.add_constant` with its default on one row; `const`
is not added and the prediction fails.

**Expected output:**

```
[330.9, 256.9, 405.0]
```
