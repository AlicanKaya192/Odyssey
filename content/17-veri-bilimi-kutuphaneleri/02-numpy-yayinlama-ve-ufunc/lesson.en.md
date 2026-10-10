# Broadcasting and ufuncs

In NumPy, writing `array * 2` applies 2 to every item; writing `matrix - row`
subtracts the row from every row. This is **broadcasting**: two arrays of
different shapes enter an operation with the smaller one "spread" to the
larger one's shape, without being copied. The functions behind it that work
item by item are **ufuncs** (universal functions). This section covers the
rules of broadcasting, its most common mistake (`keepdims`) and the
lesser-known powers of ufuncs.

## The rule: compare from the right

```python
import numpy as np

col = np.array([[1], [2], [3]])
row = np.array([10, 20, 30, 40])
print(col.shape, row.shape, (col + row).shape)
print(col + row)
print(np.broadcast_shapes((5, 3), (3,)), np.broadcast_shapes((3, 1), (1, 4)))
```

```text
(3, 1) (4,) (3, 4)
[[11 21 31 41]
 [12 22 32 42]
 [13 23 33 43]]
(5, 3) (3, 4)
```

The two shapes are compared axis by axis **from the right**. On every axis the
two sizes must either be **equal** or one of them must be **1**; the one with
1 is spread to the other's size. A missing axis is added at the front as 1.

- `(3, 1)` + `(4,)` → `(4,)` first becomes `(1, 4)`; then on both axes one of
  them is 1: the result is `(3, 4)`. The column spread to every row, the row
  to every column.
- `(5, 3)` + `(3,)`: the last axes are equal (3); `(3,)` spreads over five
  rows. Subtracting a row from every row is exactly this.
- **No copy is made:** NumPy does not duplicate the small array in memory; it
  uses a step (stride) of 0.

## Scaling by column

```python
import numpy as np

X = np.array([[1.0, 200], [2, 400], [3, 600]])
Z = (X - X.mean(axis=0)) / X.std(axis=0)
print(X.mean(axis=0).shape)
print(Z.round(2).tolist())
```

```text
(2,)
[[-1.22, -1.22], [0.0, 0.0], [1.22, 1.22]]
```

- `X.mean(axis=0)` is the mean of every **column**: shape `(2,)`. `(3, 2)`
  and `(2,)` match from the right; the mean is subtracted from every row.
- The result is standardised data: every column has mean 0 and deviation 1.
  Machine learning's `StandardScaler` does exactly this inside.

## The most common mistake: by row, and keepdims

```python
import numpy as np

X = np.array([[1.0, 200], [2, 400], [3, 600]])
print(X.sum(axis=1).shape)
try:
    X / X.sum(axis=1)
except ValueError as error:
    print("ValueError:", str(error).strip())
share = X / X.sum(axis=1, keepdims=True)
print(X.sum(axis=1, keepdims=True).shape)
print(share.round(3).tolist())
```

```text
(3,)
ValueError: operands could not be broadcast together with shapes (3,2) (3,)
(3, 1)
[[0.005, 0.995], [0.005, 0.995], [0.005, 0.995]]
```

- We want to divide each row by its own total. `X.sum(axis=1)` has shape
  `(3,)`; compared from the right, `X`'s last axis (2) and 3 do not match: an
  **error**. (If the number of rows equalled the number of columns, there
  would not even be an error; it would divide along the **wrong** axis. More
  dangerous.)
- **`keepdims=True`** does not drop the summed axis; it leaves it as 1:
  `(3, 1)`. Now each row's own total spreads over it.
- The rule: for operations **by row** (axis=1), `keepdims=True`; by column
  (axis=0) it is not needed.

## Everyone with everyone: a distance matrix

```python
import numpy as np

points = np.array([[0, 0], [3, 4], [6, 8]])
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
print(diff.shape)
distance = np.sqrt((diff ** 2).sum(axis=-1))
print(distance.tolist())
```

```text
(3, 3, 2)
[[0.0, 5.0, 10.0], [5.0, 0.0, 5.0], [10.0, 5.0, 0.0]]
```

- `(3, 1, 2)` − `(1, 3, 2)` → `(3, 3, 2)`: the difference of every point to
  every point, **without a loop**. Summing the squares over the last axis and
  taking the square root gives the distance matrix.
- The insides of algorithms like k-nearest neighbours and clustering are
  computed this way (the Algorithms path, the ML Algorithms module).
- The price is memory: n × n × dimensions for n points; for a very large n it
  is computed in pieces.

## The hidden abilities of ufuncs

```python
import numpy as np

print(np.add.reduce([1, 2, 3, 4]), np.add.accumulate([1, 2, 3, 4]))
print(np.multiply.outer([1, 2], [10, 20, 30]).tolist())
print(np.maximum([1, 5, 3], [4, 2, 6]), np.maximum.reduce([3, 9, 2]))
out = np.empty(3)
np.multiply([1, 2, 3], 2, out=out)
print(out)
v = np.array([1.0, -2.0, 4.0])
print(np.sqrt(v, where=v >= 0, out=np.full(3, np.nan)))
```

```text
10 [ 1  3  6 10]
[[10, 20, 30], [20, 40, 60]]
[4 5 6] 9
[2. 4. 6.]
[ 1. nan  2.]
```

- Every ufunc has methods: **`reduce`** (combine them all: a sum),
  **`accumulate`** (cumulative), **`outer`** (every pair: a multiplication
  table).
- **`np.maximum`** compares two arrays item by item (`np.max` is the largest
  of one array; the two are different).
- **`out=`** writes the result into an existing array: in big loops a new
  array is not built every time.
- **`where=`** computes only where the condition holds; the square root of a
  negative number is skipped without a warning (`out` starts as `nan`).

## Vectorising a Python function?

```python
import timeit

import numpy as np

data = np.random.default_rng(1).normal(size=200_000)
vector = min(timeit.repeat(lambda: data * 2 + 1, number=1, repeat=3))
loop = min(timeit.repeat(lambda: [x * 2 + 1 for x in data], number=1, repeat=3))
wrapped = np.vectorize(lambda x: x * 2 + 1)
vectorized = min(timeit.repeat(lambda: wrapped(data), number=1, repeat=3))
print(loop / vector > 10, vectorized / vector > 10)
```

```text
True True
```

- The array operation (`data * 2 + 1`) is about 36 times faster than the loop
  on this computer.
- **`np.vectorize`** makes a Python function applicable to an array, but the
  name is misleading: inside it is still a loop; its speed is close to the
  loop (~27 times slower than the array operation). It is only for
  convenience.
- For speed, rewrite the expression with array operations (`np.where`,
  `np.clip`, ufuncs).

## Summary

- Broadcasting: shapes are compared from the right; equal or 1. The small
  array spreads without being copied.
- By column `X - X.mean(axis=0)`; by row `keepdims=True` is required.
- "Everyone with everyone" computations without loops via `[:, np.newaxis]`.
- ufunc methods: `reduce`, `accumulate`, `outer`; `out=` and `where=`.
- `np.vectorize` does not bring speed.
