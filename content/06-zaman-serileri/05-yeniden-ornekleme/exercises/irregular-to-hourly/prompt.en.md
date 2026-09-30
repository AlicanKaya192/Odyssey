`machine_log.csv` holds a machine's temperature records. The sensor sent
them not at regular intervals but at random ones, and for a while not at all.

**What to do:**

1. Read the file with `index_col="time"` and `parse_dates=True`; take the
   `temp_c` column into a series called `temp`.
2. Print the longest gap between two consecutive records:
   `temp.index.to_series().diff().max()`.
3. Turn it into hourly means (`resample("h").mean()`); print the number of
   hours and the number of empty (`NaN`) hours on one line.
4. Print the empty hours as a list in `"%m-%d %H:%M"` form.
5. For 7 May 04:00 print the results of `resample("h").sum()` and
   `resample("h").mean()` on one line.
6. Fill the hourly series with `interpolate()` and print the value at 7 May
   05:00, rounded to two decimals.

**Expected output:**

```
0 days 05:42:44
72 4
['05-07 03:00', '05-07 04:00', '05-07 05:00', '05-07 06:00']
0.0 nan
57.64
```

The fifth line shows the trap: the sum of an hour with no records is 0.0, its
mean `nan`. The machine was not at zero degrees; there was no measurement.
The value in the last line is not a measurement either but a guess lying on
the straight line drawn between the two ends.
