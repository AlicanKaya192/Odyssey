Write the function `count_leaves(node)`: it returns the number of **leaves**
in the tree. A leaf is a node whose left **and** right children are `None`.
`0` for an empty tree.

A node with one child is not a leaf: in the chain
`[1, [2, [3, None, 4], None], None]` only `4` is a leaf.

Trees are written as nested lists: `[value, left, right]`, a plain value
is a leaf, `None` is empty. `build_tree` turns this into `TreeNode`s; `TREE`
is the lesson's tree (`[1, [2, 4, 5], [3, None, 6]]`).

**Expected output:**

```
3
1
0
```
