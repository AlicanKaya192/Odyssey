`times` are backup times sorted from earliest to latest (ISO text).
`worst_gap_hours(times)` should return the longest gap between two
consecutive backups in hours, rounded to 1 place. With fewer than two
backups, `0.0`.

**Expected output:**

```
12.0
0.0
```
