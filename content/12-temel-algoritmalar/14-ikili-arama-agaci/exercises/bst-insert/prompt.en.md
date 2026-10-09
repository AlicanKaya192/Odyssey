Write the function `insert(node, value)` **with recursion**: it adds the
value in the right place by the rule and returns the root of the subtree. A
value already in the tree is **not added**.

`insert_all(values)` inserts the values in order and returns the result of
`inorder`; in a correct BST this is a sorted list without repeats. No `sorted`
and no `sort`: the tree must build the order.

**Expected output:**

```
[1, 3, 4, 6, 7, 8, 10, 13, 14]
[2, 5, 9]
```
