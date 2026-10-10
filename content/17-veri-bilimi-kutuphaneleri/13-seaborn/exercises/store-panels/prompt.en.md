`store_panels(hours, sales, stores, order)` should open one panel per store
with `sns.relplot` (`col="store"`, `col_order=order`, `height=2`). The panel
titles should be just the store name (`set_titles("{col_name}")`). Save it as
`panels.png`, close the figure and return `{"shape": [rows, columns],
"titles": [...]}`. In the starter code the titles look like `store =
Izmir`.

**Expected output:**

```
[1, 2]
['Izmir', 'Bursa']
```
