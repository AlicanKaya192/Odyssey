Write the function `add_months(text, n)`: add `n` months to a date in the
format `"2026-01-31"` (`n` can be negative) and return the result as text in
the same format. If the day does not exist in the new month, fall back to the
last day of the month (`calendar.monthrange(year, month)[1]`).

**Expected output:**

```
2026-02-28
2027-02-15
2026-02-28
```
