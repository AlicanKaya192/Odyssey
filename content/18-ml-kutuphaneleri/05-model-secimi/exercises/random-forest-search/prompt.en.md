`random_forest_search(n_iter)` should run
`RandomizedSearchCV(RandomForestClassifier(random_state=0), space, n_iter=n_iter,
cv=3, random_state=0)` on the training data. The space: `"n_estimators":
randint(10, 60)`, `"max_depth": randint(2, 8)`. Return `[best_max_depth,
best_score]` (depth an `int`, score with 3 places).

**Expected output:**

```
[7, np.float64(0.84)]
```
