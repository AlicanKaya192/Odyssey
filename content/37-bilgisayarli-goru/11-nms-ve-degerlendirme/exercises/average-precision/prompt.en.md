`average_precision(hits, total_truth)` should compute AP rounded to 3 places from
a list of right (1) / wrong (0) predictions in score order: precision and
recall at each step; the envelope of precision (at each point the largest to
its right); each increase in recall × the envelope at that point, summed.

**Expected output:**

```
0.704
0.833
0.333
```
