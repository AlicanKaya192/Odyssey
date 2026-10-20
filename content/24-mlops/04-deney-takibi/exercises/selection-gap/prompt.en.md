Turn the lesson's winner's curse measurement into a function. `scores` is a list: every element is one model's `[validation, test]` scores. `selection_gap(scores)` should return a dictionary:

- Find the model with the highest validation score (the earlier one on a tie).
- `"val_lead"`: that model's validation score minus the mean of all validation scores.
- `"test_lead"`: the **same** model's test score minus the mean of all test scores.
- Round both to three digits.

**Expected output:**

```
validation lead: 0.022
test lead: 0.005
```
