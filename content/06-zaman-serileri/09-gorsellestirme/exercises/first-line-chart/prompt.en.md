Plot three years of daily sales and save it as `chart.png`.

**What to do:**

1. Read `store_sales.csv` as a series `s` with a date index.
2. Open a canvas with `figsize=(10, 4)` and draw the series with a thin line:
   `ax.plot(s.index, s.values, linewidth=0.8)`.
3. Set the title to `Daily sales` and the vertical axis label to `Units`.
4. Save the chart as `chart.png`.
5. Print the number of lines (`len(ax.lines)`), the title and the vertical
   axis label, one per line.
6. Print the width and height of the canvas on one line
   (`fig.get_size_inches()`).

**Expected output:**

```
1
Daily sales
Units
10.0 4.0
```

The chart will appear in the **Output** tab on the left. Look for the rising
trend, the peak at the end of each year and the thick band made by the weekly
zigzag.
