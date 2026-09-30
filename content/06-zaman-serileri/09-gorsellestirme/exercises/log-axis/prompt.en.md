`passengers_monthly.csv` holds monthly passenger numbers (thousands),
2013–2024. The series grows, and its seasonal waves grow with it. Draw the
same series with two axes side by side.

**What to do:**

1. Read the file with `index_col="month"` and `parse_dates=True`; take the
   `passengers` column into a series called `p`.
2. Find the lowest and the highest month of each year
   (`p.groupby(p.index.year).agg(["min", "max"])`).
3. Print the summer–winter **difference** (`max - min`) for 2013 and 2024 on
   one line.
4. Print the summer–winter **ratio** (`max / min`) for the same two years,
   rounded to two decimals, on one line.
5. Open two panels side by side (`plt.subplots(1, 2, figsize=(11, 4))`),
   draw the series on both, make the vertical axis of the second one
   logarithmic (`set_yscale("log")`) and save as `chart.png`.
6. Print the vertical axis scale of the two panels as a list
   (`ax.get_yscale()`).

**Expected output:**

```
61 183
1.6 1.6
['linear', 'log']
```

The difference tripled; the ratio did not change at all: the seasonality is
proportional to the level of the series. On the linear panel the waves grow
over the years; on the logarithmic panel they are all the same height and the
line is almost straight.
