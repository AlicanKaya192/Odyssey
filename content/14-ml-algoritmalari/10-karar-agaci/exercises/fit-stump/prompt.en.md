Write the function `fit_stump(X, y)`: a one-question tree (a decision stump).
Across all features and midpoint thresholds find the one minimising the
weighted Gini (on a tie the earlier feature and the smaller threshold). Return
`[feature, threshold, left label, right label]`; the threshold
`round(..., 4)`, the labels the majority on that side (the smaller on a tie).
`gini` is ready.

No `DecisionTreeClassifier`.

**Expected output:**

```
[0, 4.5, 0, 1]
```
