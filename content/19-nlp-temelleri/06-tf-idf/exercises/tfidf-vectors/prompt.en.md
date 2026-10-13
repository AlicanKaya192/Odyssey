`tfidf_vectors(docs)` should do the lesson's calculation: the vocabulary sorted
alphabetically; each word's IDF is `ln((1 + n) / (1 + df)) + 1`; count ×
IDF in each document; then bring the row to unit length with L2 and round to
3 places. The starter code only returns the counts.

**Expected output:**

```
[0.577, 0.577, 0.577, 0.0]
[0.707, 0.707, 0.0, 0.0]
[0.0, 0.0, 0.836, 0.549]
```
