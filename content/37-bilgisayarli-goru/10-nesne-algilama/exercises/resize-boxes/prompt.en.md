`resize_boxes(boxes, old_size, new_size)` should multiply the boxes by the same
ratio when a square picture is scaled from `old_size` to `new_size`, and clip
them into the new picture with `clip_boxes_to_image` (returns a list).

**Expected output:**

```
64 [8.0, 12.0, 28.0, 24.0]
64 [50.0, 40.0, 62.0, 60.0]
16 [2.0, 3.0, 7.0, 6.0]
16 [12.5, 10.0, 15.5, 15.0]
```
