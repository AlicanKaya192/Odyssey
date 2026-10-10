`beats_baseline(weight)` should generate imbalanced data with
`make_classification(n_samples=1000, n_features=5, weights=[weight],
random_state=3)`, split it with `train_test_split(..., random_state=3)` and
train two models: `DummyClassifier(strategy="most_frequent")` and
`LogisticRegression()`. Return:

- `"baseline"`, `"model"`: the test accuracies, 3 places
- `"better"`: whether the model's accuracy is **at least 0.02** above the
  baseline

**Expected output:**

```
0.892 0.94
True
```
