`zero_shot(doc_vectors, label_vectors, names)` should assign each document
vector to the label vector with the largest dot product and return that
label's name (the first one on ties).

**Expected output:**

```
['shipping', 'account', 'shipping']
```
