`neutral_scores(class_weight)` should train a logistic regression with the given
`class_weight` (`None` or `"balanced"`) and return the **neutral** class's
`[precision, recall]` on the test data with 3 places. Compute precision and
recall yourself (without `sklearn.metrics`).

**Expected output:**

```
plain [0.778, 0.681]
balanced [0.652, 0.806]
```
