Test seasonal naive, Holt–Winters and ARIMA side by side on the rig of
Section 15: 13 origins, a 28-day horizon.

In the starter code `snaive`, `hw` and `backtest(forecast)` are ready.
(This exercise takes a few seconds because it fits an ARIMA 13 times.)

**What to do:**

1. Write the function `arima(train, h)`: it fits the `(0, 1, 1)(0, 1, 1, 7)`
   model on `train` and returns the `h`-day forecast as a numpy array.
2. Put the three methods through `backtest`. For each print the mean MAE and
   the worst experiment with two decimals as `name mean worst`, one per line
   (names: `snaive`, `hw`, `arima`).
3. ARIMA against seasonal naive: print the mean of the `snaive − arima`
   difference (two decimals) and the number of experiments ARIMA wins on one
   line.
4. ARIMA against Holt–Winters: print the mean and the standard deviation
   (`ddof=1`, two decimals) of the `hw − arima` difference and the number of
   experiments ARIMA wins on one line.

**Expected output:**

```
snaive 17.95 41.29
hw 15.91 38.57
arima 15.94 52.2
2.02 11
-0.02 5.13 9
```

ARIMA beats seasonal naive in 11 of the 13 experiments. Against Holt–Winters
it is ahead in 9 experiments and yet the mean difference is zero: it wins by a
little where it wins and loses by a lot where it loses. A tie. Two different models arrive at the same place; that is all the
information that can be drawn from the past of the series. In the worst
experiment ARIMA is markedly behind: the same mean, a bigger risk.
