Write the function `invalid_share(rows, limits)` for the validation step:

- `limits`: `{column: [low, high]}`.
- A row is invalid if one of the columns in `limits` is missing (`None` or absent) or out of range.
- Return the share of invalid rows, rounded to three digits.

**Expected output:**

```
0.75
0.0
```
