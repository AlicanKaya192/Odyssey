A sensor in Berlin records the temperature once an hour; the
timestamps are UTC (`2024-03-29T23:00:00Z`). The report, though, is wanted by
local day.

**What to do:**

1. Read `berlin_sensor.csv` and convert the `time_utc` column to dates.
2. Convert to local time with `dt.tz_convert("Europe/Berlin")` into a column
   called `local`.
3. Print how many records there are for each **local day**:
   `value_counts().sort_index()` on `local.dt.date`; one line per day as
   `date count`.
4. Print the **local** time of the row with the highest temperature as
   `"%Y-%m-%d %H:%M"` (`idxmax()`).

**Expected output:**

```
2024-03-30 24
2024-03-31 23
2024-04-01 24
2024-03-31 12:00
```

No hour is missing in UTC. 31 March having 23 rows comes from Berlin moving
its clocks one hour forward that night. A report of daily totals would show
that day lower than it was.
