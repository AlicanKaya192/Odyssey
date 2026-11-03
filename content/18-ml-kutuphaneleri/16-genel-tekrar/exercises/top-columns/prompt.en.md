`top_columns(k)` should return the names of the `k` most important columns by
permutation importance for the trained pipeline. The importance must be
computed **on the test data**; the starter code gives the training data, and
the boosting model shows `monthly`, which it memorised in training, as the
most important column.

**Expected output:**

```
['tenure', 'support']
```
