Repair the three outlier days (14 March, 20 June, 8 October): treat them
as missing and fill them with the average of a week before and a week after.
Keep the original data and flag the days you touched.

**What to do:**

1. Take `clean = visits.astype(float).copy()` and set the three days to `NaN`.
2. Fill the gaps with the average of a week before and a week after
   (`pd.concat([clean.shift(7), clean.shift(-7)], axis=1).mean(axis=1)`).
3. Print the new values of the three days as a list.
4. Build a table: `visits` (original), `clean` (repaired) and `repaired`
   (`True` on the days touched). Print the number of rows and the total of
   `repaired` on one line.
5. Print the standard deviation before and after the repair, rounded to one
   decimal, on one line.
6. Print the mean of the Thursdays (`dayofweek == 3`) before and after the
   repair, rounded to one decimal, on one line.
7. Print the total effect of the campaigns: the sum, over the two campaign
   days, of the differences between the original and the repaired value (a
   whole number).

**Expected output:**

```
[4116.0, 4120.5, 5226.5]
366 3
914.2 805.6
4621.3 4423.5
10285
```

The number of rows did not change: no day was deleted, only three values
changed. The standard deviation fell by 108 units and the Thursday mean by
200: the weekly pattern is no longer distorted by two campaigns. Because you
kept the original column you could answer the last question too: the two
campaigns brought about 10 thousand extra visits.
