`my_nms(boxes, scores, threshold)` should do NMS itself: sort the boxes by
score, keep the highest-scoring one, drop those whose IoU with it is above
`threshold`, continue with the rest. Return the kept boxes' numbers in the
order they were kept. You may use `box_iou` for IoU; do not use `nms`.

**Expected output:**

```
[0, 3]
[4, 1]
[0, 3, 1, 4]
```
