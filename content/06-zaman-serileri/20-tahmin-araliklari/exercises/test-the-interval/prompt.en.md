Does the interval the model calls "95%" really hold 95%? Measure it on the
rig of Section 15: 13 origins, a 28-day horizon. (It takes a few seconds.)

`cuts` is ready in the starter code.

**What to do:**

1. At each cut: the training is `s.loc[:cut]`, the test the next 28 days. Fit
   `ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7))`, take
   `get_forecast(28)` and compute the 95% interval.
2. For each experiment keep whether the actual values are inside the interval
   (28 true/false values) and the mean width of the interval.
3. Print the overall coverage of all the experiments with three decimals.
4. Print the coverage experiment by experiment with two decimals as a list.
5. Print the cut days of the experiments whose coverage is below 0.8 as a
   `"%Y-%m-%d"` list.
6. With those experiments removed, print the coverage of the rest with three
   decimals and the mean interval width with one decimal on one line.

**Expected output:**

```
0.874
[0.0, 0.96, 1.0, 1.0, 0.96, 1.0, 1.0, 1.0, 0.93, 1.0, 1.0, 0.96, 0.54]
['2024-01-02', '2024-12-03']
0.984 68.5
```

The "95%" interval holds 87% across 13 experiments: too narrow. But the
problem is not everywhere: two experiments (the start and the end of the year)
collapse, and in the other eleven the coverage is close to perfect. An
interval measures the uncertainty the model knows about; the model does not
know the movement at the turn of the year, so neither does its interval. The
cure is not a wider interval but the missing information (the calendar
variables of Section 18).
