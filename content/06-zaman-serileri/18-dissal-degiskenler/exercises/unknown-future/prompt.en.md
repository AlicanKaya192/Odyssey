The campaign and holiday calendar is known in advance; the temperature is
not. Imagine you are standing on 31 October and forecast with three different
assumptions about November's temperature.

In the starter code `train`, `test`, `columns` and the fitted model `fit` are
ready.

**What to do:**

1. Build three future tables. In all three `promo` and `holiday` are the
   actual values of the test period (the calendar is known); only the `temp_c`
   column differs:
   - `"actual"`: the actual temperature in the test (cheating)
   - `"last"`: the temperature on the last training day, for all 28 days
   - `"normal"`: the seasonal normal: the mean temperature of that calendar
     day (`dayofyear`) in the training data
2. Print the **temperature** error of each assumption (the mean absolute
   difference from the actual test temperature, one decimal) as `name error`,
   one per line.
3. Forecast **sales** with each assumption and print the mean absolute error
   with two decimals as `name MAE`, one per line.
4. Print how much better the "actual temperature" result is than the best of
   the honest ones, with two decimals (the best honest MAE minus the cheating
   MAE).

**Expected output:**

```
actual 0.0
last 1.5
normal 2.2
actual 11.07
last 12.5
normal 15.59
1.43
```

The result with the actual temperature is a ceiling: on 31 October those
measurements did not exist. Over these 28 days "the last value" came out
better than the seasonal normal, because November's temperature happened to
stay around the value at the end of October. In the 13-experiment test of the
lesson the order is reversed: the seasonal normal 15.0, the last value 17.7. A
single period misleads; which proxy is good is decided with a rolling origin
too.
