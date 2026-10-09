Write the function `majority(y_train, n)`: it returns a list repeating the
most frequent training label `n` times (the baseline). On a tie the **smaller**
label is chosen.

Hint: `np.bincount` gives the count of each label, `np.argmax` the first
position of the largest.

**Expected output:**

```
[1, 1, 1, 1]
[3, 3]
```
