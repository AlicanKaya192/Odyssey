Rows (each with `"churned"` and the slice's column) and the model's predictions are given in the same order. Write the function `slice_accuracy(rows, predictions, column)`:

- Group the rows by the value of the `column` column.
- In each group, round the share of rows where the prediction equals `"churned"` to three digits.
- Return `[[value, accuracy], ...]`, with the values **sorted**.

**Expected output:**

```
basic 0.667
pro 0.667
```
