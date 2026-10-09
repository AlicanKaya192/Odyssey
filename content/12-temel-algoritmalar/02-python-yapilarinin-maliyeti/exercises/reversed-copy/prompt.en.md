Write the function `reversed_copy(items)`: it returns **a copy of the list
in reverse order**; the original list must not change.

The first idea is to add every element at the front of a new list
(`insert(0, x)`), but that shifts the whole list on every addition: `O(n²)`.
Instead go through the list **from the end to the start** and add with
`append`: `O(n)`.

**Rules:** do not use `insert`, `reverse`, `reversed` or `[::-1]`.

**Expected output:**

```
[4, 3, 2, 1]
[1, 2, 3, 4]
[]
```
