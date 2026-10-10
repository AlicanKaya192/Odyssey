`twin_axes(temp, sales)` should draw temperature on the left axis and sales on
the **right** axis opened with `ax.twinx()`. The left axis is named
`"temperature"`, the right `"sales"`; the lines' `label`s are the same names.
Show both lines in a **single** legend (`ax.legend(handles=[...])`). Save it
as `twin.png` and close the figure. Return `[number_of_areas, left_name,
right_name, names_in_legend]`. The starter code draws both series on the same
axis; temperature stays like a flat line next to sales.

**Expected output:**

```
2 temperature sales
['temperature', 'sales']
```
