`train_test_gap(depth)` should run `cross_validate(..., cv=5, scoring=["accuracy",
"f1"], return_train_score=True)` for `DecisionTreeClassifier(max_depth=depth,
random_state=0)` and return with 3 places:

- `"train"`: the mean training accuracy
- `"test"`: the mean test accuracy
- `"f1"`: the mean test F1

**Expected output:**

```
{'train': 1.0, 'test': 0.78, 'f1': 0.488}
{'train': 0.87, 'test': 0.81, 'f1': 0.429}
```
