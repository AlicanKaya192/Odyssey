Write seasonal naive as a function that works at any frequency and any
horizon.

**What to do:**

1. Write the function `seasonal_naive(train, h, m)`:
   - Take the last `m` values (`train.iloc[-m:].to_numpy()`).
   - Produce the values `last[i % m]` for `h` steps.
   - Let the index be the `h` dates **after** the last training date:
     `pd.date_range(train.index[-1], periods=h + 1, freq=train.index.freq)[1:]`.
   - Return a series.
2. Call it on the daily sales (`s`, up to 3 December 2024) with `m=7`,
   `h=10`. Print the values of the returned series as a list.
3. Print the first and the last date of the same forecast on one line.
4. Call it on the monthly passengers (`p`, up to the end of 2023) with
   `m=12`, `h=12`. Print the values as a list.
5. Compare the passenger forecast with the actual values of 2024: print the
   mean absolute error and the bias (the mean of the errors) with two decimals
   on one line.

**Expected output:**

```
[297, 297, 336, 432, 393, 269, 290, 297, 297, 336]
2024-12-04 2024-12-13
[293, 279, 321, 323, 344, 395, 425, 448, 369, 350, 303, 345]
40.42 40.42
```

With a horizon of 10 the last three values take the first three days of the
week again: `i % 7` does not need the horizon to be a multiple of the season.
For the passenger forecast the MAE and the bias are the same number: the
forecast was low in all twelve months, because the series is growing and the
copy runs a year behind.
