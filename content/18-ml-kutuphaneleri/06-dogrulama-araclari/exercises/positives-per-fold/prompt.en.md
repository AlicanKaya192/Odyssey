`positives_per_fold(labels, k)` should split the label list with
`StratifiedKFold(k)` (without shuffling) and return the number of positives
(1) in each **test** fold as a list. The starter code uses `KFold`; with
sorted labels all positives fall into the last fold.

**Expected output:**

```
[2, 2, 2]
```
