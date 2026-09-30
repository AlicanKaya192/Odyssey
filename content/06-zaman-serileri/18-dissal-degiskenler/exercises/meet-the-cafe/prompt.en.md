`cafe_daily.csv` holds three years of daily sales of a café in a business
district. Columns: `date`, `sales`, `temp_c` (the day's mean temperature),
`promo` (a campaign day: 1), `holiday` (a public holiday: 1).

**What to do:**

1. Read the file with a date index and apply `asfreq("D")`. Print the shape of
   the table.
2. Print the number of campaign days and of holidays on one line.
3. Print which weekdays the campaign days fall on: the sorted list of distinct
   `dayofweek` values of the rows where `promo == 1`.
4. Print the mean sales of three groups with one decimal on one line: campaign
   days, holidays, other days (both 0).
5. Print the rough campaign effect: the mean of the campaign days minus the
   mean of the days where `promo == 0` (one decimal).
6. Print the correlation between sales and temperature with two decimals.

**Expected output:**

```
(1096, 4)
84 41
[3, 4, 5]
284.0 166.7 229.6
57.0
0.62
```

Campaigns always fall on Thursday, Friday and Saturday (3, 4, 5). That is why
the "rough effect" on line 5 is not reliable: it compares campaign days with
all days, whereas sales on those three days differ anyway. The correlation
with temperature is high too: a café that is busy in summer.
