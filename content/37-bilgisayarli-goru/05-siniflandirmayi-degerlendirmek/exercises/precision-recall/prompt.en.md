`precision_recall(matrix, c)` should return class `c`'s precision and recall
from a confusion matrix (row true, column predicted) rounded to 3 places, as
`[precision, recall]`. If a denominator is 0, that value is `0.0`.

**Expected output:**

```
0 [0.833, 0.833]
1 [0.333, 0.5]
2 [1.0, 0.5]
[0.0, 0.0]
```
