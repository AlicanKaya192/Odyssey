Each item in `pairs` is `[start, end]`, ISO text (`"2026-10-03T08:00"`).
`mean_hours(pairs)` should return the mean of the durations in hours,
rounded to 1 place. If the list is empty, `0.0`. Hint:
`(end - start).total_seconds() / 3600`.

**Expected output:**

```
4.1
0.0
```
