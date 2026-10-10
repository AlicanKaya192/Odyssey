`distances(points)` should return the Euclidean distance of every point to
every point as a matrix (nested list) rounded to 2 places. **Loops are
forbidden:** take the differences with `points[:, None, :] -
points[None, :, :]`, sum their squares over the last axis, square root.

**Expected output:**

```
[0.0, 5.0, 10.0]
[5.0, 0.0, 5.0]
[10.0, 5.0, 0.0]
```
