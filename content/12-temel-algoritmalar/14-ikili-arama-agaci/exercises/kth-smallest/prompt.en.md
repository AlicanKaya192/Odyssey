Write the function `kth_smallest(root, k)`: it returns the `k`-th smallest
value in the tree (`k = 1` is the smallest). `None` if `k` is larger than the
number of values in the tree.

The inorder walk already gives the values sorted; no `sorted`, `sort`, `min`.

`VALUES` is the insertion order of the lesson's tree; `build_bst(values)` builds the tree with the ready `insert`.

**Expected output:**

```
1 1
3 4
9 14
10 None
```
