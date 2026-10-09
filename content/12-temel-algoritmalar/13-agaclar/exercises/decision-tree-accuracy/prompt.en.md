You have a decision tree written as nested dictionaries (`tree`) and five
labelled flowers. Write two functions:

- `predict(node, flower)`: start at the root; if `flower[feature] <=
  threshold` go to `left`, otherwise to `right`. As soon as the node is not
  a dictionary (a leaf), return it.
- `accuracy(tree, flowers, labels)`: predict each flower and return the share
  of correct predictions (`correct / total`).

The program prints each flower's prediction and true label, then the
accuracy.

**Expected output:**

```
setosa setosa
versicolor versicolor
virginica virginica
virginica versicolor
virginica virginica
0.8
```
