## Common scoring names

| Name | Measure |
|---|---|
| `"accuracy"`, `"balanced_accuracy"` | accuracy, mean of per-class recall |
| `"f1"`, `"precision"`, `"recall"` | two classes, positive class 1 |
| `"f1_macro"`, `"f1_weighted"`, `"recall_macro"` | multiclass averages |
| `"roc_auc"`, `"average_precision"` | ranking (with probabilities) |
| `"neg_log_loss"`, `"neg_brier_score"` | quality of the probabilities |
| `"neg_mean_absolute_error"`, `"neg_root_mean_squared_error"` | regression error |
| `"r2"`, `"neg_mean_absolute_percentage_error"` | regression |

## Kinds of average

| `average=` | What it does |
|---|---|
| `None` | each class's value separately |
| `"macro"` | plain mean; a small class counts equally |
| `"weighted"` | weighted by class size |
| `"micro"` | all predictions in one pool |
| `"binary"` (default for two classes) | only the `pos_label` class |

## make_scorer

| Code | Meaning |
|---|---|
| `make_scorer(f)` | `f(y_true, y_pred)`, larger is better |
| `make_scorer(f, greater_is_better=False)` | smaller is better; the scorer returns it negated |
| `make_scorer(f, response_method="predict_proba")` | `f` gets probabilities |
| `make_scorer(fbeta_score, beta=2)` | extra settings pass to `f` |
| `get_scorer("roc_auc")` | turns a name into a scorer object |

## Threshold

| Code | What it does |
|---|---|
| `TunedThresholdClassifierCV(m, scoring=scorer, cv=5)` | chooses the threshold on training data with cross-validation; `best_threshold_` |
| `FixedThresholdClassifier(m, threshold=0.2)` | fixes the threshold |
| `(model.predict_proba(X)[:, 1] >= t).astype(int)` | a threshold by hand |
