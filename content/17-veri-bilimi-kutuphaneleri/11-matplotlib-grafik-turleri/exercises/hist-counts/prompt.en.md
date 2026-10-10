`hist_counts(a, b, bins, low, high)` should draw the two data sets as
histograms in the same area; both must use **the same** bins: `bins=bins`,
`range=(low, high)`. `ax.hist` also returns the counts (`counts, edges, _ =
ax.hist(...)`). Close the figure and return `[a_counts, b_counts]` (each a
list of `int`). The starter code passes no `range`; the bins sit somewhere
else for each data set.

**Expected output:**

```
[1, 4, 2, 0]
[0, 1, 4, 3]
```
