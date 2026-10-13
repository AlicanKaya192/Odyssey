`count_vector(doc, vocab)` should split the document (lowercased) with
`split()` and return, in `vocab` order, how many times each word of `vocab`
appears in the document. Words not in the vocabulary are not counted.

**Expected output:**

```
[1, 0, 2, 1, 1]
[0, 0, 0, 0, 0]
```
