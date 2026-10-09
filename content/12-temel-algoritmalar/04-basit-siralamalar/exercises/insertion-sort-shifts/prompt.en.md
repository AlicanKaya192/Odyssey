Write the function `insertion_sort(items)`: it returns a sorted copy of the
list and the number of **shifts** made, as a tuple:
`(sorted_list, shifts)`.

One shift = the line `items[j + 1] = items[j]` running once. This number
equals the list's **inversion count** (the number of pairs in the wrong
order): 0 for a sorted list, `n(n−1)/2` for a reversed one.

Do not use `sorted` or `.sort()`.

**Expected output:**

```
([5, 6, 11, 12, 13], 7)
([1, 2, 3, 4], 0)
([1, 2, 3, 4], 6)
```
