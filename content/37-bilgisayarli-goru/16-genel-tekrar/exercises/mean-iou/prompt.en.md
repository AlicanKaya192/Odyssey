`mean_iou(predicted, truth, num_classes)` should return the mean of the
per-class IoUs of two masks rounded to 3 places. A class found neither in the
prediction nor in the truth (empty union) does not enter the mean.

**Expected output:**

```
0.611
0.611
```
