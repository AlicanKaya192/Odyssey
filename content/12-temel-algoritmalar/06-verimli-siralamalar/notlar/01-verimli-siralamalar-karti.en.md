## Comparison

| | Merge sort | Quick sort | Timsort (`sorted`) |
|---|---|---|---|
| Idea | split, sort both halves, merge | split around a pivot, sort both sides | find runs, fix small ones with insertion, merge |
| Best | `O(n log n)` | `O(n log n)` | `O(n)` (sorted data) |
| Average | `O(n log n)` | `O(n log n)` | `O(n log n)` |
| Worst | `O(n log n)` | `O(n²)` (bad pivot) | `O(n log n)` |
| Extra memory | `O(n)` | `O(log n)` (stack) in the in-place version | `O(n)` |
| Stable? | yes | usually not | yes |

## Merging is useful on its own

Merging two sorted lists is `O(n + m)`; it turns up outside sorting too:

- Putting two sorted files (log records, transactions) into one order
- Sorting data that does not fit in memory (**external sorting**): sort the
  pieces separately, write them to disk, then merge the pieces
- `heapq.merge(*lists)`: Python's ready-made multi-way merge

## Choosing the pivot

| Choice | On sorted input | Note |
|---|---|---|
| First or last element | `O(n²)`, deep recursion | do not use |
| A random element | expected `O(n log n)` | simple and safe |
| Median of three (first, middle, last) | `O(n log n)` | makes bad inputs hard to produce |

## Which one when?

- In Python: **always `sorted` / `list.sort`.**
- If stability is required and memory is no problem: merge sort.
- Little memory, average speed matters: in-place quick sort (most C
  libraries use a variant of it).
- The data does not fit in memory: sort in pieces + merge (the same idea as
  chunked reading in the Big Data path).
