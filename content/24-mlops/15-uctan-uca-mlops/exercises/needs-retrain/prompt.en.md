Write the function `needs_retrain(live, base, drift, max_drop, max_drift)` for the pipeline's trigger. Return `True` if either of these holds, otherwise `False`:

- `live` is less than `base - max_drop` (accuracy dropped).
- `drift` is greater than `max_drift` (the drift is large).

**Expected output:**

```
False
True
True
```
