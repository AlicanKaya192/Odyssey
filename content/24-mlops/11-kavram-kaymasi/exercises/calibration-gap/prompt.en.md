Write the function `calibration_gap(probabilities, labels)` that does the lesson's calibration test:

- `probabilities`: the churn probabilities the model gave.
- `labels`: the outcomes that happened (`1` churned, `0` stayed).
- Subtract the mean of the labels from the mean of the probabilities, round to three digits.

A positive result shows the model expects too much churn.

**Expected output:**

```
0.067
0.0
-0.4
```
