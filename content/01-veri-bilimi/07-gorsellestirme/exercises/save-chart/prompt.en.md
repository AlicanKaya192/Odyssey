You will draw a histogram and **save it to a file** — the real step in
reporting.

**What you need to do:**

1. Draw a **histogram** of the `score` column using `bins=4`.
2. Set the title to `Score distribution` and the x axis to `Score`.
3. Save the chart as `chart.png` with `dpi=150` and `bbox_inches="tight"`.
4. Close the canvas.
5. Print, in order: whether the file exists, whether its size is greater than
   zero, and the title.

**Expected output:**

```
True
True
Score distribution
```

**Things to know:**

- A **histogram** differs from a bar chart: there you have categories, here
  **numeric ranges**. `describe()` gave you the mean; a histogram shows the
  **shape** — two peaks, a skew, where the extremes are.
- `dpi=150` gives a resolution good enough for a report.
- `bbox_inches="tight"` trims the excess margin so long labels are not cut
  off.
- `plt.close(fig)` closes the canvas. If you produce charts in a loop this is
  essential: otherwise open canvases pile up and matplotlib warns you.

There is also `plt.show()`, but there is no window in Odyssey; and saving to
a file is more useful for reporting anyway.
