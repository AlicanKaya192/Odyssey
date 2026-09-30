`energy_hourly.csv` holds hourly load (MW). Take two separate daily
summaries from the same series: the total energy used and the day's peak
load.

**What to do:**

1. Read the file with a date index; take the `load_mw` column into a series
   called `load`.
2. Compute the daily total (`sum`) and the daily maximum (`max`).
3. Print the number of days.
4. Print the day with the most energy used (`"%Y-%m-%d"`) and that day's
   total (one decimal) on one line.
5. Print the day with the highest peak load and that peak value on one line.
6. Print the mean daily total of weekdays and of weekend days, rounded to
   whole numbers, on one line.

**Expected output:**

```
61
2024-03-04 22841.7
2024-03-07 1282.0
22383 19256
```

The day with the most energy used and the day with the highest peak need not
be the same: one looks at the whole day's total, the other at a single
hour.
