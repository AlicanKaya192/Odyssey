Write the function `average_precision(y, score)`: sort the scores from large
to small; at each position precision is `TP / position` and recall is
`TP / number of positives`; multiply each increase in recall by the precision at
that point and add up. `round(..., 4)`.

No `average_precision_score`.

**Expected output:**

```
0.7222
1.0
```
