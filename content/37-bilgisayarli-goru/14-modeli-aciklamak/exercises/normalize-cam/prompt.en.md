`normalize_cam(cam)` should zero the map's negative values (ReLU), then divide
by the largest value and return a list of lists rounded to 2 places. If every
value is 0 or negative, do not divide; return the map of zeros.

**Expected output:**

```
[[0.0, 0.0], [0.5, 1.0]]
[[0.0, 0.0], [0.0, 0.0]]
```
