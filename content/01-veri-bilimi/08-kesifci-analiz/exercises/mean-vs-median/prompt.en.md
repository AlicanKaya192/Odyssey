You will summarise the scores of an exam and see in a chart **why the mean
can mislead**.

The data is in `exam.csv`; its first lines look like this:

```text
student,score
S01,95
S02,92
S03,90
S04,88
S05,88
S06,86
...
```

**What to do:**

1. Write the imports and read the file.
2. Print, in order, the mean of `score` (two decimals), its median and its
   standard deviation (two decimals).
3. Is the mean smaller than the median? Print `True` or `False`.
4. Draw a **histogram** of the scores (`bins=6`).
5. Mark the mean with a **dashed red** vertical line and the median with a
   **green** vertical line; label both and add a legend.
6. Set the title to `Exam scores` and the x axis to `Score`, and save it as
   **`histogram.png`**.

**Expected output:**

```
73.2
84.0
22.89
True
```

Once you run it, your chart appears in the **results panel**.

**What the chart shows:** most scores are bunched between 80 and 95, with a
few very low ones on the left. Those four low scores **pull the mean
down**; the red line sits well to the left of where most students are. The
median looks at the student in the middle and ignores the extremes — the
green line is inside the crowd.

**The rule:** when a distribution leans to one side, look at the median for
the "typical" value. If you report the mean, put the median next to it.
