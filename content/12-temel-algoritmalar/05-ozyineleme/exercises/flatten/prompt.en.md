Write the function `flatten(items)` **recursively**: it returns every number
in a list, however deeply nested, **in order from left to right** in a flat
list.

- `flatten([1, [2, 3], [4, [5, [6]]]])` → `[1, 2, 3, 4, 5, 6]`
- `flatten([[], [[]]])` → `[]`

You may use `for` to go over the elements; but for sublists the function
**must call itself**. `isinstance(item, list)` tells whether a value is a
list.

**Expected output:**

```
[1, 2, 3, 4, 5, 6]
[]
```
