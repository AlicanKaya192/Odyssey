`quantize_int8(values)` should do symmetric, per-tensor quantisation: scale
`largest |w| / 127`, `round(w / scale)`, clip to `[-127, 127]`, `int8`.
Return `[list of int8 values, scale]`, the scale with 4 places
(`round(scale.item(), 4)`).

**Expected output:**

```
[[50, -127, 1], 0.01]
```
