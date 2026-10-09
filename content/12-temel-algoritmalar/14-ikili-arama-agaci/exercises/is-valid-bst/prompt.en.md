Write the function `is_bst(node, low=None, high=None)`: it returns `True` if
the tree is a valid binary search tree. Every node must be in the range
`low < value < high` (`None` means no bound); going left, the upper bound
becomes the node's value, going right, the lower bound. An equal value is
invalid. The empty tree is valid.

Looking only at the children is not enough:

- `[5, [3, 1, 6], 8]` → `False` (6 is left of 5 but larger than 5)
- `[5, [3, 1, 4], 8]` → `True`

Trees are written as nested lists: `[value, left, right]`, a plain value is a
leaf, `None` is empty; `build_tree` is ready.

**Expected output:**

```
False
True
True
```
