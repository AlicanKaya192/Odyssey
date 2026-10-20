The lesson's `SCHEMA` and `check_row` are ready in `rules.py`. Write the function `gate(rows, schema, max_bad_share)`. This time, instead of raising an error, return a **dictionary**:

- Check every row with `check_row(row, schema)`; a row with problems counts as quarantined (`quarantined`), one without as sound (`good`).
- If the share of bad rows (`quarantined / len(rows)`) is **greater** than `max_bad_share`, the `"status"` value is `"rejected"`, otherwise `"accepted"`.
- If there are no rows, the empty batch is rejected: `{"status": "rejected", "good": 0, "quarantined": 0}`.
- The returned dictionary's keys: `"status"`, `"good"`, `"quarantined"`.

**Expected output:**

```
accepted 200 0
rejected 188 12
rejected 0 0
```
