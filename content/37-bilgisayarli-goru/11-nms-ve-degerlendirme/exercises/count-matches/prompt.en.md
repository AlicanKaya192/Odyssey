`count_tp_fp_fn(pred_boxes, pred_scores, truth_boxes, threshold)` should do
greedy matching: go through the predictions in score order; each takes the
not-yet-matched true box with the highest IoU, if that IoU ≥ `threshold`.
Return `[TP, FP, FN]`.

**Expected output:**

```
[2, 3, 1]
[2, 0, 1]
```
