`best_depth(depths)` should run `validation_curve(DecisionTreeClassifier(random_state=0),
X, y, param_name="max_depth", param_range=depths, cv=5)` and return
`[best_depth, test_means]`: the means as a list with 3 places, the best depth
the one with the highest test mean (the first on a tie).

**Expected output:**

```
[4, [0.773, 0.79, 0.82, 0.787]]
```
