`optimal_matches(predicted, truth, threshold)` should find the matching that
maximises the total IoU with `box_iou` and `linear_sum_assignment`, and
return the pairs whose IoU is not below `threshold` as a sorted list of
`[prediction, truth]`.

**Expected output:**

```
[[0, 0], [1, 1]]
[[1, 0], [2, 1]]
```
