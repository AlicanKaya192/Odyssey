`best_c(options)` should search the `C` of the logistic regression in the pipeline
with `GridSearchCV` (AUC, the given `cv`) and return `[best_C, best_score]`
(score with 3 places). The starter code writes the grid key as `"C"`; in a
pipeline the setting's name is `step__setting`.

**Expected output:**

```
[0.1, 0.777]
```
