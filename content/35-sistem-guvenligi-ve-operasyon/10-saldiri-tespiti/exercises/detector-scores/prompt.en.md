`detector_scores(alerts, attacks)` should return `[precision, recall]`
from the ids of alerted events and of real attacks (two lists), both
rounded to 2 places. Precision is `TP / (TP + FP)`, recall is
`TP / (TP + FN)`. If a denominator is 0, that value is `0.0`.

**Expected output:**

```
[0.5, 0.67]
[0.0, 0.0]
```
