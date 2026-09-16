You will combine grouping and charts: **compute, sort, draw, save.** This
is exactly how a chart for a report is made.

The data is in `students.csv`:

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
2. Work out the average score per city, round it to one decimal and **sort
   it from highest to lowest**; print it as a dictionary.
3. Draw the averages as a bar chart and open the axis **from 0 to 100**.
4. Set the title to `Average score by city` and the y axis to `Score`.
5. Save it as **`report.png`** (`dpi=150`, `bbox_inches="tight"`) and close
   the figure.
6. Print side by side on one line: the number of bars, the upper axis limit
   (a whole number) and the title.

**Expected output:**

```
{'Ankara': 85.2, 'Adana': 82.0, 'Izmir': 71.3, 'Bursa': 70.0}
4 100 Average score by city
```

Once you run it, your chart appears in the **results panel**.

**The pattern this module repeats most:**

```python
averages = data.groupby("city")["score"].mean()
ax.bar(averages.index, averages.values)
```

**Sorting is not taste, it is readability.** With the bars in alphabetical
order the reader has to hunt for the tallest; sorted, the first bar is the
answer. **Starting the axis at zero** is not taste either: the length of a
bar stands for its value.
