Let every word (row) of a sentence attend to all the words. `self_attention(X)`
should return the weight table: scores `X @ X.T / √d` (`d` is the number of
columns), a separate softmax on each row, 3 places, a list of lists.

**Expected output:**

```
[0.401, 0.198, 0.401]
[0.198, 0.401, 0.401]
[0.248, 0.248, 0.503]
```
