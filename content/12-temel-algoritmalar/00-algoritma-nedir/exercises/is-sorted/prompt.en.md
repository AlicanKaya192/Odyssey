Write the function `is_sorted(numbers)`: it returns `True` if the list is
sorted from smallest to largest and `False` otherwise. Equal neighbours count
as sorted (`[1, 2, 2, 3]` is sorted).

**Rules:**

- Do not use `sorted()` or `.sort()`.
- An empty list and a one-element list count as sorted.

**The idea:** in a sorted list no element can be **bigger than its right-hand
neighbour**. Seeing a single violation is enough to say `False`; you can
return at once.

**Expected output:**

```
True
False
True
```
