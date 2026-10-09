Write the function `bubble_sort(items)`: it returns **a sorted copy** of the
list using bubble sort; the original list must not change.

**What to do:**

1. Take a copy with `items = items[:]`.
2. In each pass compare neighbouring pairs and swap them if they are in the
   wrong order.
3. If a pass made no swap, leave early.

Do not use `sorted` or `.sort()`.

**Expected output:**

```
[1, 2, 4, 5, 8]
[5, 1, 4, 2, 8]
[]
```
