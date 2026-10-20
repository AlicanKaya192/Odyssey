Write the function `mean_shift(reference, rows, column)`. Measure how many **standard deviations** the mean of one column of the new batch moved from the reference data:

- Skip `None` values in both lists.
- `|new mean - reference mean| / reference standard deviation`.
- Use `statistics.mean` for the mean and `statistics.pstdev` for the standard deviation.
- Round the result to two digits.

The code compares month 3's customers with month 0's; the customers change as the months go by.

**Expected output:**

```
tenure 0.03 ok
monthly_fee 0.27 ok
support_calls 0.53 CHECK
usage_hours 0.54 CHECK
```
