`match_counts(predicted, truth, threshold)` should walk the predictions
(`[x1, y1, x2, y2, class, confidence]`) from the highest confidence down and
match each with the unmatched true box (`[x1, y1, x2, y2, class]`) of the
same class with the highest IoU. If the IoU is not below the threshold it is
a true positive, otherwise a false positive. Return `[TP, FP, FN]`. Use the
given `iou` function.

**Expected output:**

```
[1, 2, 1]
```
