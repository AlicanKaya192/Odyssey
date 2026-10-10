`grouped_bars(names, a, b)` should draw the two series **side by side** in each
category: `x = np.arange(len(names))`, the first series at `x - 0.2`, the
second at `x + 0.2`, width `0.4`. Centre the ticks with `ax.set_xticks(x,
names)`. Close the figure and return `[number_of_bars, bar_centres]`; a
bar's centre is `p.get_x() + p.get_width() / 2`, rounded to 1 place, in
`ax.patches` order. In the starter code both series are drawn in the same
place.

**Expected output:**

```
[6, [-0.2, 0.8, 1.8, 0.2, 1.2, 2.2]]
```
