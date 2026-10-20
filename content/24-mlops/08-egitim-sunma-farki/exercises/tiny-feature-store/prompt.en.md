Write the lesson's `FeatureStore` class and close two gaps:

- `write(customer, day, values)`: adds `[day, values]` to the customer's history (dates are written in increasing order).
- `offline(customer, day)`: the last values written on or before that date; `None` if there are none or the customer doesn't exist.
- `online(customer)`: the customer's most recently written values; `None` if the customer doesn't exist.

**Expected output:**

```
training C7: {'support_calls': 1}
training C9: None
serving C7: {'support_calls': 4}
serving C5: None
```
