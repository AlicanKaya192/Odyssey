Write the function `merge_sort(items)` **recursively**: it returns a sorted
copy of the list. The merge function (`merge`) is ready.

1. Base case: a list of 0 or 1 elements is already sorted.
2. Split in the middle: `items[:mid]` and `items[mid:]`.
3. Sort each half with `merge_sort` and combine them with `merge`.

Do not use `sorted` or `.sort()`.

**Expected output:**

```
[3, 9, 10, 27, 38, 43, 82]
[]
```
