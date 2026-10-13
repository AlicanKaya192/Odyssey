# Linear Models and Evaluation

Naive Bayes found each word's weight by counting. **Linear models**
(logistic regression, linear SVMs) **learn** the weights: they set how
important each word is for each class so as to minimise the prediction
error. TF-IDF + logistic regression is the strongest "first try" in text
classification and is often enough. This section compares three models, then
shows why accuracy is not enough, and covers the per-class measures
**precision**, **recall** and **F1**.

## A linear model on text

Logistic regression gives every word a weight for every class. A document's
score for a class is the sum of the TF-IDF values of its words times their
weights for that class (plus a constant). The scores are turned into
probabilities with softmax and the largest is chosen. It is the same model
you wrote from scratch in ML Algorithms; here the columns are words.

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = TfidfVectorizer().fit(X_train)
A, B = vectorizer.transform(X_train), vectorizer.transform(X_test)
models = {"logistic": LogisticRegression(max_iter=1000),
          "svm": LinearSVC(), "naive bayes": MultinomialNB()}
for name, model in models.items():
    model.fit(A, y_train)
    print(name, round(model.score(B, y_test), 3))
```

```text
logistic 0.88
svm 0.888
naive bayes 0.852
```

- Logistic regression 88%, the linear SVM 88.8%; with the same TF-IDF
  features Naive Bayes 85.2%.
- `LinearSVC` widens the margin between the border separating the classes
  and the closest examples; it works very well and fast on sparse text data
  with many columns. It gives no probabilities (no `predict_proba`).
- `max_iter=1000`: logistic regression adjusts the weights step by step; the
  default number of steps is sometimes not enough and it warns.

## Accuracy is not enough: the confusion matrix

88% accuracy does not mean 88% for every class. To see which class is
confused with which, let us use the proper name of the error table from
section 00: the **confusion matrix**.

```python
from sklearn.metrics import confusion_matrix

lr = models["logistic"]
pred = lr.predict(B)
print(lr.classes_.tolist())
print(confusion_matrix(y_test, pred, labels=lr.classes_))
```

```text
['negative', 'neutral', 'positive']
[[ 75   2  21]
 [  6  49  17]
 [  2  12 316]]
```

- Rows are the **true** class, columns the **prediction** (negative, neutral,
  positive in that order). The diagonal holds the correct predictions: 75,
  49, 316.
- 21 negative reviews were taken for positive; 17 neutral ones too. When the
  model is unsure it drifts towards the largest class, positive.
- 316 of the 330 positive reviews are right: this class is what pulls the
  accuracy up.

## Precision, recall, F1

Two questions are asked for every class:

- **Precision:** when the model says "negative", how often is it right?
  $\frac{\text{correct negatives}}{\text{all called negative}}$
- **Recall:** how many of the true negatives did it catch?
  $\frac{\text{correct negatives}}{\text{all true negatives}}$
- **F1** is their harmonic mean: $\frac{2PR}{P + R}$. If either is very low,
  F1 is low too.

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, pred, digits=3))
```

```text
              precision    recall  f1-score   support

    negative      0.904     0.765     0.829        98
     neutral      0.778     0.681     0.726        72
    positive      0.893     0.958     0.924       330

    accuracy                          0.880       500
   macro avg      0.858     0.801     0.826       500
weighted avg      0.878     0.880     0.877       500
```

- Negative: precision 0.904 (mostly right when it says negative), recall
  0.765 (it misses a quarter of the negatives).
- Neutral is the hardest class: F1 0.726.
- **macro avg** is the plain mean over classes: every class counts equally.
  **weighted avg** is weighted by class size: the big class (positive)
  dominates. On imbalanced data macro F1 (0.826) is a more honest summary
  than accuracy (0.880).

## Strengthening a small class

`class_weight="balanced"` weights each class's errors inversely to the
class's size: a mistake in a small class costs more.

```python
balanced = LogisticRegression(max_iter=1000, class_weight="balanced")
balanced.fit(A, y_train)
print(classification_report(y_test, balanced.predict(B), digits=3))
```

```text
              precision    recall  f1-score   support

    negative      0.784     0.888     0.833        98
     neutral      0.652     0.806     0.720        72
    positive      0.947     0.861     0.902       330

    accuracy                          0.858       500
   macro avg      0.794     0.851     0.818       500
weighted avg      0.872     0.858     0.862       500
```

- Negative recall 0.765 → 0.888, neutral 0.681 → 0.806: the minority classes
  are caught much better.
- The price: their precision fell (neutral 0.778 → 0.652) and overall
  accuracy went 0.880 → 0.858.

Which one is right depends on the task. If missing complaints matters
(routing negative reviews to customer service), recall; if false alarms are
expensive, precision. This is a **trade-off**: raising one usually lowers the
other.

## What did the model learn?

Logistic regression's weights (`coef_`) can be read: the words with the
biggest weights for each class.

```python
words = vectorizer.get_feature_names_out()
for i, label in enumerate(lr.classes_):
    top = np.argsort(lr.coef_[i])[::-1][:5]
    print(label, [str(words[j]) for j in top])
```

```text
negative ['not', 'hate', 'worse', 'can', 'say']
neutral ['okay', 'fine', 'delivery', 'took', 'job']
positive ['but', 'totally', 'love', 'well', 'much']
```

- Negative: "not", "hate", "worse"; but **"can" and "say"** are there too.
  The data holds the phrase "I can't say it is good", and TF-IDF's default
  tokeniser drops the "n't" (02): "can't" became "can". The model loaded the
  negation onto the word "can".
- Neutral: "okay", "fine", "delivery took" ("Delivery took 16 days" is
  common in neutral reviews).
- Positive: "but" comes first: from the phrase "I expected ... but no" in
  positive reviews.

Looking at the coefficients is the cheapest way both to understand the model
and to catch oddities in the data.

## With word pairs

```python
from sklearn.metrics import f1_score

bigrams = TfidfVectorizer(ngram_range=(1, 2)).fit(X_train)
A2, B2 = bigrams.transform(X_train), bigrams.transform(X_test)
for model in [LogisticRegression(max_iter=1000), LinearSVC()]:
    pred2 = model.fit(A2, y_train).predict(B2)
    accuracy = round(float((pred2 == y_test).mean()), 3)
    macro = round(f1_score(y_test, pred2, average="macro"), 3)
    print(type(model).__name__, accuracy, macro)
```

```text
LogisticRegression 0.898 0.846
LinearSVC 0.916 0.874
```

The linear SVM with word pairs reached 91.6% accuracy and 0.874 macro F1:
the best result in this module so far. The rules of section 00 were at
44.9%.

## Summary

- Linear models learn a weight for every word and every class. TF-IDF +
  logistic regression or a linear SVM is a strong start for text
  classification.
- The confusion matrix shows which class is confused with which; rows are
  true, columns predicted.
- Precision is "is it right when it says so", recall "did it catch them all";
  F1 is their harmonic mean. On imbalanced data look at macro F1.
- `class_weight="balanced"` raises the recall of minority classes and lowers
  precision and accuracy: choose for the task.
- Coefficients can be read; they reveal phrases in the data and traces of the
  tokeniser ("can").
