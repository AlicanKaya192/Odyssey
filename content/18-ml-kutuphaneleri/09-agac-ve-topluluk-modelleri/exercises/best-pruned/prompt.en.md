`best_pruned(folds)` should take the `ccp_alphas` candidates from the unlimited
tree's `cost_complexity_pruning_path`, choose the best with
`GridSearchCV(..., cv=folds)` and return `[alpha, leaf_count, test_score]`
(alpha with 4 places, score with 3; trees with `random_state=0`). The starter
code does not prune.

**Expected output:**

```
[0.0062, 12, 0.9]
[0.0088, 9, 0.867]
```
