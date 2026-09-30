`machine_log.csv` is the temperature sensor of a machine (`time`,
`temp_c`). Readings arrive at irregular intervals, and on the night of 7 May
the sensor goes quiet for hours. Put the data on a 10-minute grid; fill the
short gaps and do not touch the fault.

**What to do:**

1. Read the file with a date index and turn the `temp_c` column into
   10-minute means: `r = x.resample("10min").mean()`.
2. Print the length of `r` and its number of `NaN` values on one line.
3. Find the lengths of the gaps (the `(missing != missing.shift()).cumsum()`
   counter). Print the **number** of gaps, the length of the longest gap, and
   the total number of cells in gaps of 3 cells or shorter, on one line.
4. Fill linearly only the gaps of 3 cells or shorter: for every row find the
   length of the gap it is in with `missing.groupby(run_id).transform("sum")`,
   build the mask `short = missing & (run_length <= 3)` and write
   `result = r.where(~short, r.interpolate())`.
5. Print the number of `NaN` values left in `result`.
6. For comparison print the number of `NaN` values left after
   `r.interpolate(limit=3)`.

**Expected output:**

```
432 54
22 33 21
33
30
```

All the short gaps were filled and the 33 cells of the fault stayed as they
were. `interpolate(limit=3)`, on the other hand, filled the first three cells
of the fault as well: 30 empty cells instead of 33. `limit` does not mean
"short gaps", it means "at most three from each gap".
