`stack_months(months)` takes a dictionary of month name → `[city, sales]`
rows. It should make each month a DataFrame (`columns=["city", "sales"]`) and
combine them with a **single** `pd.concat(..., keys=names)` call. Return:

- `"rows"`: the total row count
- `"index"`: the index of the table combined with `ignore_index=True` (a list)
- `"totals"`: total sales per month, in the months' **given order**
  (`groupby(level=0, sort=False)`)

**Expected output:**

```
6 [0, 1, 2, 3, 4, 5]
{'jan': 200, 'feb': 50, 'mar': 170}
```
