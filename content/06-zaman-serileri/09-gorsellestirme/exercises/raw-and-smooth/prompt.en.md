Draw the daily sales of 2024 with a faint line and two moving averages
on top with bold lines.

**What to do:**

1. Read the file. Compute the moving averages **on the whole series**
   (`s.rolling(7).mean()`, `s.rolling(28).mean()`), then select 2024. That
   way the first days of the year are not left empty.
2. On a `figsize=(10, 4)` canvas draw three lines: daily
   (`color="lightgray"`, label `daily`), 7-day (label `7-day mean`), 28-day
   (label `28-day mean`).
3. Add the legend (`ax.legend()`) and save as `chart.png`.
4. Print the number of lines.
5. Print the legend labels as a list:
   `[t.get_text() for t in ax.get_legend().get_texts()]`.
6. Print the number of `NaN` values in the 7-day and 28-day means within 2024
   on one line.

**Expected output:**

```
3
['daily', '7-day mean', '28-day mean']
0 0
```

Because you computed the means on the whole series first, 1 January 2024 has
a value too: the window is fed by the last days of 2023. Had you selected
2024 first and then called `rolling`, the first 27 days would have been
empty.
