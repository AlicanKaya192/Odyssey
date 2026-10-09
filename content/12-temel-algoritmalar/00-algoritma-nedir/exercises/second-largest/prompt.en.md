Write the function `second_largest(numbers)`: it returns **the largest value
that is smaller than the largest**. If there is no such value, it returns
`None`.

**Examples:**

- `[4, 9, 7, 9]` → `7` (there are two 9s; the second largest **distinct**
  value is 7)
- `[5, 5]` → `None` (no value is smaller than the largest)
- `[3]` and `[]` → `None`

**Rules:** do not use `sorted()`, `.sort()` or `max()`. Going through the
list **once** is enough.

**The idea:** keep two values through the loop: `first` (the largest so far)
and `second` (the largest of those smaller than it). Start both at `None`.
When a new number is bigger than `first`, the old `first` becomes `second`.

**Expected output:**

```
7
None
-5
```
