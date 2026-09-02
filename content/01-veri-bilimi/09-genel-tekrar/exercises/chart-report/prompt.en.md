You will combine grouping with visualisation: compute, draw, save.

**What you need to do:**

1. Compute the average score by city, round to one decimal and print it **as
   a dict**.
2. Create a canvas and a drawing area.
3. Draw the averages as a bar chart.
4. Force the axis to run from **0 to 100**.
5. Set the title to `Average score by city` and the y axis to `Score`.
6. Save it as `report.png` (`dpi=150`, `bbox_inches="tight"`) and close the
   canvas.
7. Print on one line, side by side: the number of bars, the upper bound of
   the axis (as a whole number), the title, and whether the file exists.

**Expected output:**

```
{'Ankara': 80.0, 'Bursa': 45.0, 'Izmir': 76.5}
3 100 Average score by city True
```

**This is the module's most repeated pattern:**

```python
averages = data.groupby("city")["score"].mean()
ax.bar(averages.index, averages.values)
```

`groupby(...).mean()` returns a Series — `index` is the groups and `values`
the numbers. A bar chart wants them separately.

**Starting the axis at zero** is not a preference here: the length of a bar
represents the value, and cutting off the bottom makes the chart lie.

And the chart is saved to a file — that is what goes into the report.
