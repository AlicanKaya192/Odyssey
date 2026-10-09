Write the function `tree_predict(tree, X)`: the tree is a nested dictionary;
an inner node is `{"feature", "threshold", "left", "right"}`, a leaf `{"leaf"}`.
For each row start at the root: left if `x[feature] <= threshold`, otherwise
right; take the value at the leaf. Return the list of labels.

**Expected output:**

```
[0, 1, 0]
```
