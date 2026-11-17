`iou(a, b)` should return the IoU of two xyxy boxes rounded to 3 places. If
the common region's width or height comes out negative, count it as 0. Do
not use torchvision's `box_iou`.

**Expected output:**

```
[10, 10, 20, 20] 1.0
[15, 10, 25, 20] 0.333
[12, 12, 22, 22] 0.471
[30, 30, 40, 40] 0.0
[0, 0, 10, 10] 0.0
```
