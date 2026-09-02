You will draw your first bar chart — and **label** it.

**What you need to do:**

1. Create a canvas and a drawing area (`fig`, `ax`).
2. Draw a **bar chart** with the cities on the x axis and the scores on the
   y axis.
3. Set the title to `Average score by city`.
4. Label the x axis `City` and the y axis `Score`.
5. Print, in order: the number of bars, the title, the x label and the y
   label.

**Expected output:**

```
4
Average score by city
City
Score
```

**Why the labels are part of this exercise:** a chart is drawn to be shown to
someone. A chart without a title and axis labels is an unfinished sentence —
whoever sees it does not know what they are looking at.

You can read back what you drew with calls like `ax.patches` (the bars) and
`ax.get_title()`. That is how you confirm a chart was drawn correctly.
