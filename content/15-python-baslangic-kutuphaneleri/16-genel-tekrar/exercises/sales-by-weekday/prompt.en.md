There is a `sales.csv` next to your file: the columns are `date` (like
`2026-03-16`) and `amount`. Write the function `sales_by_weekday(path)`: read
it with `csv.DictReader`, find each row's day with
`date.fromisoformat(...).weekday()`, take its name from the `DAYS` list, and
return the totals per day (`round(..., 2)`) as a dictionary.

**Expected output:**

```
Mon 160.75
Tue 80.0
Sat 200.0
Sun 15.75
```
