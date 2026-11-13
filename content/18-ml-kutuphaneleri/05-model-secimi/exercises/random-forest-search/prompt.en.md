`random_forest_search(n_iter)` should run
`RandomizedSearchCV(RandomForestClassifier(min_samples_leaf=10, random_state=0),
space, n_iter=n_iter, cv=3, random_state=0)` on the training data. The space: `"n_estimators":
randint(10, 60)`, `"max_depth": randint(2, 8)`. Return `[best_max_depth,
best_score]` (depth an `int`, score with 3 places).

`min_samples_leaf=10` keeps the leaves large: in very small leaves two splits
can get exactly the same score and the processor breaks that tie differently;
with large leaves the result is the same on every computer.

**Expected output:**

```
[5, np.float64(0.8)]
```
