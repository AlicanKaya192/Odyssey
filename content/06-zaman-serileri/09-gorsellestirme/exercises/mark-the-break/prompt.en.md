`web_traffic.csv` holds a site's daily visits. It contains two campaign
spikes, one outage and a lasting rise in level from 2 September. Put them on
the chart.

**What to do:**

1. Read the file with a date index; take the `visits` column into a series
   called `visits`.
2. Find the unusual days (the method from Section 07):
   `base = visits.shift(1).rolling(28)`,
   `z = (visits - base.mean()) / base.std()`, `unusual = z[z.abs() > 3]`.
3. Draw the series on a `figsize=(10, 4)` canvas.
4. Add a dashed vertical line for each unusual day
   (`ax.axvline(day, linestyle="--", color="gray")`).
5. Shade the stretch from 2 September 2024 to the end of the series
   (`ax.axvspan(..., alpha=0.15)`) and save as `chart.png`.
6. Print the marked days as a list in `"%m-%d"` form.
7. Print the number of lines on the chart (`len(ax.lines)`).
8. Print the median visits before and from 2 September, rounded to whole
   numbers, on one line.

**Expected output:**

```
['03-14', '06-20', '10-08']
4
3917 5129
```

There are four lines: the series itself and three vertical markers. Without
the shaded area the change on 2 September could be read as gradual growth;
the medians show it is a change of level that happened all at once.
