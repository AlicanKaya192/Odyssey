Write the function `k_smallest(values, k)`: it returns the smallest `k`
elements of the list as a list **from smallest to largest**. If `k` is larger
than the number of elements, it returns all of them.

The way: turn a **copy** of the list into a heap with `heapq.heapify`, then
`heapq.heappop` `k` times. The original list must not change. No `sorted`,
`sort`, `nsmallest`.

**Expected output:**

```
[1, 2, 4]
[1, 2, 4, 7, 8, 9]
[7, 2, 9, 4, 1, 8]
```
