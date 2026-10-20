So that training and serving use the same order, let the feature vector be built from a **definition list**. Write the function `vector(row, spec)`:

- `spec` is the list of column names; the vector is built in this order.
- If the name is `"is_pro"`, the value comes from the row's `"plan"`: `1` if `"pro"`, otherwise `0`.
- For the other names, the row's value as it is.

**Expected output:**

```
[2, 45.0, 6, 5.0, 1]
[0, 2]
```
