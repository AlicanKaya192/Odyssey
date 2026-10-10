# NumPy Indexing

In the Data Science path you saw slicing, fancy indexing and conditional
selection. This section goes into two-dimensional and more complex selections:
selecting rows and columns together, knowing whether a selection is a **view
or a copy** (whether writing to it changes the original), combining
conditions, and tools like `where`, `argsort` and `unique` that answer the
question "where?".

## Selecting in two dimensions

```python
import numpy as np

m = np.arange(1, 13).reshape(3, 4)
print(m)
print(m[1, 2], m[:, 1])
print(m[1:, ::2].tolist())
```

```text
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]
7 [ 2  6 10]
[[5, 7], [9, 11]]
```

- **`m[row, column]`**: two axes at once, with a comma. `m[1][2]` gives the
  same result but first pulls out the whole row; `m[1, 2]` goes straight
  there, and a slice on the second axis (`m[:, 1]`) is only possible with
  this form.
- **`m[:, 1]`**: column 1 of every row.
- **`m[1:, ::2]`**: from row 1 to the end, skipping every other column.

## A row list and a column list: two different meanings

```python
import numpy as np

m = np.arange(1, 13).reshape(3, 4)
print(m[[0, 2], [1, 3]])
print(m[np.ix_([0, 2], [1, 3])])
```

```text
[ 2 12]
[[ 2  4]
 [10 12]]
```

- **Selecting with two lists pairs them up:** `m[[0, 2], [1, 3]]` takes the
  positions (0, 1) and (2, 3): **two items**, not a sub-matrix. One of the
  most common NumPy mistakes.
- For a **sub-matrix** (these rows × these columns), **`np.ix_`**: four items,
  2 × 2.

## View or copy?

```python
import numpy as np

m = np.arange(1, 13).reshape(3, 4)
part = m[0:2, 0:2]
part[0, 0] = 100
print(m[0, 0], np.shares_memory(m, part))
m[0, 0] = 1
picked = m[[0, 1]]
picked[0, 0] = -5
print(m[0, 0], np.shares_memory(m, picked))
m[m > 10][0] = 999
print(m.max())
m[m > 10] = 0
print(m[2].tolist())
```

```text
100 True
1 False
12
[9, 10, 0, 0]
```

- **A slice (`:`) is a view:** writing to `part` changed `m`.
- **Selecting with a list or a mask (fancy indexing) is a copy:** writing to
  `picked` did not touch `m`.
- **Chained assignment does nothing:** `m[m > 10][0] = 999` first pulls out a
  **copy**, then changes the copy's first item; `m` stayed the same (the
  largest is still 12).
- **Assignment in one step works:** `m[m > 10] = 0` writes straight into `m`.
  The rule: use the mask or list **on the left side of the assignment, in a
  single pair of brackets**.

## Combining conditions

```python
import numpy as np

v = np.array([5, -3, 8, 0, -1, 7])
print(v[(v > 0) & (v < 8)])
print(v[~(v > 0)])
print(v[(v < 0) | (v == 8)])
try:
    v[v > 0 and v < 8]
except ValueError as error:
    print("ValueError:", str(error)[:46])
```

```text
[5 7]
[-3  0 -1]
[-3  8 -1]
ValueError: The truth value of an array with more than one
```

- Masks combine with **`&`** (and), **`|`** (or), **`~`** (not); every
  condition goes in **parentheses**: `&` is applied before comparisons, so
  `v > 0 & v < 8` is read wrongly.
- Python's `and` / `or` / `not` words do not work on arrays: they expect a
  single `True` / `False` and cannot tell what to do with an array
  (`ValueError`).

## Where? where, nonzero, argsort

```python
import numpy as np

v = np.array([5, -3, 8, 0, -1, 7])
print(np.where(v > 0, v, 0))
print(np.where(v < 0)[0], np.nonzero(v)[0])
order = np.argsort(v)
print(order, v[order][::-1][:3])
scores = np.array([[3, 90], [1, 75], [2, 82]])
print(scores[scores[:, 1].argsort()[::-1]].tolist())
print(np.argmax(np.array([[1, 9, 3], [7, 2, 8]]), axis=1))
```

```text
[5 0 8 0 0 7]
[1 4] [0 1 2 4 5]
[1 4 3 0 5 2] [8 7 5]
[[3, 90], [2, 82], [1, 75]]
[1 2]
```

- **`np.where(condition, a, b)`**: `a` where the condition holds, `b`
  otherwise; an item-by-item "if-else". With a single argument
  (`np.where(condition)`) it gives the **positions** where it holds (a tuple;
  `[0]` for the first axis).
- **`np.nonzero(v)`**: the positions of the non-zero items.
- **`np.argsort(v)`** gives not the values but the **order** (the indices)
  that would sort them. `v[order]` is the sorted array; `[::-1][:3]` the three
  largest.
- **Sorting rows by a column:** all rows are selected with that column's
  `argsort`; here by score, largest first.
- **`argmax(axis=1)`**: the column position of the largest in each row.

## unique, isin, clip, newaxis

```python
import numpy as np

labels = np.array(["b", "a", "b", "c", "b"])
values, counts = np.unique(labels, return_counts=True)
print(values, counts)
print(np.isin(np.array([1, 2, 3, 4]), [2, 4]))
print(np.clip(np.array([5, -3, 8, 0]), 0, 5))
x = np.array([1, 2, 3])
print(x[:, np.newaxis].shape, x[np.newaxis, :].shape)
```

```text
['a' 'b' 'c'] [1 3 1]
[False  True False  True]
[5 0 5 0]
(3, 1) (1, 3)
```

- **`np.unique(..., return_counts=True)`**: the sorted distinct values and how
  many times each appears.
- **`np.isin(array, list)`**: is each item in the list (like `IN` in SQL).
- **`np.clip(array, low, high)`**: pulls everything outside the limits to the
  limit.
- **`np.newaxis`** (the same as `None`) adds a new dimension: `(3,)` → `(3, 1)`
  a column, `(1, 3)` a row. The key to broadcasting in the next section.

## Summary

- `m[row, column]`; `m[:, j]` is a column.
- Selecting with two lists **pairs** them; for a sub-matrix, `np.ix_`.
- A slice is a view, a list/mask a copy; chained assignment
  (`m[mask][0] = …`) does not change the original, `m[mask] = …` does.
- Masks with `&`, `|`, `~` and parentheses; not `and`/`or`.
- `where` (a conditional value / positions), `argsort` (the sorting order),
  `argmax`, `unique`, `isin`, `clip`, `newaxis`.
