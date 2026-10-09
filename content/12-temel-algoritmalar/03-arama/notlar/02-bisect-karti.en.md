The `bisect` module is a ready-made binary search on a sorted list. The list
**must be sorted**; if it is not, you get no error, just a wrong answer.

## Functions

| Function | Returns / does | Cost |
|---|---|---|
| `bisect_left(a, x)` | the leftmost index where `x` could go | `O(log n)` |
| `bisect_right(a, x)` (= `bisect`) | the rightmost index where `x` could go | `O(log n)` |
| `insort_left(a, x)`, `insort(a, x)` | inserts `x` without breaking the order | place `O(log n)`, insertion `O(n)` |

All of them take `lo`, `hi` (to limit the search to a range) and `key=` (since
Python 3.10).

## Common uses

```python
import bisect

a = [10, 20, 20, 20, 30, 40]

# Is x in the list?
i = bisect.bisect_left(a, 20)
found = i < len(a) and a[i] == 20              # True

# How many times does x occur?
count = bisect.bisect_right(a, 20) - bisect.bisect_left(a, 20)   # 3

# How many values are in [low, high]?
in_range = bisect.bisect_right(a, 35) - bisect.bisect_left(a, 15)   # 4

# The first value above x
j = bisect.bisect_right(a, 25)
first_above = a[j] if j < len(a) else None      # 30
```

## Classifying by thresholds

Putting grade boundaries in a sorted list of thresholds and taking the letter
by index is shorter than a long `if/elif` chain:

```python
def letter(score):
    limits = [50, 60, 70, 85]          # from these thresholds on, one letter up
    letters = ["F", "D", "C", "B", "A"]
    return letters[bisect.bisect_right(limits, score)]

print(letter(49), letter(50), letter(84), letter(85))   # F D B A
```

Whether you use `bisect_right` or `bisect_left` decides which side a
threshold value falls on: 50 points is D with `bisect_right` (the threshold
belongs to the upper band) and would be F with `bisect_left`.

## Keeping a sorted list alive

For a list that keeps receiving elements and is often asked "how many are
smaller than x?", `insort` + `bisect` make a good pair. Since insertion is
`O(n)` it slows down over millions of insertions; at that point priority
queues or tree structures (later sections) come in.
