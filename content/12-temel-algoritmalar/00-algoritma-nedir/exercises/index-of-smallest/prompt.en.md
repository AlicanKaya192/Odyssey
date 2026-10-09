Write the function `index_of_smallest(numbers)`: it returns the **position
(index)** of the smallest number in the list.

**Rules:**

- If the smallest appears more than once, return the index of the **first**.
- If the list is empty, return `-1`.
- Do not use `min()` or `.index()`.

**What to do:**

1. Handle the empty list first.
2. Keep the **index**, not the value, of the smallest in mind: `best = 0`.
3. Go through with `for i in range(1, len(numbers)):`; if `numbers[i]` is
   smaller, set `best = i`.

**Expected output:**

```
1
-1
```
