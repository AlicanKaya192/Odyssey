`results_rows(cs)` should run `GridSearchCV(LogisticRegression(), {"C": cs}, cv=5)` on
the training data and return a `[C, mean, spread]` row for each candidate
(`params`, `mean_test_score`, `std_test_score` from `cv_results_`; scores with
3 places).

**Expected output:**

```
[0.001, 0.733, 0.063]
[0.1, 0.831, 0.023]
[10.0, 0.822, 0.0]
```
