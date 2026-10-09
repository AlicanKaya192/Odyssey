Write the function `paths(root)`: it returns the path from the root to each
leaf as a string like `"1->2->4"`, in a list ordered **left to right**. `[]`
for an empty tree.

- The lesson's tree → `["1->2->4", "1->2->5", "1->3->6"]`

Hint: a helper function goes down carrying the path so far (`prefix`); when
it reaches a leaf it adds the path to the list.

Trees are written as nested lists: `[value, left, right]`, a plain value
is a leaf, `None` is empty. `build_tree` turns this into `TreeNode`s; `TREE`
is the lesson's tree (`[1, [2, 4, 5], [3, None, 6]]`).

**Expected output:**

```
1->2->4
1->2->5
1->3->6
[]
```
