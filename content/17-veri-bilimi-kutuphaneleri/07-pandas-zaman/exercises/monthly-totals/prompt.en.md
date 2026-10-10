`monthly_totals(dates, amounts)` should build a series with a date index
(`pd.Series(amounts, index=pd.to_datetime(dates))`), total it by month with
`resample("ME").sum()` and return `{"YYYY-MM": total}`. A month in between
with no records must appear too, with 0 (resample does this itself). For the
keys, `index.strftime("%Y-%m")`. **Do not write a loop.**

**Expected output:**

```
('2026-01', 150)
('2026-02', 0)
('2026-03', 70)
```
