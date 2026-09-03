A list to look at when you get stuck on the exercises. Everything assumes
`import numpy as np`.

## Creating arrays

| Written as | What it does |
|---|---|
| `np.array([1, 2, 3])` | Builds an array from a list |
| `np.array([[1, 2], [3, 4]])` | A two-dimensional array |
| `np.zeros(5)` | Five zeros (decimal) |
| `np.zeros(5, dtype=int)` | Five zeros (integer) |
| `np.ones(3)` | Three ones |
| `np.full(4, 7)` | Four sevens |
| `np.arange(0, 10, 2)` | From 0 to 10 **in twos**: `[0 2 4 6 8]` |
| `np.linspace(0, 1, 5)` | **Five** numbers between 0 and 1, ends included |
| `np.eye(3)` | The identity matrix |

`arange` leaves the end out, `linspace` includes it. This is the pair that
gets confused most.

## Attributes

| Written as | What it gives |
|---|---|
| `a.ndim` | Number of dimensions |
| `a.shape` | The `(rows, columns)` tuple |
| `a.size` | Total number of elements |
| `a.dtype` | The element type |
| `len(a)` | The number of elements in the **first** dimension — rows in 2D |

`a.shape` is a tuple: `a.shape[0]` is the number of rows, `a.shape[1]` the
number of columns.

## Changing shape

| Written as | What it does |
|---|---|
| `a.reshape(2, 3)` | Shows the same data as 2x3 |
| `a.reshape(-1)` | Flattens; `-1` means "work the rest out" |
| `a.reshape(3, -1)` | Three rows, let the columns be computed |
| `a.T` | Transpose: rows become columns |
| `a.flatten()` | Flattens and returns a **copy** |
| `a.ravel()` | Flattens, avoiding a copy where possible |

The number of elements has to match; if it does not you get a `ValueError`.

## Selecting

| Written as | What it selects |
|---|---|
| `a[0]` | The first element (the first row in 2D) |
| `a[-1]` | The last element |
| `a[1:4]` | From 1 to 4 (4 not included) |
| `a[::2]` | Every other one |
| `a[::-1]` | Reversed |
| `a[1, 2]` | Second row, third column |
| `a[:, 0]` | The first column of every row |
| `a[0, :]` | The whole first row |
| `a[[0, 3]]` | Fancy indexing: elements 0 and 3 |
| `a[a > 5]` | Selecting by condition |

**A slice is not a copy; use `.copy()` for one.** Fancy indexing and
selecting by condition already give you a copy.

## Conditions

| Written as | What it does |
|---|---|
| `a > 5` | An array of `True`/`False` |
| `a[a > 5]` | The elements that match |
| `(a > 5) & (a < 10)` | Two conditions together — **parentheses required** |
| `(a < 2) \| (a > 8)` | Either one or the other |
| `~(a > 5)` | The opposite |
| `np.where(a > 5, 1, 0)` | Write 1 where it matches, 0 where it does not |
| `(a > 5).sum()` | How many match (`True` counts as 1) |
| `(a > 5).any()` | Does at least one match |
| `(a > 5).all()` | Do they all match |

`and` / `or` / `not` **do not work**; an array has no single truth value.

## Arithmetic

| Written as | What it does |
|---|---|
| `a + 10` | Adds 10 to every element |
| `a * b` | Multiplies element by element |
| `a ** 2` | Squares every element |
| `a @ b` | Matrix multiplication (not element by element) |
| `np.sqrt(a)` | Square root |
| `np.round(a, 2)` | Two digits after the point |
| `np.abs(a)` | Absolute value |

## Aggregation

| Written as | What it gives |
|---|---|
| `a.sum()` | The total |
| `a.mean()` | The average |
| `a.std()` | The standard deviation |
| `a.min()` / `a.max()` | Smallest / largest |
| `a.argmin()` / `a.argmax()` | The **position** of the smallest / largest |
| `np.median(a)` | The median |
| `np.unique(a)` | The distinct values, sorted |
| `np.sort(a)` | A sorted **copy** |
| `a.cumsum()` | Running total |

The ones starting with `arg` give you the **index**, not the value.

## axis

| Written as | Result |
|---|---|
| `a.sum()` | A single number |
| `a.sum(axis=0)` | One number per **column** |
| `a.sum(axis=1)` | One number per **row** |

A way to remember: `axis` means "which dimension disappears". `axis=0`
removes the rows and leaves one result per column.

Because a row is a record in a table, `axis=0` usually means "the average of
each attribute".

## Missing values

| Written as | What it does |
|---|---|
| `np.nan` | A missing value |
| `np.isnan(a)` | Which cells are empty |
| `a[~np.isnan(a)]` | The ones that are not empty |
| `np.nanmean(a)` | The mean, skipping the empty ones |
| `np.nansum(a)` | The total, skipping the empty ones |
| `np.isnan(a).sum()` | How many are empty |

`np.nan` is always a decimal; an array containing `nan` cannot be `int`.

## Random numbers

| Written as | What it does |
|---|---|
| `np.random.seed(42)` | Makes the result repeatable |
| `np.random.randint(0, 10, size=5)` | Five integers between 0 and 9 |
| `np.random.random(5)` | Five decimals between 0 and 1 |
| `np.random.normal(10, 2, 5)` | Five numbers with mean 10, deviation 2 |

Without `seed` you get a different result on every run. When an exercise
expects a specific output, `seed` is essential.
