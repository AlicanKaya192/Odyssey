`shift` and `diff` count **rows**, not days. In a series with missing
days that silently gives a wrong result.

**What to do:**

1. Read `sales_messy.csv`, sort it and add up the repeats
   (`sort_index().groupby(level=0).sum()`) → `fixed`.
2. Print the value of `fixed.diff()` for 18 July 2024.
3. Show which day that difference was taken against: print the date
   (`"%Y-%m-%d"`) of the row just before 18 July in `fixed`.
4. Put the series on the calendar with `asfreq("D")` and take `diff()` again;
   print the value for 18 July.
5. Print the number of `NaN` values in the two difference series on one line
   (`fixed.diff()` first, then the one on the calendar).

**Expected output:**

```
-59.0
2024-07-14
nan
1 14
```

The -59 in the first line reads like "the change since yesterday", but it is
against four days earlier. On the calendar that difference is honestly `nan`.
In the last line there are 14 `NaN` values instead of 1: the eight missing
days themselves, the first day after each gap, and the first day of the
series.
