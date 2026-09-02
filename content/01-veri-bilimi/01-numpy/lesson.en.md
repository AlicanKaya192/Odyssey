# NumPy Arrays

In the previous section you computed an average by hand, filtered with a
loop and grouped with dictionaries. It all worked. Now you will learn to do
the same jobs **without writing a loop**.

NumPy has a single data structure: the **array**. This section is about that
structure and what you do with it.

```python
import numpy as np
```

The `np` abbreviation is a convention. Everybody writes it this way; you
should too, so anyone reading your code knows what it is.

## Why not a list?

You want to multiply the elements of two lists:

```python
a = [1, 2, 3, 4]
b = [2, 3, 4, 5]

result = []
for i in range(len(a)):
    result.append(a[i] * b[i])

print(result)
```

```text
[2, 6, 12, 20]
```

The same job with NumPy:

```python
a = np.array([1, 2, 3, 4])
b = np.array([2, 3, 4, 5])

print(a * b)
```

```text
[ 2  6 12 20]
```

No loop, no `append`, no empty list. This is called a **vectorised
operation**: you tell the whole array what to do, not each element.

There are two reasons to work this way:

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Short</h4>
      <p>Five lines become one. Easy to write, easy to read, hard to get wrong.</p>
    </div>
    <div class="versus-side">
      <h4>Fast</h4>
      <p>The loop runs in C underneath, not in Python. On millions of elements the difference is measured in seconds.</p>
    </div>
  </div>
</figure>

Where does the speed come from? Because **an array holds a single type.** A
Python list keeps a separate object with its own type information for every
element; an array says "all of these are `int64`" and stores the raw numbers
side by side.

## Creating an array

The most common way is converting a list:

```python
numbers = np.array([3, 7, 1, 9])
print(numbers)
```

```text
[3 7 1 9]
```

There are also ways to generate one from scratch:

```python
print(np.zeros(4, dtype=int))
print(np.arange(0, 10, 2))
print(np.linspace(0, 1, 5))
```

```text
[0 0 0 0]
[0 2 4 6 8]
[0.   0.25 0.5  0.75 1.  ]
```

`arange` takes a **step** (from zero to ten, in twos), `linspace` takes **how
many pieces** you want (five numbers between zero and one). These two get
confused often: `arange` leaves the end out, `linspace` includes it.

## Attributes of an array

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(matrix.ndim)    # how many dimensions
print(matrix.shape)   # how many elements per dimension
print(matrix.size)    # total elements
print(matrix.dtype)   # the type inside
```

```text
2
(2, 3)
6
int64
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">ndim</span><span class="anat-body">number of dimensions — 1 a vector, 2 a table, 3 and up deeper structures</span></div>
    <div class="anat-row"><span class="anat-label">shape</span><span class="anat-body">a tuple: <code>(rows, columns)</code>. The attribute you use most</span></div>
    <div class="anat-row"><span class="anat-label">size</span><span class="anat-body">total number of cells — the values in <code>shape</code> multiplied</span></div>
    <div class="anat-row"><span class="anat-label">dtype</span><span class="anat-body">the shared type of every element</span></div>
  </div>
</figure>

## What a single type means

If you put different types into an array, NumPy converts them all to a
**common type**:

```python
mixed = np.array([1, 2.5, 3])
print(mixed.dtype)
print(mixed)
```

```text
float64
[1.  2.5 3. ]
```

The integers became decimals. In the other direction you get **data loss**:

```python
values = np.array([1, 2, 3])
values[0] = 9.7
print(values)
```

```text
[9 2 3]
```

`9.7` quietly became `9` — the array's type is `int64` and the decimal part
was dropped. No error, no warning. This is one of the most common traps in
NumPy.

## Reshaping

Seeing the same data in a different arrangement:

```python
flat = np.arange(6)
print(flat)
print(flat.reshape(2, 3))
```

```text
[0 1 2 3 4 5]
[[0 1 2]
 [3 4 5]]
```

The number of elements has to match: you can make six elements `(2, 3)`, but
not `(2, 4)` — you get a `ValueError`.

## Selecting

In one dimension it is the same as a list:

```python
values = np.array([10, 20, 30, 40, 50])

print(values[0])
print(values[-1])
print(values[1:4])
```

```text
10
50
[20 30 40]
```

In two dimensions you use a comma: `[row, column]`.

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(matrix[0, 2])   # first row, third column
print(matrix[1])      # the whole second row
print(matrix[:, 0])   # the first column of every row
```

```text
3
[4 5 6]
[1 4]
```

`matrix[0][2]` also works, but `matrix[0, 2]` is both shorter and faster: the
first one builds an intermediate array on the way.

## A slice is not a copy

This behaviour breaks the habit you brought from lists:

```python
values = np.array([1, 2, 3, 4, 5])
part = values[1:3]
part[0] = 99

print(values)
```

```text
[ 1 99  3  4  5]
```

`part` is not a new array but a **window** (a view) onto the same data.
Changing it changes the original. A Python list does not behave this way;
`some_list[1:3]` gives you a real copy.

If you want a copy you have to ask for it:

```python
part = values[1:3].copy()
```

The reason is speed: not copying the data when you slice a million-element
array is a big win. But it is also easy to corrupt the original without
noticing.

## Fancy indexing

Selecting several elements with a list of indices:

```python
values = np.array([10, 20, 30, 40, 50])
picked = values[[0, 3, 4]]
print(picked)
```

```text
[10 40 50]
```

The difference from a slice: the selection **does not have to be in order**,
and the result is a real copy.

## Selecting by condition

This is what you will use most. When you make a comparison, NumPy hands you
an array of `True`/`False`:

```python
scores = np.array([45, 82, 91, 60, 74])

print(scores > 70)
```

```text
[False  True  True False  True]
```

Putting that array inside the square brackets gives you **only the ones that
are `True`**:

```python
print(scores[scores > 70])
print(scores[scores > 70].mean())
```

```text
[82 91 74]
82.33333333333333
```

Those two lines are the equivalent of the ten lines you wrote in the previous
section.

To combine conditions you use `&` and `|`, not `and` and `or` — and the
**parentheses are required**:

```python
print(scores[(scores > 50) & (scores < 90)])
```

```text
[82 60 74]
```

If you write `and` you get a `ValueError`: Python expects a single truth
value, and what you have is five of them.

## Arithmetic and aggregation

Across the whole array at once:

```python
values = np.array([3, 7, 1, 9])

print(values + 10)
print(values * 2)
print(values.sum())
print(values.mean())
print(values.min(), values.max())
print(values.argmax())
```

```text
[13 17 11 19]
[ 6 14  2 18]
20
5.0
1 9
3
```

`argmax` gives you the **position**, not the value itself: the largest
element is at index three. That is exactly what you need for "who got the
highest score".

## axis: in which direction?

On a two-dimensional array "the total" is an ambiguous request — of the rows
or of the columns?

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(matrix.sum())
print(matrix.sum(axis=0))
print(matrix.sum(axis=1))
```

```text
21
[5 7 9]
[ 6 15]
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">no axis</span><span class="anat-body">add everything up, get one number</span></div>
    <div class="anat-row"><span class="anat-label">axis=0</span><span class="anat-body">go down through the rows — you get <b>column</b> totals</span></div>
    <div class="anat-row"><span class="anat-label">axis=1</span><span class="anat-body">go across through the columns — you get <b>row</b> totals</span></div>
  </div>
  <figcaption>A way to keep it straight: axis reads as "which one disappears". axis=0 removes the rows and leaves the columns.</figcaption>
</figure>

Because rows are records and columns are attributes in a table, `axis=0`
usually means "the average of each attribute" — the form you will use most.

## Broadcasting

When you work with arrays of different shapes, NumPy **stretches the smaller
one to fit**:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bonus = np.array([10, 20, 30])

print(matrix + bonus)
```

```text
[[11 22 33]
 [14 25 36]]
```

`bonus` has three elements, `matrix` has two rows. NumPy adds `bonus` to each
row separately. You do not have to write a loop for it.

The rule is: shapes are compared **from the end backwards**, and at every
position they must either be equal or one of them must be 1. If they do not
match you get an error.

## Missing values

In real data cells are empty. In NumPy that is `np.nan`:

```python
scores = np.array([80.0, np.nan, 90.0])

print(scores.mean())
print(np.nanmean(scores))
```

```text
nan
85.0
```

**A single missing value turns the whole result into `nan`.** This is
deliberate: NumPy is saying "a total that includes an unknown number is also
unknown".

On arrays containing `nan` you use `nanmean`, `nansum` and `nanmax`.
`np.isnan` tells you which cells are empty:

```python
print(np.isnan(scores))
print(scores[~np.isnan(scores)])
```

```text
[False  True False]
[80. 90.]
```

The `~` means "not": select the ones that are not `True`.

One oddity: `np.nan == np.nan` is `False`. An unknown number is not equal to
another unknown number. That is why you cannot search for it with equality
and need `isnan`.

## Summary

- NumPy's data structure is the **array**: single type, fixed size, fast.
- **Vectorised operation:** `a * b` multiplies the whole array, no loop
  needed.
- `ndim`, `shape`, `size`, `dtype` — an array's identity. `shape` is the one
  you use most.
- One type only: put a decimal into an `int` array and it is **silently
  truncated**.
- **A slice is not a copy**, it is a window onto the same data. Use `.copy()`
  for a real copy.
- Selecting by condition: `scores[scores > 70]`. Combine conditions with `&`
  and `|`, and do not forget the parentheses.
- `axis=0` gives a result per column, `axis=1` per row.
- **Broadcasting:** different shapes are stretched to fit, without a loop.
- A missing value is `np.nan`; a single one turns the mean into `nan`, which
  is what `nanmean` and `isnan` are for.
