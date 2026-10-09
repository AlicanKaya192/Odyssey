Write the function `first_repeat(items)`: reading the list from the start, it
returns the **first** value seen **a second time**; `None` if there is no
repeat.

- `[3, 1, 4, 1, 5, 3]` → `1` (3 started earlier, but 1's second came first)

The large input on the last line makes an `O(n²)` solution hit the time limit; `O(n)` is needed. No `count` and no `index`.

**Expected output:**

```
1
None
199999
```
