The heart of insertion sort is a single step: placing a new value into a
sorted list by **sliding it into its right place**.

Write the function `insert_sorted(sorted_items, value)`: it appends `value` to
a copy of the sorted list, then, going **from the end towards the start**,
shifts the ones bigger than it one place right to put it in its place, and
returns the new list.

Do not use `insert`, `sorted`, `.sort()` or `bisect`.

**Expected output:**

```
[10, 20, 25, 30, 40]
[5, 10, 20, 30, 40]
[10, 20, 30, 40, 50]
[7]
```
