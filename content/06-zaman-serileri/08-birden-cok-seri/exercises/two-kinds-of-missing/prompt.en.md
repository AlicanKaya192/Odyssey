In the wide table two shops have `NaN` values, and they mean two
different things: C is **closed** on Sundays, D is **absent** before 1 May.

**What to do:**

1. Read `stores.csv` and turn it into the wide shape.
2. Show which day of the week C's `NaN` days are: print the distinct
   `day_name()` values of those dates as a list.
3. For C print two means rounded to one decimal on one line: skipping the
   `NaN` values, and with `fillna(0)`.
4. For D print the same two means on one line.
5. Compute the daily total of the four shops (`wide.sum(axis=1)`) and print
   its values for 30 April and 1 May 2024 on one line.
6. Compute the total of only the three shops that exist all year (A, B, C)
   and print the values for the same two days on one line.

**Expected output:**

```
['Sunday']
248.5 213.2
170.9 114.4
626.0 775.0
626.0 669.0
```

Both of C's means are meaningful: one per open day, the other per calendar
day. D's second mean is wrong: it counts four months that did not exist as
zero sales. The four-shop total jumps on 1 May because a new series entered
it; the three-shop total has no such break.
