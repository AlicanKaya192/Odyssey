`dates` are backups with ISO dates, `today` is today's ISO date.
`gfs_keep(dates, today)` should return the dates of the backups to keep,
from earliest to latest. A backup is kept if:

- it is less than 7 days old (age `< 7`),
- it is a Sunday (`weekday() == 6`) and less than 28 days old,
- it is the first day of a month.

**Expected output:**

```
11
2026-10-01
2026-10-11
2026-10-18
2026-10-25
2026-10-26
```
