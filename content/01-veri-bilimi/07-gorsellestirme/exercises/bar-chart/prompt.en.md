You will show each city's average score as a **bar chart** — and see the
chart you drew.

The data is in `students.csv`; its first lines look like this:

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

1. Import `pandas` and `matplotlib.pyplot` and read the file.
2. Work out the average score per city.
3. Create a figure and an axes (`plt.subplots()`) and draw the averages as
   bars: cities along the bottom, averages up the side.
4. Set the title to `Average score by city`, the x axis to `City` and the y
   axis to `Score`.
5. Save the chart as **`chart.png`**.
6. Print, in order: the number of bars, the title, and the two axis labels
   (with ` | ` between them).

**Expected output:**

```
4
Average score by city
City | Score
```

Once you run it, your chart appears in the **results panel**.

**A bar chart compares categories.** Grouping gives you a Series: its
`index` holds the cities and its `values` the numbers. `ax.bar` wants the
two separately, which is why you write `ax.bar(averages.index,
averages.values)`.

There is no need for `plt.show()`; there is no window here, you save the
chart to a file.
