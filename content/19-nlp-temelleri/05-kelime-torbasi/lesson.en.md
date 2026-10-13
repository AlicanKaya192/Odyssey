# Bag of Words

A model wants a table of numbers: each row an example, each column a
feature. The oldest and still most widely used way to turn text into such a
table is the **bag of words**: every document becomes a row that counts how
many times each word of the vocabulary appears in it. The order is
forgotten; only a bag full of words is left. This section builds a bag of
words first by hand, then with scikit-learn's `CountVectorizer`, shows what
happens to words never seen in training and uses the bag itself to find
which words point to which class.

## A bag of words by hand

```python
docs = ["the battery is great", "the battery died", "great price great sound"]
vocab = sorted({w for d in docs for w in d.split()})
print(vocab)
for d in docs:
    words = d.split()
    print([words.count(w) for w in vocab])
```

```text
['battery', 'died', 'great', 'is', 'price', 'sound', 'the']
[1, 0, 1, 1, 0, 0, 1]
[1, 1, 0, 0, 0, 0, 1]
[0, 0, 2, 0, 1, 1, 0]
```

- The **vocabulary** is the sorted list of distinct words across all
  documents: 7 words. Each word is a column.
- Each document is a row of 7 numbers: in the row of "great price great
  sound" the "great" column is 2, "price" and "sound" 1, the rest 0.
- All the rows have the same length. The texts have different lengths, yet
  the table is regular: that is exactly what a model needs.

## CountVectorizer

scikit-learn does the same job together with splitting, lowercasing and a
sparse matrix:

```python
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)
print(vectorizer.get_feature_names_out().tolist())
print(X.toarray().tolist())
print(vectorizer.vocabulary_["great"], X.shape)
```

```text
['battery', 'died', 'great', 'is', 'price', 'sound', 'the']
[[1, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 0, 0, 1], [0, 0, 2, 0, 1, 1, 0]]
2 (3, 7)
```

- `fit` learns the vocabulary, `transform` counts the documents;
  `fit_transform` does both. Like every scikit-learn transformer.
- `get_feature_names_out()` gives the column names, `vocabulary_` a
  dictionary from word to column number: "great" is column 2 (counting from
  zero).
- `X` is a sparse matrix (the note of section 04); in a small example we can
  look at it with `toarray()`, but do not do that on big data.

## A word not in the vocabulary

The vectoriser has been `fit` once; what if a new text brings words it has
**never seen**?

```python
new = vectorizer.transform(["the camera is great but the zoom died"])
print(new.toarray().tolist())
analyze = vectorizer.build_analyzer()
tokens = analyze("the camera is great but the zoom died")
print([w for w in tokens if w in vectorizer.vocabulary_])
```

```text
[[0, 1, 1, 1, 0, 0, 2]]
['the', 'is', 'great', 'the', 'died']
```

"camera", "but" and "zoom" are not in the vocabulary; **they were dropped
without any warning**. They are called **out-of-vocabulary** (OOV) words.
The model can never see a new product's name, a new error or new slang.
Always `fit` the vocabulary **on the training data only** and apply only
`transform` to the test data; fitting on all the data leaks the test data's
words into training (the same data leakage as in ML Libraries).

## The bag does not know order

```python
pair = ["the battery is great", "great is the battery"]
a, b = vectorizer.transform(pair).toarray()
print(a.tolist(), b.tolist(), (a == b).all())
```

```text
[1, 0, 1, 1, 0, 0, 1] [1, 0, 1, 1, 0, 0, 1] True
```

The two sentences have exactly the same vector. "dog bites man" and "man
bites dog" end up in the same bag too. For most classification tasks this
loss matters surprisingly little: whether a review is positive or negative
is usually clear from which words appear. If order matters, you need the
n-grams of section 04 or the sequence models of the second module.

## Counts or presence?

```python
text = ["great great great price"]
counts = CountVectorizer().fit_transform(text).toarray()
flags = CountVectorizer(binary=True).fit_transform(text).toarray()
print(counts.tolist(), flags.tolist())
```

```text
[[3, 1]] [[1, 1]]
```

`binary=True` writes only present (1) or absent (0) instead of a count. In
short texts (reviews, tweets, titles) a word appearing three times often
carries no more information than appearing once; a binary bag can work
better. Which one is better is measured on validation data.

## Which words point to which class?

The bag of words is not only input for a model; it is an inspection tool on
its own. Let us compare each word's share in negative reviews with its share
in positive reviews:

```python
import numpy as np
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
words = vectorizer.get_feature_names_out()
pos = np.asarray(X[labels == "positive"].sum(axis=0)).ravel() + 1
neg = np.asarray(X[labels == "negative"].sum(axis=0)).ravel() + 1
log_ratio = np.log((neg / neg.sum()) / (pos / pos.sum()))
for i in np.argsort(log_ratio)[::-1][:6]:
    print(words[i], int(neg[i] - 1), int(pos[i] - 1), round(log_ratio[i], 2))
print("---")
for i in np.argsort(log_ratio)[:4]:
    print(words[i], int(neg[i] - 1), int(pos[i] - 1), round(log_ratio[i], 2))
```

```text
terrible 15 0 3.91
hate 73 13 2.8
worse 71 13 2.78
honest 42 8 2.7
box 63 13 2.66
damaged 63 13 2.66
---
works 3 207 -2.81
expected 2 147 -2.76
well 8 426 -2.72
too 4 231 -2.7
```

- `X[labels == "positive"]` is the rows of the positive reviews;
  `sum(axis=0)` sums each column, that is, how many times each word appears
  in positive reviews.
- **Adding 1** (smoothing) keeps a word that never appears in one class from
  a division by zero. "terrible" never appears in positive reviews; without
  the +1 its ratio would be infinite.
- A positive **log ratio** means the word is more frequent in negative
  reviews: "terrible", "hate", "worse", "damaged". A negative one means
  positive reviews: "works", "well".
- Two words stand out: **"honest"** points to negative and **"expected"** to
  positive reviews. On their own both are neutral words. The data holds the
  phrases "not good, to be honest" and "I expected it to be bad, but no".
  A model learns not the **meaning** of words but which class they appear
  **together** with. That is both its strength and its danger: if the
  phrasing changes, the learned association breaks.

This calculation is the heart of the Naive Bayes classifier of section 08;
there we add up these same ratios to make a decision.

## Long document, big numbers

```python
lengths = np.asarray(X.sum(axis=1)).ravel()
print(lengths.min(), lengths.max(), round(lengths.mean(), 1))
```

```text
3 38 15.0
```

The row totals range from 3 to 38 words. A long review has bigger counts
than a short one; when comparing two documents, length can drown out
meaning. The topic of the next section, TF-IDF, corrects this as well as the
weight of frequent words that appear in every document.

## Summary

- A bag of words turns each document into a row of counts of the vocabulary's
  words; order is forgotten.
- `CountVectorizer`: `fit` learns the vocabulary, `transform` counts; the
  result is a sparse matrix.
- Words not in the vocabulary are silently dropped. Build the vocabulary on
  the training data only.
- `binary=True` is a presence bag; in short texts it can beat counts.
- Word totals by class and the log ratio with +1 smoothing show which word
  points to which class. A model learns association, not meaning.
