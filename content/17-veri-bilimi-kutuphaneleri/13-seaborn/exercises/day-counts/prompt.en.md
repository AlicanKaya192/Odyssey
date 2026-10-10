`day_counts(days, order)` should draw how many times each day appears with
`sns.countplot`; the days go in the order of `order`. No bar is drawn for a
day that never appears in the data, so the list holds only the days that
appear, in that order. Close the figure and return the bar heights as an
`int` list. The starter code gives no order: the days line up in the order
they first appear in the data.

**Expected output:**

```
[3, 2, 1, 1]
```
