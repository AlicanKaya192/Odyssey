Show the two patterns of hourly electricity load (day of the week and
hour of the day) on a single heatmap.

**What to do:**

1. Read `energy_hourly.csv` with a date index; take the `load_mw` column into
   a series called `load`.
2. Build the day × hour table of means:
   `load.groupby([load.index.dayofweek, load.index.hour]).mean().unstack()`.
3. Print the table's shape.
4. Draw the heatmap (`ax.imshow(grid.values, aspect="auto")`), add the colour
   bar (`fig.colorbar(image)`) and save as `chart.png`.
5. Print, on one line, which day (0–6) and hour the highest mean is at, and
   its value (a whole number). Hint: `grid.stack().idxmax()` gives a
   (day, hour) pair.
6. Print the same for the lowest mean.
7. Print the means at 13:00 for Monday (0) and Sunday (6), rounded to whole
   numbers, on one line.

**Expected output:**

```
(7, 24)
3 13 1238
6 5 667
1222 1068
```

The peak is at midday on a weekday, the low before dawn on Sunday. At the
same hour Sunday is clearly below Monday: the day-of-week pattern holds at
every hour of the day.
