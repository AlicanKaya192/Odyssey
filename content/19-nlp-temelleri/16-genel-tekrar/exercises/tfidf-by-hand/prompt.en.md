`tfidf_weights(docs, word)` should return the TF-IDF weight of `word` for each
document (a token list) (3 places, no normalisation):

- TF: how many times the word appears in the document
- IDF: `ln((1 + n) / (1 + df)) + 1`; `n` is the number of documents, `df` the
  number of documents containing the word (scikit-learn's default)

**Expected output:**

```
[2.575, 0.0, 1.288]
[1.288, 1.288, 0.0]
```
