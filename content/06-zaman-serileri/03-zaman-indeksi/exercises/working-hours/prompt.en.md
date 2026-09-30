`energy_hourly.csv` holds a region's hourly electricity load (MW). How
much does the load depend on the time of day?

**What to do:**

1. Read the file with `index_col="timestamp"` and `parse_dates=True`; take
   the `load_mw` column into a series called `load`.
2. Print how many records there are on 15 March 2024.
3. Print the daytime (`between_time("08:00", "18:00")`) and night
   (`between_time("22:00", "06:00")`) means, rounded to one decimal, on one
   line.
4. Print the ratio of the daytime mean to the night mean, rounded to two
   decimals.
5. Print the mean load at 18:00 of every day (`at_time`), rounded to one
   decimal.

**Expected output:**

```
24
1038.1 768.4
1.35
871.2
```

Daytime load is a third higher than the night's. This is a seasonality of 24
steps that repeats every day: the strongest clue when forecasting hourly
data.
