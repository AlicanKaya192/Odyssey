`save_all(series)` should open a separate figure for each series in the name →
values dictionary, draw it, use the name as the title and save it as
`<name>.png`. After saving, **close** each figure. Return `[number_of_files,
number_of_open_figures]`; the number of open figures is
`len(plt.get_fignums())`. The starter code does not close the figures.

**Expected output:**

```
[3, 0]
```
