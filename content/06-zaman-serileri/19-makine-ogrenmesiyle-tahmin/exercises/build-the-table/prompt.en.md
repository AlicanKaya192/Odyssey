Turn the daily sales series into a feature table.

**What to do:**

1. Write the function `features(y)`; it returns a table indexed by `y.index`:
   - `lag1`, `lag2`, `lag7`, `lag14`: `y.shift(k)`
   - `mean7`: `y.shift(1).rolling(7).mean()`
   - `mean28`: `y.shift(1).rolling(28).mean()`
   - `dow`: the day of the week, `month`: the month
2. Add the target to the `features(s)` table as a column `y`
   (`.join(s.rename("y"))`) and apply `dropna()`. Print its shape and its
   first date on one line.
3. Print the column names as a list.
4. Check the row of 10 March 2024: print that day's `y`, `lag1`, `lag7` and
   `mean7` (the first three as whole numbers, `mean7` with one decimal) on one
   line.
5. Compute the same `mean7` by hand: the mean of the sales of 3–9 March 2024
   (one decimal).

**Expected output:**

```
(1068, 9) 2022-01-29
['lag1', 'lag2', 'lag7', 'lag14', 'mean7', 'mean28', 'dow', 'month', 'y']
311 384 319 283.7
283.7
```

The `mean7` on the last two lines is the same: the feature of 10 March covers
3–9 March; 10 March itself is **not** in it. That is exactly what `shift(1)`
ensures. The table is 28 rows shorter: the days for which there was not enough
past for `mean28`.
