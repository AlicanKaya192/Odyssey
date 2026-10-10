`raw_points(hours, sales)` should draw with `sns.lineplot` but **without
averaging** the values at the same hour, each record as its own point
(`estimator=None`). Close the figure and return the number of points on the
line: `len(ax.lines[0].get_xdata())`. The starter code uses the default: it
reduces equal hours to one point.

**Expected output:**

```
5
```
