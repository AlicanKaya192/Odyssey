Build `pipe` as a two-step Pipeline: `TfidfVectorizer()` named `"tfidf"` and
`LogisticRegression(max_iter=1000)` named `"model"`. Train it on all the
reviews. `predict_labels(sentences)` should take a list of raw sentences and
return the predictions as a plain list.

**Expected output:**

```
['positive', 'negative']
```
