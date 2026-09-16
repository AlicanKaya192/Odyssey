You will show a year of monthly sales as a **line chart**.

The data is in `sales.csv`:

```text
month,sales
Jan,120
Feb,135
Mar,128
Apr,150
May,162
Jun,158
...
```

**What to do:**

1. Write the imports and read the file.
2. Draw a line chart with months along x and sales along y; mark the points
   with `marker="o"`.
3. Set the title to `Monthly sales` and the y axis, **with its unit**, to
   `Sales (thousands)`.
4. Save the chart as **`chart.png`**.
5. Print, in order: the number of lines, the month with the highest sales,
   the difference between the end and the start of the year, and the y
   label.

**Expected output:**

```
1
Dec
110
Sales (thousands)
```

Once you run it, your chart appears in the **results panel**.

**Two things to take away:**

- **Bars compare categories; a line shows how something changes.** The
  chart shows a rising trend over the year with small dips along the way —
  much harder to see in the table.
- **The y label carries a unit.** With just `Sales`, the reader would have
  to guess between items, lira or thousands of lira.

To find the best month, `idxmax()` gives you the row's **index**; you take
the month's name from that row with `loc`.
