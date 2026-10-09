## Classification measures

| Measure | Formula | Question | scikit-learn |
|---|---|---|---|
| Accuracy | `(TP + TN) / n` | how many out of how many are right? | `accuracy_score` |
| Precision | `TP / (TP + FP)` | how many of my "positive"s are right? | `precision_score` |
| Recall | `TP / (TP + FN)` | how many positives did I find? | `recall_score` |
| Specificity | `TN / (TN + FP)` | how many negatives did I leave alone correctly? | — |
| F1 | `2PR / (P + R)` | precision and recall together | `f1_score` |
| ROC AUC | the area under the curve | does a positive score above a negative? | `roc_auc_score` |
| Average precision | weighted sum of precisions | finding positives when imbalanced | `average_precision_score` |

## Regression measures (section 3)

MSE, RMSE (in the target's unit), MAE (robust to outliers), R² (relative to the
baseline).

## Which one when?

- If the classes are balanced and the errors cost the same, accuracy is enough.
- If a false alarm is costly (a spam filter deleting real mail), precision.
- If missing is costly (disease, fraud), recall.
- For threshold-free ranking quality, ROC AUC; if positives are very rare,
  average precision.

## Common mistakes

- Reporting accuracy on imbalanced data without the baseline (the most
  frequent class) next to it.
- Computing AUC from 0/1 predictions instead of scores: the curve collapses to
  a single point.
- Giving precision and recall without stating the threshold: both depend on
  it.
