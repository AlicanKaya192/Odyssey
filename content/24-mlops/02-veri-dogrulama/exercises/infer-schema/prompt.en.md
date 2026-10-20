Write the function `infer_schema(rows, numeric, categorical, margin)` that infers a schema from trusted reference data:

- For every column in the `numeric` list, find the smallest (`low`) and largest (`high`) value. Leave a **margin** of `margin * (high - low)` on both ends of the range. Values in these columns cannot be negative: if the lower limit goes below 0, write 0 (`max(0.0, ...)`). Round both limits to two digits: `{"min": ..., "max": ...}`.
- For every column in the `categorical` list, the **sorted** list of the values seen: `{"allowed": [...]}`.
- Add the numeric columns first, then the categorical ones, in the given order.

**Expected output:**

```
monthly_fee {'min': 1.1, 'max': 63.41}
usage_hours {'min': 0.0, 'max': 74.09}
plan {'allowed': ['basic', 'pro']}
```
