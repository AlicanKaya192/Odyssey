`tuned_threshold(fn_cost)` should train `TunedThresholdClassifierCV(LogisticRegression(),
scoring=scorer, cv=5)` on the training data with the `cost` measure
(`fn_cost` is given to `make_scorer` as an extra setting) and return
`[threshold, test_cost]`: the threshold `best_threshold_` with 3 places, the
cost from the tuned model's test predictions.

**Expected output:**

```
[0.455, 4]
[0.293, 43]
```
