Forecast "tomorrow" for every day of 2024 with five baselines and draw up
the scoreboard. Each forecast must use only data **from before that day**.

**What to do:**

1. Build five one-step forecasts over the whole series (in a dictionary, in
   this order):
   - `"mean so far"`: the mean of all the past up to that day
     (`s.shift(1).expanding().mean()`)
   - `"mean of 7"`: the mean of the last 7 days
   - `"naive"`: yesterday's value
   - `"seasonal naive"`: the same day last week
   - `"mean of 4 weeks"`: the mean of the same weekday in the last four weeks
     (`s.shift(7)`, `s.shift(14)`, `s.shift(21)`, `s.shift(28)`)
2. For each print the mean absolute error and the bias over 2024 as
   `name MAE bias`, with two decimals, one per line.
3. Print the skill of the best method over naive (`1 - MAE / MAE_naive`),
   rounded to two decimals.
4. **A leakage experiment:** what would the MAE be if you built "the mean of
   four weeks" wrongly and included today
   (`(s + s.shift(7) + s.shift(14) + s.shift(21)) / 4`)? Print it with two
   decimals.

**Expected output:**

```
mean so far 52.48 43.49
mean of 7 42.74 0.22
naive 41.1 -0.16
seasonal naive 13.87 0.92
mean of 4 weeks 13.89 2.03
0.66
9.86
```

The two methods that use the weekly pattern are far ahead and very close to
each other. The bias is close to zero for four of them; only the mean of all
the past is systematically low (the series is growing and the early years pull
the mean down). The last line shows what leakage looks like: the best result
on the board, but a fake one. The forecast sees its own target inside the
average; in reality you could not make it without knowing that day. **When you
see a result that is too good, look for leakage first.**
