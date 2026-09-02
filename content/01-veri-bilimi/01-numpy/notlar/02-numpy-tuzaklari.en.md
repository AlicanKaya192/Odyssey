# NumPy Traps

Most NumPy mistakes **do not raise an error.** The program runs, hands you a
number, and the number is wrong. These are the ones people hit most.

## 1. A slice changes the original array

```python
values = np.array([1, 2, 3, 4, 5])
part = values[1:3]
part[0] = 99
print(values)
```

```text
[ 1 99  3  4  5]
```

A Python list does not behave this way; there a slice is a real copy. In
NumPy a slice is a **window** onto the same data.

**The fix:** ask for `.copy()` if you are going to modify it.

```python
part = values[1:3].copy()
```

**How do I tell?** If `part.base` points at the original array it is a
window; if it is `None` it is a copy.

Fancy indexing (`a[[0, 2]]`) and selecting by condition (`a[a > 5]`) already
give you a copy; only slices are windows.

## 2. Putting a decimal into an integer array

```python
values = np.array([1, 2, 3])
values[0] = 9.7
print(values)
```

```text
[9 2 3]
```

The decimal part was quietly dropped. The array's type is `int64` and NumPy
does not change the type — it truncates the value.

**The fix:** build the array as decimal from the start.

```python
values = np.array([1, 2, 3], dtype=float)
```

This bites often when you compute an average and write it back: put it into
an `int` array and everything after the point is gone.

## 3. `&` instead of `and`

```python
scores[scores > 50 and scores < 90]
```

```text
ValueError: The truth value of an array with more than one element is
ambiguous.
```

`and` expects a single truth value; what you have is five of them.

**The fix:** `&` and `|`, and with **parentheses**.

```python
scores[(scores > 50) & (scores < 90)]
```

Forgetting the parentheses is a silent mistake too: `&` runs **before** the
comparison and something completely different gets computed.

## 4. A single `nan` ruins everything

```python
scores = np.array([80.0, np.nan, 90.0])
print(scores.mean())
```

```text
nan
```

One missing value turns the whole average into `nan`. This is deliberate: a
total that includes an unknown number is also unknown.

**The fix:** `np.nanmean`, `np.nansum`, `np.nanmax`.

```python
print(np.nanmean(scores))   # 85.0
```

And an oddity: `np.nan == np.nan` is `False`. You cannot look for a missing
value with equality; you need `np.isnan`.

```python
print(np.nan == np.nan)          # False
print(np.isnan(scores).sum())    # 1
```

## 5. `axis` is read backwards

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix.sum(axis=0))
```

Most people expect `axis=0` to mean "add up the rows", but the result is
`[5 7 9]` — the **column** totals.

**A way to remember:** `axis` means "which dimension disappears". `axis=0`
removes the row dimension, leaving one result per column.

If you are unsure, look at `shape`: on a `(2, 3)` array, `axis=0` gives three
elements and `axis=1` gives two.

## 6. `arange` is not reliable with decimals

```python
print(np.arange(0, 1, 0.1).size)
```

```text
10
```

Here it is 10, but depending on the step you can get one element more:
decimals are not stored exactly in binary and the end boundary is missed by a
hair.

**The fix:** when you need a decimal step, use `linspace` — it asks how many
elements you want instead of guessing.

```python
print(np.linspace(0, 1, 11))
```

## 7. `reshape` does not change the number of elements

```python
np.arange(6).reshape(2, 4)
```

```text
ValueError: cannot reshape array of size 6 into shape (2,4)
```

`reshape` rearranges the data, it does not create more. Six elements can be
`(2, 3)` or `(3, 2)`, but not `(2, 4)`.

If you want the column count worked out for you, write `-1`:
`a.reshape(2, -1)`.

## 8. Appending to an array is expensive

```python
values = np.array([1, 2, 3])
values = np.append(values, 4)
```

This works, but every call **rebuilds the array from scratch**. Used inside a
loop, this is where the slowness comes from.

**The fix:** collect into a Python list first and convert once at the end.

```python
collected = []
for x in something:
    collected.append(x)

values = np.array(collected)
```

An array has a fixed size; that is where NumPy's speed comes from.

## 9. `a[0, 2]` rather than `a[0][2]`

Both give the same result, but `a[0][2]` first produces the whole first row
as a separate array and then selects from it. `a[0, 2]` goes straight to the
cell.

On small arrays there is no difference; on large ones and inside loops there
is.

## 10. `argmax` gives the position, not the value

```python
scores = np.array([45, 82, 91, 60])
print(scores.argmax())   # 2
print(scores.max())      # 91
```

`argmax` is "which one", `max` is "how much". You need both: if you keep the
names in another array, `names[scores.argmax()]` gives you the name of the
person with the highest score.
