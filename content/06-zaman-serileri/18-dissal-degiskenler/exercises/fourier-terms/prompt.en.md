Go back to the daily shop sales of Section 17. The worst experiment of
ARIMA was at the end of the year. Give the model two pieces of calendar
information: the yearly wave (Fourier) and the December climb.

In the starter code `train` (up to 3 December 2024) and `test` (the next
28 days) are ready.

**What to do:**

1. Write the function `fourier(index, K)`:
   `day = index.dayofyear.to_numpy()`; for each `k = 1..K` the columns
   `sin{{k}}` and `cos{{k}}` (`np.sin(2 * np.pi * k * day / 365.25)` and its
   cosine); it returns a table indexed by `index`.
2. Write the function `calendar(index)`: to the table `fourier(index, 2)` it
   adds a `dec` column: `index.day / 31` on December days and 0 on other days.
3. Print the shape and the column names of `calendar(train.index)` on one
   line.
4. Fit two models (both `order=(0, 1, 1)`, `seasonal_order=(0, 1, 1, 7)`): one
   without external variables, the other with `exog=calendar(train.index)`.
5. Take the 28-day forecast of the two models (give the second
   `exog=calendar(test.index)`). Print their mean absolute errors and biases
   with two decimals as `name MAE bias`, one per line (names: `plain`,
   `calendar`).
6. Print the coefficient of the `dec` column with one decimal.

**Expected output:**

```
(1068, 5) ['sin1', 'cos1', 'sin2', 'cos2', 'dec']
plain 31.34 31.07
calendar 14.35 9.5
49.4
```

The plain model does not know about the December climb: it is low on all
28 days (the bias is almost as large as the MAE). With calendar information
the error falls by more than half and the bias drops from 31 to 9.5. The
`dec` coefficient tells by how many units sales rise towards the end of the
month. No forecast was needed for the future of the Fourier columns: the day
of the year is known from the calendar.
