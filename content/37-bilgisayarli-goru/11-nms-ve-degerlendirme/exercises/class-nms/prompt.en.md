`class_nms(boxes, scores, labels, conf, iou)` should first drop the boxes with
a score below `conf`, then do per-class NMS with `batched_nms`. Return the
remaining boxes' numbers **in the original list** (in score order).

**Expected output:**

```
[0, 3, 2]
[0, 3, 2]
```
