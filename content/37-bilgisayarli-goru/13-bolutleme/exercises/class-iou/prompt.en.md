`class_iou(predicted, truth, num_classes)` should return the IoU of each class
(common pixels / union pixels) rounded to 3 places, as a list. For a class
with an empty union, write `-1`.

**Expected output:**

```
[0.636, 0.8, 0.25]
[0.636, 0.8, 0.25, -1]
```
