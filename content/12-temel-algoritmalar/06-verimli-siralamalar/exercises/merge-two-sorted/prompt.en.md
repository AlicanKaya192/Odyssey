Write the function `merge(left, right)`: it merges two **sorted** lists into
one sorted list.

Put an index (`i`, `j`) at the start of each list; add the smaller one to the
result and move that index on. When one list runs out, add the rest of the
other. On ties take the **left** one first (`<=`).

Do not use `sorted` or `.sort()`: joining the lists and sorting is
`O(n log n)`, merging is `O(n)`.

**Expected output:**

```
[1, 2, 3, 4, 9, 10, 12]
[5, 6]
```
