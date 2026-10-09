Write the function `threshold_for_recall(y, score, target)`: walk the scores
from large to small; return the threshold at which the recall (with
`score >= threshold` positive) first reaches `target`. That is, the **highest**
threshold reaching the target. The scores are all different.

**Expected output:**

```
0.7
0.2
```
