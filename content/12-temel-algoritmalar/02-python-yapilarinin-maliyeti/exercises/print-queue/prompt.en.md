Jobs arrive at a printer in order. Each round the printer prints **at most
2 pages** of the next job; if the job is not finished, it moves to the
**back** of the queue with its remaining pages.

Write the function `print_order(jobs)`: `jobs` is a list of `[name, pages]`
pairs; the function returns the names **in the order the jobs finish**.

- `[["a", 3], ["b", 1], ["c", 2]]` → `["b", "c", "a"]`
  (a prints 2 pages and moves to the back, b and c finish, a's remaining
  page is printed)

**Rules:** use `collections.deque` for the queue; do not use `pop` or
`insert` on a list (removing from the front of a list is `O(n)`).

**Expected output:**

```
['b', 'c', 'a']
['memo', 'report']
```
