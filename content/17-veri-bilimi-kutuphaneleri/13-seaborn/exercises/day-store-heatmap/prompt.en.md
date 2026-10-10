`day_store_table(days, stores, sales, day_order, store_order)` should build the
day × store **mean** sales table with `pivot_table`, put the rows in
`day_order` and the columns in `store_order` order, and draw it with
`sns.heatmap(..., annot=True, fmt=".0f")`. Save it as `heat.png`, close the
figure and return:

- `"shape"`: the table's shape `[rows, columns]`
- `"first_row"`: the cell texts of the first row (from `ax.texts`, in order)

**Expected output:**

```
[2, 2]
['100', '80']
```
