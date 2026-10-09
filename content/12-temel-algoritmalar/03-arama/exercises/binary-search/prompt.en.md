Write the function `binary_search(items, target)`: it finds `target` in a
sorted list with binary search and returns its index; `-1` if missing.

**Rules:** do not use `.index()`, scanning with `in` or `bisect`; throw away
half the region every round.

The check will try your function with **every** value in the list, with
values not in it (below the smallest, above the largest, between two), and
with an empty and a one-element list.

**Expected output:**

```
4
0
-1
```
