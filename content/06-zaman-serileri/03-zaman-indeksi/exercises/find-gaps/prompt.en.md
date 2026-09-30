After resolving the repeats 358 rows remain; 2024 has 366 days. Which
days are not there?

**What to do:**

1. Read the file, sort it and add up the repeats (as in the previous
   exercise).
2. Produce the full daily calendar from the first date to the last
   (`pd.date_range`, `freq="D"`) and find the days that are not in the series
   (`difference`).
3. Print the number of missing days and the missing dates (`"%Y-%m-%d"`, as
   a list).
4. Print the **longest** gap between two consecutive rows in days:
   `fixed.index.to_series().diff().max().days`.
5. Put the series on the full calendar with `asfreq("D")`; print the number
   of rows and the number of `NaN` values on one line.

**Expected output:**

```
8
['2024-02-10', '2024-02-11', '2024-04-23', '2024-07-15', '2024-07-16', '2024-07-17', '2024-10-29', '2024-12-25']
4
366 8
```

The longest gap is 4 days: the row after 14 July is 18 July. Before `asfreq`,
"the previous row" in this series was not always yesterday; afterwards there
is a row for every day and the gaps show as `NaN`.
