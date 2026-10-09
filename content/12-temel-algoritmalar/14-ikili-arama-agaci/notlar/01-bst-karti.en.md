## The rule

At every node: the **whole** left subtree is smaller, the **whole** right
subtree is larger. The inorder walk gives the values sorted.

## Costs

| Operation | Balanced BST | Chain-shaped BST | Sorted list + `bisect` | Dictionary / set |
|---|---|---|---|---|
| Search | `O(log n)` | `O(n)` | `O(log n)` | `O(1)` |
| Insert | `O(log n)` | `O(n)` | `O(n)` (shifting) | `O(1)` |
| Delete | `O(log n)` | `O(n)` | `O(n)` | `O(1)` |
| Smallest / largest | `O(log n)` | `O(n)` | `O(1)` | `O(n)` |
| Walking in order | `O(n)` | `O(n)` | `O(n)` | `O(n log n)` (needs sorting) |

If order is not needed, dictionaries and sets are always faster. The BST's job
is to be changeable **while keeping the order**.

## The three cases of deletion

| Case | What is done |
|---|---|
| Leaf | It is removed |
| One child | The child takes its place |
| Two children | The smallest of the right subtree (the next value) is written in its place, then that value is deleted from the right subtree |

Instead of the next value, **the previous value** (the largest of the left
subtree) can be used too; both keep the rule.

## Common mistakes

- **Looking only at the children:** even if `left < node < right` holds at
  every node, the tree may not be a BST. In the tree `[5, [3, 1, 6], 8]`, `6`
  is in the right place to the right of `3`, but it is in the **left**
  subtree of `5` and larger than `5`. Validation is done by carrying the
  allowed **range** (a lower and an upper bound) to each node.
- **Forgetting equal values:** decide up front what happens to an equal value
  on insert (ignore it, count it or always put it to the right).
- **Not linking the return value in a recursive insert:** if you write
  `insert(node.left, value)` without `node.left = ...`, the new node is never
  attached to the tree.
- **Inserting sorted data:** the tree turns into a chain. Shuffle the data or
  use a balanced structure.
