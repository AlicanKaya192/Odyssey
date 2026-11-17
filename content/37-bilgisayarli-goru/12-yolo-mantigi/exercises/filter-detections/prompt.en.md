`filter_detections(xyxy, conf, cls, wanted, min_conf, iou)` should keep, from
a detection library's output, only the boxes of class `wanted` whose
confidence is not below `min_conf`, apply `nms` to them and return the
remaining boxes as a list.

**Expected output:**

```
0 0.5 1
[10.0, 10.0, 30.0, 60.0]
0 0.3 2
[10.0, 10.0, 30.0, 60.0]
[100.0, 5.0, 120.0, 55.0]
2 0.5 1
[50.0, 20.0, 90.0, 45.0]
```
