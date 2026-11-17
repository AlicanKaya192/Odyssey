`anchor_match(objects, anchors)` should return, for each `[width, height]`
object, the position of the anchor with the most similar shape: the anchor
with the highest IoU computed as if both boxes had the same centre.

**Expected output:**

```
[1, 2, 0, 0]
```
