`f1_averages(c)` trains `LogisticRegression(C=c)` on the training data and predicts
the test. Return (all with 3 places):

- `"per_class"`: each class's F1 (a list)
- `"macro"`: the macro average
- `"weighted"`: the weighted average

**Expected output:**

```
[0.841, 0.392, 0.125]
0.453 0.68
```
