Write the function `training_window(rows, current_month, size)` that picks the last window:

- `rows`: dictionaries, each with a `"month"` key.
- Return the rows whose month is not later than `current_month` and falls within the last `size` months: `current_month - size < month <= current_month`.
- Keep the rows' order. If `size` is `0`, the list is empty.

**Expected output:**

```
3
[2, 3]
[]
```
