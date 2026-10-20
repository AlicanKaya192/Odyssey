Write the function `audit_codes(release, min_gain)` that writes the lesson's auditor with short codes. Add these codes in order:

- `"seed"`: `release["seed"]` is `None`.
- `"digest"`: `release["data_digest"]` is empty.
- `"gate"`: `gate_month` is less than `trained_month`.
- `"gain"`: `gain` is less than `min_gain`.
- `"threshold"`: `threshold` is exactly `0.5`.
- `"fallback"`: `fallback` is `None`.
- `"drift"` and `"calibration"`: if missing from the `monitors` list (in this order).

**Expected output:**

```
seed
digest
gate
gain
threshold
fallback
drift
calibration
[]
```
