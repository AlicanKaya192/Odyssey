You will see the **distribution** of the scores with a histogram and save
the chart at a quality fit for a report.

The data is `students.csv`:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

**What to do:**

1. Write the imports and read the file.
2. Draw a **histogram** of the `score` column with `bins=5`.
3. Set the title to `Score distribution`, the x axis to `Score` and the y
   axis to `Students`.
4. Save the chart as **`histogram.png`** with `dpi=150` and
   `bbox_inches="tight"`. Then close the figure.
5. Print, in order: the number of bars, how many students fall in each
   range (as a list), the mean (one decimal) and the median side by side,
   and the title.

**Expected output:**

```
5
[2, 3, 3, 2, 2]
77.4 77.5
Score distribution
```

Once you run it, your chart appears in the **results panel**.

**Worth knowing:**

- **A histogram is not a bar chart:** a bar chart has categories, a
  histogram has **ranges of numbers**. The mean gives one number; the
  histogram shows the **shape** — one peak or two, where the extremes are.
- `ax.hist` returns three things: the count in each range, the edges of the
  ranges and the bars it drew. The list comes from the first one.
- `dpi=150` is report resolution; `bbox_inches="tight"` trims the extra
  margin.
- `plt.close(fig)` closes the figure. If you make charts in a loop it is a
  must, otherwise open figures pile up.
