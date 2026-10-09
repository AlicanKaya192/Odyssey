Write the function `unique_in_order(items)`: it removes repeats from the
list, keeping **the order in which each value first appears**.

- `[3, 1, 3, 2, 1]` → `[3, 1, 2]`
- `[]` → `[]`

**Speed requirement:** at the end of the code a list of 100 000 elements is
deduplicated, and the exercise has 10 seconds. If you ask the "seen it?"
question of a **list**, it becomes `O(n²)` and the time runs out; keep a
**set**.

**Expected output:**

```
[3, 1, 2]
50000
```
