`month_table(dates, stores, amounts)` should read the dates (`YYYY-MM-DD`),
turn them into months (`dt.to_period("M").astype(str)`) and build a month ×
store **total** table (`pivot_table(..., aggfunc="sum", fill_value=0)`).
Return:

- `"months"`: the months in the rows (a list)
- `"values"`: the table as a list of lists

**Do not write a loop.**

**Expected output:**

```
['2026-01', '2026-02', '2026-03']
[[100, 50], [70, 0], [0, 30]]
```
