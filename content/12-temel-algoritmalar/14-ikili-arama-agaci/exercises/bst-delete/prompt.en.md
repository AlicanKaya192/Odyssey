Write the function `delete(node, value)`: it deletes the value from the tree
and returns the root of the subtree. If the value is missing, the tree does
not change. Three cases:

- a leaf: remove it
- one child: the child takes its place
- two children: **the smallest of the right subtree** is written in its
  place, then that value is deleted from the right subtree (`minimum` is
  ready)

`after(values, removed)` builds the tree, deletes the values and returns the
result of `inorder` and the root.

**Expected output:**

```
[[1, 4, 6, 8, 10, 13], 8]
[[1, 3, 6, 10, 14], 10]
[[], None]
```
