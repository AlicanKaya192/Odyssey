Write the function `top_k(stream, k)` with **a min-heap of size at most `k`**:
it returns the largest `k` values **from largest to smallest**.

- If the heap has fewer than `k` elements, add the new number.
- If it is full and the new number is larger than the root (`heap[0]`), put
  it in the root's place with `heapq.heapreplace`.
- At the end, emptying the heap with `heappop` gives the values from smallest
  to largest; reverse them.

No `sorted`, `sort`, `nlargest`. `[]` for `k <= 0`.

**Expected output:**

```
[9, 8, 7]
[5, 5]
```
