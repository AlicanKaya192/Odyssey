Test the model with external variables on a rolling origin. In every
experiment build the future table **only from what is known at that moment**:
the calendar is real, the temperature is the seasonal normal.

In the starter code `cuts` (6 cuts 56 days apart) and `plain(train, test)`
(the forecast of the model without external variables) are ready. (It takes a
few seconds.)

**What to do:**

1. Write the function `with_exog(train, test)`:
   - `columns = ["promo", "holiday", "temp_c"]`
   - Fit the model on `train` (`order=(1, 0, 0)`,
     `seasonal_order=(0, 1, 1, 7)`, `exog=train[columns]`).
   - The future table: `test[columns].copy()`; replace the `temp_c` column
     with the seasonal normal computed from the **training** data
     (`train["temp_c"].groupby(train.index.dayofyear).mean()`; for a missing
     day `.get(day, normal.mean())`).
   - Return the 28-day forecast as a numpy array.
2. Run the two methods over the 6 experiments: at each cut the training is
   `c.loc[:cut]` and the test the next 28 days. Keep the MAE of each
   experiment.
3. For each method print the mean MAE and the worst experiment with two
   decimals as `name mean worst`, one per line (names: `plain`, `exog`).
4. Print the number of experiments the model with external variables wins and
   its skill (`1 - mean_exog / mean_plain`, two decimals) on one line.

**Expected output:**

```
plain 28.23 44.88
exog 14.81 16.97
6 0.48
```

The model built from what is known at forecast time halves the error and is
ahead in 6 of 6 experiments. The worst experiment improves markedly too. You
recomputed the seasonal normal from `train` in every experiment: had you
computed it once from all the data, the temperatures of the test period would
have leaked into the normal.
