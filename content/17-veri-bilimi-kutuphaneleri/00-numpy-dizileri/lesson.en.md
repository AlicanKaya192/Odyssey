# NumPy Arrays and Data Types

In the Data Science path you built NumPy arrays, selected from them and summed
them. This module goes **behind the scenes** of the same libraries. The first
stop is the array's data type (dtype): every item of an array is stored with
the same type and the same size. That is what makes NumPy fast; but when the
wrong type is chosen, numbers break **silently**, text gets cut and memory is
wasted. This section shows those silent errors by measuring them.

## Every array has a dtype

```python
import numpy as np

a = np.array([1, 2, 3])
print(a.dtype, a.itemsize, a.nbytes)
print(np.array([1.5, 2, 3]).dtype)
mixed = np.array([1, 2.5, "x"])
print(mixed.dtype, mixed)
print(np.array([1, None]).dtype)
```

```text
int64 8 24
float64
<U32 ['1' '2.5' 'x']
object
```

- **`dtype`** is the type of the items, **`itemsize`** the size of one item in
  bytes, **`nbytes`** the size of the whole array. On this computer the
  default for integers is `int64`: 8 bytes per item.
- When types mix, NumPy moves up to the **single** type that can carry them
  all: if there is one decimal, everything becomes `float64`.
- If a string mixes in, **everything becomes text** (`<U32`: Unicode of at
  most 32 characters). The numbers are no longer numbers; adding them fails.
- If `None` mixes in, `object`: the items are stored as ordinary Python
  objects and NumPy's speed is lost.

## Overflow: numbers that break silently

```python
import numpy as np

print(np.iinfo(np.int8).min, np.iinfo(np.int8).max)
small = np.array([100, 120], dtype=np.int8)
print(small + small, (small + small).dtype)
print(np.array([300]).astype(np.int8))
print(np.iinfo(np.int64).max)
```

```text
-128 127
[-56 -16] int8
[44]
9223372036854775807
```

- **`int8`** holds −128 to 127. `100 + 100 = 200` does not fit; the result
  became `-56` **without a warning** (the overflowing value wraps around).
  Python's own `int` has no such limit; NumPy's types do.
- **`astype(np.int8)`** turned 300 into `44`, again without a warning.
- **`np.iinfo(type)`** gives the limits of an integer type; for decimals,
  `np.finfo`.
- The rule: a small type **saves memory** (below) but is used only when you
  are **sure** the values fit. The results of additions and multiplications
  must fit too.

## float32 and precision

```python
import numpy as np

print(np.finfo(np.float32).eps, np.finfo(np.float64).eps)
count = np.float32(16_777_217)
print(count, int(count))
print(np.float64(16_777_217) == 16_777_217)
```

```text
1.1920929e-07 2.220446049250313e-16
1.6777216e+07 16777216
True
```

- **`float32`** holds about 7 significant digits, **`float64`** about 16;
  `eps` is the gap between 1 and the smallest number above 1.
- 16,777,217 does not fit in `float32`: the closest value is 16,777,216. Big
  counters, ID numbers and amounts in cents **break** in `float32`.
- `float32` is common in deep learning (half the memory, fast on graphics
  cards); for statistics and money, `float64` (or the ways from the decimal
  section).

## Memory: the right type, a smaller array

```python
import numpy as np

big = np.arange(1_000_000)
print(big.nbytes // 1024, big.astype(np.int32).nbytes // 1024,
      big.astype(np.int16).nbytes // 1024)
names = np.array(["ab", "cde"])
print(names.dtype)
names[0] = "hello"
print(names)
```

```text
7812 3906 1953
<U3
['hel' 'cde']
```

- A million `int64`s take 7812 KB; `int32` half of that, `int16` a quarter.
  If the values fit, shrinking the type divides the memory directly (this
  million does not fit in `int16`; here we only show the size).
- **A text array has a fixed width:** the array `["ab", "cde"]` is `<U3`,
  that is at most 3 characters. Assigning `"hello"` **silently** gave
  `"hel"`. For text of varying length, pandas' text columns or
  `dtype=object` are used.

## Ways to build an array

```python
import numpy as np

print(np.arange(0, 1, 0.25))
print(np.linspace(0, 1, 5))
print(np.full((2, 2), 7))
print(np.eye(3, dtype=int))
print(np.zeros_like(np.array([1, 2, 3])), np.ones(3, dtype=bool))
```

```text
[0.   0.25 0.5  0.75]
[0.   0.25 0.5  0.75 1.  ]
[[7 7]
 [7 7]]
[[1 0 0]
 [0 1 0]
 [0 0 1]]
[0 0 0] [ True  True  True]
```

- **`arange(start, stop, step)`**: the stop is not included. With a decimal
  step, rounding can make the number of items surprising; that is why
  **`linspace(start, stop, count)`** is preferred for a decimal range (the
  stop is included).
- **`full(shape, value)`**, **`eye(n)`** (the identity matrix), **`zeros` /
  `ones`**.
- **`*_like(array)`** builds a new array with the same shape and type.
- Every builder takes `dtype=`; the right type from the start is cheaper
  than `astype` later.

## Shape, views and copies

```python
import numpy as np

m = np.arange(12).reshape(3, 4)
print(m.shape, m.ndim, m.size, m.strides)
flat_view = m.ravel()
flat_view[0] = 99
flat_copy = m.flatten()
flat_copy[1] = -1
print(m[0, :3])
print(np.shares_memory(m, flat_view), np.shares_memory(m, flat_copy))
print(np.arange(6).reshape(2, -1).shape)
try:
    m.reshape(5, 3)
except ValueError as error:
    print("ValueError:", error)
```

```text
(3, 4) 2 12 (32, 8)
[99  1  2]
True False
(2, 3)
ValueError: cannot reshape array of size 12 into shape (5,3)
```

- **`shape`** is the dimensions, **`ndim`** the number of dimensions,
  **`size`** the number of items. **`strides`** is how many bytes to skip in
  memory to move to the next row / column: 32 bytes for a row (4 × 8), 8
  bytes for a column. NumPy usually changes shape by changing only these
  numbers, without copying the data.
- **`ravel()`** returns a **view** when it can: it looks at the same memory,
  and writing to it changed `m` (`99`). **`flatten()`** always returns a
  **copy**: writing to it did not touch `m`.
- **`np.shares_memory(a, b)`** tells whether two arrays share the same memory;
  the definite answer to "is this a copy?".
- In `reshape`, **`-1`** means "work out the rest yourself". If the item
  count does not match, `ValueError`.

## Missing values and integers

```python
import numpy as np

print(np.nan == np.nan, np.isnan(np.array([1.0, np.nan])))
counts = np.array([3, 4, 5])
try:
    counts[0] = np.nan
except ValueError as error:
    print("ValueError:", error)
print(np.array([3, np.nan, 5]).dtype)
```

```text
False [False  True]
ValueError: cannot convert float NaN to integer
float64
```

- **`NaN` is not equal even to itself**; missing values are found with
  `np.isnan`.
- NaN is a **decimal** value: it cannot go into an integer array. That is why
  a number column with missing values becomes `float64`. (pandas types like
  `Int64` solve this; in the pandas performance section.)

## Summary

- Every array has a single `dtype`; mixed input moves up to the widest type
  (text and `None` included).
- Integer arrays wrap around **without a warning** when they overflow; `iinfo`
  gives the limits. `astype` breaks values silently too.
- `float32` holds ~7 digits; it breaks big numbers.
- The right type divides memory; a text array has a fixed width.
- `ravel` is a view, `flatten` a copy; to be sure, `np.shares_memory`.
- NaN is a decimal and does not go into an integer array.
