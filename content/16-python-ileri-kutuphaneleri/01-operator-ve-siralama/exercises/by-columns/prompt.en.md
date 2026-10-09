Write the function `by_columns(rows, cols)`: return the rows (`rows`, a
list of lists) sorted by the column numbers in `cols` in turn: first by the
first column, then by the second if equal... `itemgetter(*cols)` is the key
that gives all the columns together.

**Expected output:**

```
['pen', 3, 1.5]
['book', 3, 12.0]
['ink', 10, 0.5]
```
