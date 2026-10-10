`to_wide(records, months)` should turn the `[city, month, sales]` records
(each pair once) into a city × month table with `pivot`. `pivot` sorts the
columns alphabetically; put them in the order of `months`. Return:

- `"columns"`: the columns (a list)
- `"values"`: the table as a list of lists

**Do not write a loop.**

**Expected output:**

```
['jan', 'feb', 'mar']
[120, 110, 90]
[80, 95, 70]
```
