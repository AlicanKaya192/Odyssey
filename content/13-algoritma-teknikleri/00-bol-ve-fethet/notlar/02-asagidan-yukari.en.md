Divide and conquer is usually written top-down with recursion: split the big
problem, split, split. You can also do the same work **bottom-up**: start from
the smallest pieces and climb up by merging them two at a time. No recursion,
no call stack.

## Bottom-up merge sort

```python
def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]

def merge_sort_bottom_up(values):
    runs = [[x] for x in values]          # every element is sorted on its own
    while len(runs) > 1:
        runs = [merge(runs[k], runs[k + 1]) if k + 1 < len(runs) else runs[k]
                for k in range(0, len(runs), 2)]
        print(runs)
    return runs[0] if runs else []

merge_sort_bottom_up([5, 2, 8, 1, 9, 3])
```

```text
[[2, 5], [1, 8], [3, 9]]
[[1, 2, 5, 8], [3, 9]]
[[1, 2, 3, 5, 8, 9]]
```

Each round is one level: six single-element pieces → three pairs → two
pieces → one list. The number of rounds is `⌈log₂ n⌉`, each round `n` work:
still `O(n log n)`.

## When is it preferred?

- **When the recursion depth would be a problem.** Merge sort, which halves,
  is only `log n` deep (20 for a million elements), but not every
  divide-and-conquer is that shallow.
- **When the data already comes in pieces.** Python's Timsort finds the
  ready sorted pieces (runs) in the list and merges them bottom-up; that is
  why it is very fast on nearly sorted data.
- **On data that does not fit in memory.** Sorting a file piece by piece,
  writing the pieces to disk and then merging them (external sort) is the
  same bottom-up thinking; `heapq.merge` from the Core Algorithms module did this last step.
