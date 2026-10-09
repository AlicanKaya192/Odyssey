## Rules and indexes

- Shape: a binary tree filled level by level, left to right, without gaps.
- Order (min-heap): parent ≤ child. The smallest is at `heap[0]`.
- The children of `i` are `2i + 1`, `2i + 2`; its parent is `(i - 1) // 2`.

## `heapq` functions

| Function | What it does | Time |
|---|---|---|
| `heappush(h, x)` | add | `O(log n)` |
| `heappop(h)` | take the smallest | `O(log n)` |
| `h[0]` | look at the smallest (without taking) | `O(1)` |
| `heapify(list)` | turn the list into a heap in place | `O(n)` |
| `heapreplace(h, x)` | take first, then add | `O(log n)` |
| `heappushpop(h, x)` | add first, then take | `O(log n)` |
| `nlargest(k, it)` / `nsmallest(k, it)` | the largest / smallest `k` | `O(n log k)` |
| `merge(*sorted_lists)` | merge sorted lists lazily | `O(n log k)` in total |
| `heapify_max`, `heappush_max`, `heappop_max` | max-heap (Python 3.14) | the same |

## Which one when?

| Need | Choose |
|---|---|
| Always take the smallest/largest, adding in between | a heap |
| Sort once, then read | `sorted` |
| A few of the largest/smallest (`k` small) | `nlargest` / `nsmallest` or a heap of size `k` |
| The single largest/smallest | `max` / `min` |
| Deleting from the middle, range queries | a BST or a sorted list + `bisect` |

## Common mistakes

- **Thinking the heap list is sorted:** `heap[1]` **may not** be the second
  smallest (in `[1, 3, 2, ...]` the second smallest, `2`, is at `heap[2]`).
- **Changing the list by hand:** `heap.append(x)` or `heap[3] = 0` breaks the
  rule; change it only with the `heapq` functions.
- **`heappop` without `heapify`:** `heappop` from an ordinary list gives the
  wrong element.
- **Ties in tuples:** in `(priority, value)`, if the priorities are equal the
  values are compared; if they cannot be compared, `TypeError`. Write
  `(priority, counter, value)`.
- **Forgetting the minus for a max-heap:** if you put `-x` in, turn it back
  with `-` when you take it.
