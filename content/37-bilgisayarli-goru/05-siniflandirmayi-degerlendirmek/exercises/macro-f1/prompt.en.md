`macro_f1(y_true, y_pred, k)` should compute each class's F1 (from precision
and recall) by hand and return their mean rounded to 3 places. A precision,
recall or F1 with a zero denominator counts as `0.0`. The program prints the
result next to scikit-learn's `f1_score(..., average="macro")`.

**Expected output:**

```
0.633
0.633
```
