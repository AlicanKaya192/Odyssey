`best_matches(predicted, truth)` should use `box_iou` to find the true box with
the highest IoU for each prediction: `[true box number, IoU]` for each
prediction (IoU with 2 places). For a prediction that overlaps no true box,
the number is `-1`.

**Expected output:**

```
[0, 0.82]
[1, 0.61]
[-1, 0.0]
```
