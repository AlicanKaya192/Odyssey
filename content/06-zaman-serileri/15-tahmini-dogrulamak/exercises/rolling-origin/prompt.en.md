Test seasonal naive from 13 different origins through 2024 and save the
results as a bar chart. `snaive(train, h)` is ready in the starter code.

**What to do:**

1. Run 13 experiments. The cut day of experiment `i` is
   `pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i)`. Training goes up
   to the cut (`s.loc[:cut]`), the test is the next 28 days
   (`s.loc[cut + pd.Timedelta(days=1):].iloc[:28]`).
2. In each experiment compute the MAE and the bias; keep them with the cut
   day.
3. Print the number of experiments and the mean, standard deviation
   (`ddof=1`), minimum and maximum of the MAEs, with two decimals, on one
   line.
4. Print the cut days of the two worst experiments as a `"%Y-%m-%d"` list (in
   date order).
5. Print the MAE of the experiment cut on 5 November 2024 and the mean bias of
   all the experiments, with two decimals, on one line.
6. Draw a bar chart of the 13 MAEs and save it as `chart.png`.

**Expected output:**

```
13 17.95 10.94 9.39 41.29
['2024-01-02', '2024-12-03']
11.64 1.68
```

The typical error is around 18, but it swings between 9 and 41 depending on
the period. The two worst experiments are the start and the end of the year.
The 11.64 you measured in Section 14 is just one of these 13 experiments, and
one of the good ones. Instead of a single number you now have a
distribution.
