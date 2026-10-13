`top_confusions(y_true, y_pred, k)` should count the wrong predictions by
`(true, predicted)` pair and return the `k` most common as
`[true, predicted, count]`. Order: count from largest; on ties, the pair in
alphabetical order.

**Expected output:**

```
[['c', 'b', 2], ['a', 'b', 1]]
```
