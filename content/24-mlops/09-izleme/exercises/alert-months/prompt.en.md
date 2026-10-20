Write the lesson's `alert_months(values, reference, limit, patience)` function. `values` is a monthly measure (starting from month 0):

- A month counts as crossing the threshold if its value is **more** than `limit` away from `reference`.
- Count how many months in a row it was crossed; the counter resets in a month that isn't crossed.
- Add every month where the counter reaches or passes `patience` to the list.

**Expected output:**

```
[3, 4, 5, 6, 7]
[4, 5, 6, 7]
[]
```
