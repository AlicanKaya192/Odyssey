IDF is a **statistic**: it is learned by looking at all the documents. Like a
scaler's mean, it should be learned from the training data only. What
happens if we `fit` on all the data?

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
train, test = texts[:1000], texts[1000:]
right = TfidfVectorizer().fit(train)
leaky = TfidfVectorizer().fit(texts)
print(len(right.vocabulary_), len(leaky.vocabulary_))


def idf_of(vectorizer, word):
    return round(float(vectorizer.idf_[vectorizer.vocabulary_[word]]), 3)


print(idf_of(right, "bluetooth"), idf_of(leaky, "bluetooth"))
```

```text
288 350
4.382 4.524
```

- The right way (training only) built a vocabulary of 288 words. The leaky
  way has 350: **62 words** that are in the test data but were never seen in
  training entered the model as columns.
- The IDF of "bluetooth" changed too (4.382 → 4.524): the test documents
  joined the df.

## Why does it matter?

The test data imitates new data the model has never seen. If the vocabulary
or the IDF learns something from the test data, the test score comes out
more optimistic than what you will really see. The gap may look small here;
but when a word appears only in the test data and gives the class away (a
product name, an error code), the effect is large.

## The right order

```text
vectorizer.fit(train)              # training only
X_train = vectorizer.transform(train)
X_test = vectorizer.transform(test)
```

Or use a **Pipeline** that does all of it right by itself; the topic of
section 10. Refitting the vectoriser in every fold of cross-validation is
easy only with a Pipeline too.
