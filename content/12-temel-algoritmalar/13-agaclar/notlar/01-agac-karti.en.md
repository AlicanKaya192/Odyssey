## Terms

| Term | Meaning |
|---|---|
| Root | The top node, with no parent |
| Leaf | A node with no children |
| Subtree | A node and everything below it |
| Depth | A node's distance from the root; the root is 0 |
| Height | The number of nodes on the longest root-to-leaf path |
| Binary tree | Every node has at most two children (left, right) |

## Walking orders

The tree from the lesson: root `1`; the children of `2` are `4`, `5`; the
right child of `3` is `6`.

| Order | Rule | Result | What for |
|---|---|---|---|
| Preorder | root, left, right | `1 2 4 5 3 6` | copying, printing the structure |
| Inorder | left, root, right | `4 2 5 1 3 6` | sorted values in a search tree |
| Postorder | left, right, root | `4 5 2 6 3 1` | when the children's answers come first |
| Level (BFS) | floor by floor with a queue | `[1] [2, 3] [4, 5, 6]` | shortest path, level-wise work |

## Two skeletons

Recursive (most questions):

```python
def solve(node):
    if node is None:
        return ANSWER_FOR_EMPTY_TREE
    left = solve(node.left)
    right = solve(node.right)
    return COMBINE(node.value, left, right)
```

Level by level:

```python
queue = deque([root])
while queue:
    for _ in range(len(queue)):
        node = queue.popleft()
        ...                                # a node on this level
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

## Costs

| Job | Time | Extra memory |
|---|---|---|
| Walking all nodes (DFS or BFS) | `O(n)` | DFS `O(h)`, BFS `O(width)` |
| Walking from the root to one leaf | `O(h)` | `O(1)` |
| `h` in a balanced tree | `≈ log₂ n` | |
| `h` in a chain-shaped tree | `n` | |

## Common mistakes

- Forgetting the base case (`if node is None`) → reaching `.left` of `None`
  and getting `AttributeError`.
- Defining a leaf wrongly: a leaf is a node whose `left` **and** `right` are
  `None`; a node with only one of them `None` is not a leaf.
- To separate a level in BFS, `len(queue)` must be taken **before** the loop
  starts; `range(len(queue))` does this by itself, checking `len(queue)` at
  every step inside a `while` does not.
- In a very deep (chain-like) tree recursion raises `RecursionError`; then use
  the stack or queue version.
