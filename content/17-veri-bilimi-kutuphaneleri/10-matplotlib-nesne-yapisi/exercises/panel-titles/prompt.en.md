`panel_titles(rows, cols)` should open a figure with `rows × cols` areas, give
them the titles `"p0"`, `"p1"`, ... in order and return `[[rows, cols],
[titles]]` (the array's shape and the titles in `fig.axes` order). The
starter code uses `axes.flat`, but `plt.subplots(1, 1)` returns a single
`Axes`, so it fails there. `squeeze=False` gives a two-dimensional array in
every case. Close the figure.

**Expected output:**

```
[2, 3]
['p0', 'p1', 'p2', 'p3', 'p4', 'p5']
[[1, 1], ['p0']]
```
