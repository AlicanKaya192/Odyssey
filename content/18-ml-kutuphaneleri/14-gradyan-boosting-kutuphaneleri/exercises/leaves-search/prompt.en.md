`leaves_search(options)` should search `num_leaves` for
`LGBMClassifier(n_estimators=100, random_state=0, verbose=-1)` with
`GridSearchCV(..., cv=3)` on the training data and return
`[best_num_leaves, best_score]` (the score with 3 places).

**Expected output:**

```
[63, 0.911]
```
