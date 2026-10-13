# Capstone: A Support Ticket Classifier

In this section we bring together what you learned in this module in one
project. The task: a system that sorts the tickets reaching a shop's support
team into **five categories** (account, billing, refund, shipping,
technical), pulls out the order number and flags urgent ones. The steps
follow the order of a real project: look at the data, measure the baseline,
set up preprocessing, choose the model, examine the errors, try the second
task (priority) and tie it all into one function.

## Data and baseline

```python
import re
from collections import Counter

import numpy as np
from sklearn.model_selection import train_test_split
from text_data import make_tickets

tickets = make_tickets(4000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
for name, count in Counter(labels.tolist()).most_common():
    print(name, count)
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
print(len(X_train), len(X_test), round((y_test == "shipping").mean(), 3))
```

```text
shipping 1163
technical 1005
account 819
billing 624
refund 389
3000 1000 0.291
```

- The classes are imbalanced: shipping is three times refund. So besides
  accuracy we use **macro F1** as the measure (09).
- The split uses `stratify`: each class has the same share in the test data
  as in all the data.
- The baseline: calling every ticket "shipping" is 29.1% right. Every model
  must beat this clearly.

## Preprocessing: masking

The tickets contain order numbers, amounts, emails, dates and error codes.
Each number enters the vocabulary as a separate word (`ord`, `27246`...) and
none is seen twice. Let us turn them into **shared placeholders** with the
rules from 14:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

MASKS = [(r"\bORD-\d+\b", " ordernum "), (r"\$[\d,]+(?:\.\d{2})?", " amount "),
         (r"\S+@\S+", " email "), (r"\b\d{4}-\d{2}-\d{2}\b", " date "),
         (r"\bE\d{3,4}\b", " errcode ")]


def mask(text):
    for pattern, placeholder in MASKS:
        text = re.sub(pattern, placeholder, text)
    return " ".join(text.lower().split())


print(mask("Refund $12.49 for ORD-27246 to ana7@example.com!"))
for preprocessor in [None, mask]:
    pipe = Pipeline([("tfidf", TfidfVectorizer(preprocessor=preprocessor,
                                               ngram_range=(1, 2))),
                     ("model", LinearSVC())]).fit(X_train, y_train)
    pred = pipe.predict(X_test)
    size = len(pipe.named_steps["tfidf"].vocabulary_)
    print(preprocessor is not None, size, round((pred == y_test).mean(), 3),
          round(f1_score(y_test, pred, average="macro"), 3))
```

```text
refund amount for ordernum to email
False 7117 0.966 0.96
True 1951 0.976 0.971
```

- Masking cut the vocabulary to a quarter. Instead of thousands of one-off
  numbers, a placeholder such as "ordernum" appears in many tickets and the
  model can learn a weight for it: "ordernum" being present raises the
  chance of shipping or refund (the table in 14).
- Accuracy rose a little too. But the real gain is robustness: a new order
  number is no longer a word the model has never seen.
- `mask` also lowercases; as you saw in the note of 10, when a
  `preprocessor` is given the default lowercasing is not done.

## Choosing the model

Let us search the settings with cross-validation; we look at the test data
only once, at the very end:

```python
from sklearn.model_selection import GridSearchCV

pipe = Pipeline([("tfidf", TfidfVectorizer(preprocessor=mask)),
                 ("model", LinearSVC())])
grid = GridSearchCV(pipe, {"tfidf__ngram_range": [(1, 1), (1, 2)],
                           "tfidf__min_df": [1, 2],
                           "model__C": [0.3, 1, 3]}, cv=5, scoring="f1_macro")
grid.fit(X_train, y_train)
print(grid.best_params_)
pred = grid.predict(X_test)
print(round(grid.best_score_, 3), round((pred == y_test).mean(), 3),
      round(f1_score(y_test, pred, average="macro"), 3))
```

```text
{'model__C': 3, 'tfidf__min_df': 1, 'tfidf__ngram_range': (1, 2)}
0.968 0.977 0.972
```

- 12 settings × 5 folds = 60 models. The best is word pairs and `C=3`.
- The test macro F1 of 0.972 is very close to the 0.968 of cross-validation.
  The optimism of the search is small on this data; still, the final number
  is from the test.
- From the baseline's 29.1% to 97.7%. But the tickets were generated from
  patterns; do not expect results this high on real tickets. The method
  stays the same.

## Error analysis

97.7% is good; so where is the remaining 2.3%?

```python
import textwrap

from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y_test, pred, digits=3))
print(confusion_matrix(y_test, pred, labels=grid.classes_))
wrong = [(t, a, b) for t, a, b in zip(X_test, y_test, pred) if a != b]
print(len(wrong))
for text, true, guess in wrong[:3]:
    print(true, "->", guess)
    print(textwrap.fill(text, 76, initial_indent="  ", subsequent_indent="  "))
```

```text
              precision    recall  f1-score   support

     account      0.985     0.956     0.970       205
     billing      0.962     0.974     0.968       156
      refund      0.948     0.938     0.943        97
    shipping      0.980     0.993     0.986       291
   technical      0.988     0.992     0.990       251

    accuracy                          0.977      1000
   macro avg      0.973     0.971     0.972      1000
weighted avg      0.977     0.977     0.977      1000

[[196   5   4   0   0]
 [  2 152   1   1   0]
 [  0   1  91   3   2]
 [  1   0   0 289   1]
 [  0   0   0   2 249]]
23
account -> refund
  Hey there, Please reset the password for femi88@example.com. How long do
  refunds take to show on my card?
account -> billing
  Dear support, Please reset the password for gus53@example.com. Why did my
  card get charged $196.90 this month? Waiting for your answer.
shipping -> technical
  Hey there, My pcakage was delivered to the wrong address. The app crashes
  every time I open the order page. I paid with my credit card. Thanks.
```

- The weakest class is refund (F1 0.943): the class with the fewest examples,
  and it uses the same words as billing ("card", "money", "charged").
- The largest off-diagonal cells of the confusion matrix are account →
  billing (5) and account → refund (4).
- Look at the examples: all three errors are **two-topic** tickets. An
  account ticket asking for a password reset also asks "when will my refund
  show?". Looking at the other errors one by one, all 23 errors contain a
  sentence from a second category (when the tickets were generated, such a
  sentence was added to 15% of them).
- These errors are the limit of the **task**, not of the model: putting a
  two-topic ticket into a single category is debatable anyway. The fix is not
  a better model but a system that can give a ticket more than one category
  (multi-label), or sending two-topic tickets to a person.

## A second task: priority

Tickets are also "high" or "normal" priority. Let us try a rule first, then a
model:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

priority = np.array([t["priority"] for t in tickets])
p_train, p_test = train_test_split(priority, test_size=0.25, random_state=0,
                                   stratify=labels)
rule = np.array(["high" if "urgent" in t.lower() else "normal" for t in X_test])
model = Pipeline([("tfidf", TfidfVectorizer(preprocessor=mask)),
                  ("model", LogisticRegression(max_iter=1000,
                                               class_weight="balanced"))])
guess = model.fit(X_train, p_train).predict(X_test)
for name, out in [("rule", rule), ("model", guess)]:
    print(name, round(precision_score(p_test, out, pos_label="high"), 3),
          round(recall_score(p_test, out, pos_label="high"), 3))
```

```text
rule 1.0 0.545
model 0.943 0.555
```

- The "urgent" rule is always right when it fires (precision 1.0) but finds
  only about half of the urgent tickets.
- The model cannot do better: recall close to the rule's, precision lower.
  The reason is in the data: some urgent tickets were labelled "high"
  without leaving any trace in the text (when the data was generated, 10% of
  the tickets were made urgent at random). No model can learn from text
  information that is not in the text.
- In real life this means the label comes from another source (the
  customer's membership level, the order's value). The fix is not a better
  text model but giving the model that information too.

## Tying it all together

The last step: a function that takes a ticket and returns the category, the
order numbers and the urgency in one go.

```python
def route(text):
    return {"category": str(grid.predict([text])[0]),
            "orders": re.findall(r"\bORD-\d{5}\b", text),
            "urgent": "urgent" in text.lower()}


print(route("Hello, order ORD-55120 arrived damaged. This is urgent!"))
print(route("I cannot log in since Monday."))
```

```text
{'category': 'shipping', 'orders': ['ORD-55120'], 'urgent': True}
{'category': 'account', 'orders': [], 'urgent': False}
```

This function can be put in a web service or in a script that watches an
email inbox. Do not forget to save the model with `joblib` (the first note of
10) and to keep the masking function in a module.

## Summary

- Without a baseline (29.1%) you cannot tell whether a result is good.
- Masking data-specific noise cut the vocabulary to a quarter and made the
  model robust to new numbers.
- Settings were chosen with cross-validation and the result measured once on
  the test: 97.7%, macro F1 0.972.
- Error analysis showed the weak class (refund) and the task's own limit
  (two-topic tickets).
- The priority label was partly not in the text; no text model can get
  around that.
