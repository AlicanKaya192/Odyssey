`attention(query, keys, values)` should do the lesson's scaled dot-product
attention: scores `keys @ query / √d` (`d` is the query's length), weights by
softmax, the result the weighted average of the values. Return the result as
a list with 2 places.

**Expected output:**

```
[22.17]
[20.0]
```
