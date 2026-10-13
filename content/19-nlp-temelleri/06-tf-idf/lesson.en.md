# TF-IDF

In the bag of words "the" has the biggest counts because it appears several
times in every review; yet it is no help at all in telling one review from
another. On the contrary, "bluetooth" or "damaged", which appear in only a
few reviews, say a lot about those reviews. **TF-IDF** turns this intuition
into a number: it multiplies a word's frequency in the document (TF) by the
inverse of how many documents it appears in (IDF). This section computes
TF-IDF by hand first, compares the result with scikit-learn exactly and
measures what it changes on real reviews.

## IDF: how many documents does a word appear in?

The **document frequency** (df) is the number of different documents a word
appears in. The **inverse document frequency** (IDF) is its inverse: a big
value for a word in few documents, a small one for a word in every document.
scikit-learn's default formula:

$$\text{idf}(w) = \ln\frac{1 + n}{1 + \text{df}(w)} + 1$$

Here $n$ is the number of documents. The +1 in the numerator and the
denominator avoids a division by zero for a word never seen; the +1 at the
end keeps the weight of a word found in every document from being exactly
zero.

```python
import math

docs = ["the battery is great", "the battery died", "great price great sound"]
vocab = sorted({w for d in docs for w in d.split()})
n = len(docs)
df = {w: sum(w in d.split() for d in docs) for w in vocab}
idf = {w: math.log((1 + n) / (1 + df[w])) + 1 for w in vocab}
for w in vocab:
    print(w, df[w], round(idf[w], 3))
```

```text
battery 2 1.288
died 1 1.693
great 2 1.288
is 1 1.693
price 1 1.693
sound 1 1.693
the 2 1.288
```

"battery", "great" and "the", which appear in two documents, got 1.288;
those found in a single document got 1.693. In this small example of three
documents the gap is small; in a large corpus it opens up a lot.

## TF × IDF and normalisation

A document's TF-IDF vector: each word's count in the document times its IDF.
Then the vector is brought to **unit length** (L2 normalisation): each value
is divided by the square root of the sum of the squared values.

```python
def tfidf(doc):
    words = doc.split()
    raw = [words.count(w) * idf[w] for w in vocab]
    norm = math.sqrt(sum(x * x for x in raw))
    return [round(x / norm, 3) for x in raw]


for d in docs:
    print(tfidf(d))
```

```text
[0.46, 0.0, 0.46, 0.605, 0.0, 0.0, 0.46]
[0.518, 0.681, 0.0, 0.0, 0.0, 0.0, 0.518]
[0.0, 0.0, 0.732, 0.0, 0.481, 0.481, 0.0]
```

- In the first document "is" (found only there) got the biggest weight,
  0.605; "battery", "great" and "the" stayed at 0.46.
- In the third document "great" is 0.732 because it appears twice.
- Thanks to normalisation every row has length 1: long and short documents
  are now on the same scale (the problem at the end of section 05).

## Compare with scikit-learn

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)
print(vectorizer.idf_.round(3).tolist())
mine = np.array([tfidf(d) for d in docs])
print(np.allclose(X.toarray(), mine, atol=1e-3))
```

```text
[1.288, 1.693, 1.288, 1.693, 1.693, 1.693, 1.288]
True
```

`TfidfVectorizer` = `CountVectorizer` + the IDF weight + L2 normalisation.
The `idf_` attribute holds the learned IDF values; they are the same as the
ones we computed by hand. `np.allclose` confirms that every value of the two
tables is equal (within a thousandth). Compare a calculation you wrote by
hand with the library like this: it shows you really understood the
formula.

## IDF on the reviews

```python
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
words = vectorizer.get_feature_names_out()
idf = vectorizer.idf_
order = np.argsort(idf)


def show(indices):
    return [(str(words[i]), round(float(idf[i]), 2)) for i in indices]


print("low ", show(order[:4]))
print("high", show(order[-3:]))
```

```text
low  [('the', 1.12), ('is', 1.54), ('for', 2.25), ('it', 2.33)]
high [('wosre', 7.91), ('wsate', 7.91), ('zpiper', 7.91)]
```

- The lowest IDFs are "the", "is", "for" and "it": words found in almost
  every review. TF-IDF pushes them down without any stop list.
- The highest IDFs are "wosre", "wsate" and "zpiper": **typos**. Every word
  that appears only once gets the highest IDF, and most of those are mistakes
  or one-off numbers. TF-IDF rewards rarity; it does not know whether rarity
  is information or noise. That is why `min_df` (04) is used with TF-IDF so
  often.

## The standout words of one review

The heaviest words of the same review, by count and by TF-IDF:

```python
import textwrap

from sklearn.feature_extraction.text import CountVectorizer

counts = CountVectorizer().fit(texts)
C = counts.transform(texts)
doc = 7
print(textwrap.fill(texts[doc], 60))
row_c = C[doc].toarray().ravel()
row_t = X[doc].toarray().ravel()
print("count", [str(words[i]) for i in np.argsort(row_c)[::-1][:4]])
print("tfidf", [str(words[i]) for i in np.argsort(row_t)[::-1][:4]])
```

```text
Totally worth the money. The colour is not loud at all. I
love the buttons. I love the colour.
count ['the', 'love', 'colour', 'not']
tfidf ['colour', 'love', 'the', 'buttons']
```

By count "the" (four times) comes first; with TF-IDF "colour" and "love"
moved ahead and "buttons" entered the list. "the" fell to third place but
did not leave the list: although its IDF is small, appearing four times keeps
it high. In the notes you will see the `sublinear_tf` setting that softens
this.

## Is the length effect gone?

```python
lengths = np.asarray(C.sum(axis=1)).ravel()
norms = np.sqrt(np.asarray(X.multiply(X).sum(axis=1)).ravel())
print(lengths.min(), lengths.max())
print(norms.min().round(3), norms.max().round(3))
```

```text
3 38
1.0 1.0
```

The reviews are 3 to 38 words long, yet every TF-IDF row has length 1.
`X.multiply(X)` squares every value; the square root of the row sum is the
row's length. This will matter in the next section when we measure
similarity: the dot product of two unit vectors is directly the cosine of
the angle between them.

## Summary

- TF is a word's frequency in a document, IDF the inverse of how many
  documents it appears in; TF-IDF is their product. Words found everywhere
  are pushed down, telling ones come forward.
- scikit-learn's IDF is $\ln\frac{1+n}{1+\text{df}} + 1$; then every row is
  brought to unit length with L2. The hand calculation and `TfidfVectorizer`
  are exactly the same.
- The lowest IDFs are stop words, the highest are one-off words (often
  typos). Rarity can be information or noise: `min_df`.
- Normalisation removes the length effect; every row has length 1.
