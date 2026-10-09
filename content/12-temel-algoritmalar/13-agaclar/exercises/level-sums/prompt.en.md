Write the function `level_sums(root)` **with a queue (BFS)**: it returns the
sum of the values on each level, starting from the root, as a list. `[]` for
an empty tree.

- The lesson's tree: levels `[1]`, `[2, 3]`, `[4, 5, 6]` → `[1, 5, 15]`

Use `collections.deque` and the `for _ in range(len(queue))` pattern.

Trees are written as nested lists: `[value, left, right]`, a plain value
is a leaf, `None` is empty. `build_tree` turns this into `TreeNode`s; `TREE`
is the lesson's tree (`[1, [2, 4, 5], [3, None, 6]]`).

**Expected output:**

```
[1, 5, 15]
[]
```
