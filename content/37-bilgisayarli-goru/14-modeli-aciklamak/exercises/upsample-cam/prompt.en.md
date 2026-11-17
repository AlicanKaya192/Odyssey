`upsample_cam(cam, size)` should enlarge a small map to `size × size` with
`F.interpolate` using `mode="nearest"` and return it as a list of lists.

**Expected output:**

```
[1.0, 1.0, 0.0, 0.0]
[1.0, 1.0, 0.0, 0.0]
[0.0, 0.0, 2.0, 2.0]
[0.0, 0.0, 2.0, 2.0]
```
