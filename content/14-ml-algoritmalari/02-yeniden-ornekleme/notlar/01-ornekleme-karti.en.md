## Which method when?

| Method | What it does | scikit-learn | When? |
|---|---|---|---|
| Train/test split | splits once | `train_test_split` | very large data, a quick first look |
| k-fold | `k` parts, each tested once | `KFold`, `cross_val_score` | the default in most cases |
| Stratified k-fold | keeps the class proportions | `StratifiedKFold` | classification, especially imbalanced classes |
| Leave-one-out | `k = n` | `LeaveOneOut` | very small data |
| Group k-fold | samples of the same group in the same fold | `GroupKFold` | several rows of the same patient, user |
| Time series split | training always before testing | `TimeSeriesSplit` | time-dependent data |
| Permutation test | shuffles the labels and measures again | `permutation_test_score` | does the result beat chance? |
| Bootstrap | samples with replacement | — (ALG 2 · 12) | a confidence interval |

## Common mistakes

- **Scaling first and splitting afterwards:** the mean has seen the test data
  too. In each fold, the scaler is `fit` only on that fold's training part (in
  scikit-learn a `Pipeline` does this by itself).
- **Spreading the rows of the same person on both sides:** the model memorises
  the person and the test result inflates. A grouped split is needed.
- **Shuffling a time series:** the model predicts the past while seeing the
  future.
- **Choosing a hyperparameter by looking at the test set:** the test set is
  then "seen"; the choice is made with cross-validation, the final measurement
  with a separate test set.
