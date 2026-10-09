Write the function `middle(head)` **with the tortoise and the hare**: it
returns the **value** of the node in the middle of the list. If the number of
elements is even, take **the second** of the two middles. `None` for an empty
list.

- `[1, 2, 3, 4, 5]` → `3`, `[1, 2, 3, 4]` → `3`

`slow` moves one step, `fast` two; when `fast` reaches the end, `slow` is in
the middle. Do not count the length (no `len`).

**Expected output:**

```
3
3
None
```
