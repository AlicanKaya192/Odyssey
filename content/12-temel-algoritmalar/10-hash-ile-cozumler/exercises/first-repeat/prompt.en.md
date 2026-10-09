Write the function `first_repeat(items)`: walking the list from left to
right, it returns the first element **seen before**; `None` if there is no
repeat.

- `[4, 2, 7, 2, 4]` → `2` (4 repeats too, but 2's second sighting comes first)

Keep the seen elements in a **set**. At the end of the code there is a list of
300 000 elements with the repeat at the end; the time limit is 10 seconds.

**Expected output:**

```
2
None
123
```
