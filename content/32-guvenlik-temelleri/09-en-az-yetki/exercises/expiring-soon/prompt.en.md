Every grant is a `[user, resource, end_date]` list; the date is in ISO
format (`"2026-11-05"`).

`expiring_soon(grants, today, days)` should return the grants that have
**not yet expired** (end date ≥ today) and will expire at most `days` days
later (end date ≤ today + `days`), as `"user:resource"` texts in
alphabetical order. `today` is ISO text too.

`date.fromisoformat` turns text into a date, `timedelta(days=n)` gives a
difference in days (both are in the `datetime` module).

**Expected output:**

```
['ada:prod-db', 'linus:logs']
```
