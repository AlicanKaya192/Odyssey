Write the function `merge_sorted(lists)` **with a heap**: it merges lists,
each sorted from smallest to largest, into one sorted list.

1. Put the first element of each non-empty list in the heap as `(value,
   list_number, index)`.
2. Take the smallest, add it to the result; if that list has a **next**
   element, put it in the heap.
3. When the heap is empty, you are done.

No `sorted`, `sort` and no `heapq.merge`.

**Expected output:**

```
[1, 2, 3, 4, 5, 9, 10]
[1, 1, 7]
```
