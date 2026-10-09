`push` (sift up) is ready. Write the function `pop(heap)` **without `heapq`**:
it removes and returns the smallest, leaving the rest of the list a heap.

1. Remove the last element from the list (`heap.pop()`). If the list is now
   empty, return it.
2. Keep the root and write that last element in its place.
3. Start at `i = 0`: find the **smaller** of the children `2i + 1` and
   `2i + 2` (if they exist). If it is smaller than `heap[i]`, swap and move
   down there; otherwise stop.
4. Return the kept root.

`pop_all(values)` adds them all with `push` and takes them out in order with
`pop`.

**Expected output:**

```
[1, 2, 3, 5, 8, 9]
[1, 4, 4, 7]
```
