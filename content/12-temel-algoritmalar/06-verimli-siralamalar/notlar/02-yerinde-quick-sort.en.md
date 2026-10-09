The quick sort in the lesson built new lists at every level. Real
implementations do the splitting **inside** the list, by swapping elements.
The easiest method to follow is the **Lomuto partition**:

```python
import random

def partition(items, lo, hi):
    pivot_index = random.randint(lo, hi)              # a random pivot
    items[pivot_index], items[hi] = items[hi], items[pivot_index]
    pivot = items[hi]
    boundary = lo                                      # left of it: smaller than the pivot
    for i in range(lo, hi):
        if items[i] < pivot:
            items[i], items[boundary] = items[boundary], items[i]
            boundary += 1
    items[boundary], items[hi] = items[hi], items[boundary]
    return boundary                                    # the pivot's final place

def quick_sort_in_place(items, lo=0, hi=None):
    if hi is None:
        hi = len(items) - 1
    if lo < hi:
        p = partition(items, lo, hi)
        quick_sort_in_place(items, lo, p - 1)
        quick_sort_in_place(items, p + 1, hi)

data = [9, 4, 7, 1, 8, 2]
quick_sort_in_place(data)
print(data)            # [1, 2, 4, 7, 8, 9]
```

## How does the partition work?

`boundary` is a line: every element to its left is **smaller** than the
pivot. `i` walks the list from left to right; when it finds an element
smaller than the pivot, it moves it just right of the line and advances the
line by one. When the walk ends, the pivot (waiting at the end) is put where
the line is: smaller ones on its left, larger or equal ones on its right.

No extra list; only the recursion stack is used (`O(log n)` on average).
Thanks to the random pivot, sorted input is fast too and does not hit the
depth limit.

## Stability

Long-distance swaps can break the order of equal elements: in-place quick
sort is not stable. If stability is needed, merge sort or Python's
`sorted`.
