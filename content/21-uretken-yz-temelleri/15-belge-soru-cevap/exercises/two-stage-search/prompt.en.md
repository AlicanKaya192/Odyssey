The read-only `retrieval.py` holds the lesson's `Index`, `by_article` and
`by_sentence`. `two_stage(question)` should find the most relevant article
with the article-level search (`Index(by_article()).search(question, 1)`) and
return only that article's sentences from `by_sentence()`, in their order, as
a list of texts.

**Expected output:**

```
Gift cards are available for
They cannot be exchanged for
You can use one gift
```
