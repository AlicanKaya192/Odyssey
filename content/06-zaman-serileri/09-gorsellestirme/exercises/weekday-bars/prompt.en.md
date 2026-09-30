Show mean sales by day of the week as a bar chart.

**What to do:**

1. Read the file and compute the mean by day of the week:
   `s.groupby(s.index.dayofweek).mean()`.
2. With `labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]` draw a
   bar chart (`ax.bar(labels, profile.values)`) and save it as `chart.png`.
3. Print the number of bars (`len(ax.patches)`).
4. Print the lower limit of the vertical axis (`ax.get_ylim()[0]`).
5. Print the name and mean (one decimal) of the highest and the lowest day,
   one per line.
6. Print the ratio of the weekend mean (Saturday and Sunday) to the weekday
   mean, rounded to two decimals.

**Expected output:**

```
7
0.0
Sat 336.1
Mon 217.6
1.33
```

The vertical axis starts at zero: matplotlib does that by itself for a bar
chart. It is also the right thing, because the length of a bar tells the
value; had you started the axis higher up, the difference between Saturday
and Monday would look far bigger than it is.
