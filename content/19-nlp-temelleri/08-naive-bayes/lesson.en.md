# Classification with Naive Bayes

In section 05 we measured with a log ratio how strongly each word points to
a class. **Naive Bayes** turns that idea into a classifier: it adds up the
signals of all the words in a document and picks the most likely class. It
is one of the oldest and still one of the fastest methods of text
classification, and it works surprisingly well with little data. This
section writes Naive Bayes from scratch with NumPy, compares it exactly with
scikit-learn's `MultinomialNB` and measures the effect of smoothing and of
word pairs.

## Bayes' rule

Given a document $d$, the probability that its class is $c$:

$$P(c \mid d) \propto P(c) \prod_{w \in d} P(w \mid c)$$

- $P(c)$ is the **prior**: the share of this class in the data. Most
  reviews are positive, so the positive prior is big.
- $P(w \mid c)$ is the probability that the word appears in texts of that
  class.
- $\propto$ means "proportional to": the denominator is the same for every
  class, so there is no need to compute it; picking the largest is enough.

The **"naive"** assumption is this: once the class is known, the words are
independent of each other. That is plainly false ("not" and "good" depend on
each other), yet the method still works well, because classification does
not need the probabilities to be exactly right, only the largest to belong
to the right class.

## Training and test data

```python
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = CountVectorizer().fit(X_train)
A, B = vectorizer.transform(X_train), vectorizer.transform(X_test)
print(A.shape, B.shape)
print({str(c): int((y_train == c).sum()) for c in sorted(set(y_train))})
```

```text
(1500, 326) (500, 326)
{'negative': 295, 'neutral': 217, 'positive': 988}
```

- `train_test_split` puts 75% of the reviews in training and 25% in test.
  `stratify=labels` keeps the class shares the same in both parts; important
  on imbalanced data.
- The vectoriser is `fit` on the **training** texts only (05, 06). The
  vocabulary has 326 words.

## Naive Bayes from scratch

Training is nothing but counting two things: the share of each class and
the count of each word in each class.

```python
classes = np.array(sorted(set(y_train)))
log_prior = np.log([(y_train == c).mean() for c in classes])
counts = np.array([
    np.asarray(A[y_train == c].sum(axis=0)).ravel() for c in classes])
smoothed = counts + 1
log_lik = np.log(smoothed / smoothed.sum(axis=1, keepdims=True))
print(classes.tolist(), log_prior.round(3).tolist())
print(log_lik.shape)
```

```text
['negative', 'neutral', 'positive'] [-1.626, -1.933, -0.418]
(3, 326)
```

- `log_prior` is the logarithm of each class's share: positive −0.418 (66%),
  neutral −1.933 (14.5%).
- `counts` is a 3 × 326 table: each row a class, each column a word.
- **+1 (Laplace smoothing):** if a word never seen in a class had
  probability 0, every document containing that word would get zero
  probability for that class. The +1 leaves every word a small share (the
  same idea as the log ratio of section 05).
- `log_lik` is $\log P(w \mid c)$: each row is divided by its own total and
  its logarithm is taken.

Prediction is adding up the log probabilities of the document's words and
adding the prior:

```python
scores = np.asarray(B @ log_lik.T) + log_prior
pred = classes[scores.argmax(axis=1)]
print(round(float((pred == y_test).mean()), 3))
print(round(float((y_test == "positive").mean()), 3))
```

```text
0.866
0.66
```

- `B @ log_lik.T` gives, for each test document, the sum of each word's count
  times that word's log probability: the product in the formula became a sum
  in the log world.
- The accuracy is **86.6%**; the baseline that calls every review "positive"
  gets 66%. The hand-written rules of section 00 stayed at 44.9%.

## Why the logarithm?

```python
print(np.prod(np.full(400, 0.01)))
print(np.sum(np.log(np.full(400, 0.01))).round(1))
```

```text
0.0
-1842.1
```

If every word of a 400-word document had probability 0.01, the product
would be $10^{-800}$: far below the smallest decimal number a computer can
hold. The result comes out as **0** and every class looks equal (underflow).
The sum of the logarithms stays at −1842.1 without trouble. We always add up
products of probabilities as logs.

## Compare with scikit-learn, and alpha

```python
from sklearn.naive_bayes import MultinomialNB

nb = MultinomialNB().fit(A, y_train)
print(round(nb.score(B, y_test), 3), bool((nb.predict(B) == pred).all()))
for alpha in [0.01, 0.1, 1, 10, 100]:
    model = MultinomialNB(alpha=alpha).fit(A, y_train)
    print(alpha, round(model.score(B, y_test), 3))
```

```text
0.866 True
0.01 0.868
0.1 0.872
1 0.866
10 0.862
100 0.682
```

- `MultinomialNB` agrees with our code on **every** prediction. The default
  `alpha=1` is our +1.
- `alpha` is the strength of smoothing. 0.1 is the best on this data (87.2%);
  100 leaves every word such a big share that the differences between words
  vanish and the model almost fell back to the prior, that is, the baseline
  (68.2%). `alpha` is a hyperparameter; we choose its value with validation
  data, not test data (section 10).

## Looking at predictions

```python
examples = ["the battery is great", "not good at all", "it broke after two days"]
for text in examples:
    probs = nb.predict_proba(vectorizer.transform([text]))[0]
    print(text, "->", nb.classes_[probs.argmax()], probs.round(2).tolist())
```

```text
the battery is great -> positive [0.25, 0.14, 0.62]
not good at all -> negative [0.74, 0.0, 0.26]
it broke after two days -> negative [0.93, 0.04, 0.03]
```

- `predict_proba` gives the class probabilities in `classes_` order
  (negative, neutral, positive).
- "not good at all" was found negative (74%): "not" and "all" are frequent in
  negative reviews and outweigh the positive signal of "good". Naive Bayes
  does not understand negation; it counts words one by one and was lucky this
  time.
- Naive Bayes probabilities usually come out **overconfident** (like 0.93):
  the independence assumption counts the same information several times. Not
  a problem for classification, but do not read the probability directly as
  a measure of confidence.

## Word pairs

```python
bigrams = CountVectorizer(ngram_range=(1, 2)).fit(X_train)
nb2 = MultinomialNB().fit(bigrams.transform(X_train), y_train)
print(round(nb2.score(bigrams.transform(X_test), y_test), 3))
probs = nb2.predict_proba(bigrams.transform(["not good at all"]))[0]
print(nb2.classes_[probs.argmax()], probs.round(2).tolist())
```

```text
0.888
negative [0.99, 0.0, 0.01]
```

With word pairs added the accuracy rose to 88.8%; "not good" is now a single
feature and the model is 99% sure about "not good at all". n-grams partly
undo the biggest harm of the naive assumption (words depending on each
other).

## Support tickets

The same method on the five-class ticket data:

```python
from text_data import make_tickets

tickets = make_tickets(2000)
t_texts = [t["text"] for t in tickets]
t_labels = np.array([t["category"] for t in tickets])
t_train, t_test, c_train, c_test = train_test_split(
    t_texts, t_labels, test_size=0.25, random_state=0, stratify=t_labels)
t_vec = CountVectorizer().fit(t_train)
t_nb = MultinomialNB().fit(t_vec.transform(t_train), c_train)
print(round(t_nb.score(t_vec.transform(t_test), c_test), 3))
print(round(float((c_test == "shipping").mean()), 3))
```

```text
0.928
0.296
```

92.8% accuracy; the baseline that says the most frequent class ("shipping")
gets 29.6%. As the number of classes grows the baseline falls and the
model's contribution shows more clearly.

## Summary

- Naive Bayes: $P(c \mid d) \propto P(c) \prod P(w \mid c)$; with the "naive"
  assumption that words are independent once the class is known.
- Training is counting: class shares and word counts per class; +1 (Laplace)
  keeps unseen words from getting zero probability.
- Add up logarithms instead of multiplying probabilities; otherwise the
  result underflows to 0.
- The model we wrote from scratch is exactly `MultinomialNB`: 86.6% on the
  reviews, 88.8% with word pairs, 92.8% on the tickets.
- `alpha` is the strength of smoothing; if it grows too big, the model falls
  back to the prior.
