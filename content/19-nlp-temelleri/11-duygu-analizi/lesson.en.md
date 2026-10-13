# Sentiment Analysis

**Sentiment analysis** is finding out whether a text is positive or negative.
In sections 08 and 09 we did it as classification: we learned a model from
labelled reviews and reached 91.6%. This section is the other side of the
coin: with no labelled data at all, how far can a **sentiment lexicon** and a
few rules take us? Then we compare the two ways on the same test data and
find **what** a review likes and dislikes: aspect-based sentiment.

## Lexicon-based sentiment

The simplest idea: count positive words as +1 and negative words as −1, and
look at the sign of the total.

```python
import re

import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from text_data import make_reviews

POSITIVE = {"good", "solid", "comfortable", "reliable", "sturdy", "nice",
            "quiet", "great", "excellent", "perfect", "fantastic",
            "impressive", "love", "loves", "worth", "better", "well", "needed"}
NEGATIVE = {"bad", "weak", "flimsy", "poor", "uncomfortable", "loud",
            "fragile", "terrible", "awful", "useless", "disappointing", "hate",
            "worse", "waste", "broke", "damaged", "late", "returned",
            "stopped", "never"}
TOKEN = re.compile(r"[a-z']+|[.,!?]")


def plain_score(text):
    words = TOKEN.findall(text.lower())
    return sum((w in POSITIVE) - (w in NEGATIVE) for w in words)


def to_label(score):
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)


def evaluate(name, score):
    pred = np.array([to_label(score(t)) for t in X_test])
    macro = f1_score(y_test, pred, average="macro")
    print(name, round((pred == y_test).mean(), 3), round(macro, 3))
    return pred


print(plain_score("The strap is great but the screen is weak."))
evaluate("plain", plain_score)
```

```text
0
plain 0.636 0.57
```

- We wrote the lexicon ourselves: 18 positive and 20 negative words. There is
  no training; we split off training data only for the comparison.
- "great" +1, "weak" −1: the total is 0, so neutral. Reasonable for a mixed
  sentence.
- Accuracy is 63.6%, below even the baseline (always "positive", 65.9%). But
  the lexicon does not pile everything into one class like the baseline does:
  macro F1 0.57.

## Negation

For the lexicon, "Not worth the money" is positive: "worth" is +1. The
**negation** rule: flip the sign of the few words after a word such as "not",
"can't" or "never". A punctuation mark stops the effect.

```python
NEGATORS = {"not", "can't", "never", "no", "don't", "didn't"}


def negated_score(text, window=3):
    total, left = 0, 0
    for word in TOKEN.findall(text.lower()):
        if word in ".,!?":
            left = 0
            continue
        if word in NEGATORS:
            left = window
            continue
        value = (word in POSITIVE) - (word in NEGATIVE)
        if left:
            value = -value
            left -= 1
        total += value
    return total


print(negated_score("Not worth the money."))
print(negated_score("The lid is not bad at all."))
lexicon_pred = evaluate("negation", negated_score)
```

```text
-1
1
negation 0.754 0.691
```

- `left` counts how many more words after the negator are affected (a window
  of 3). "not bad" is now +1.
- One rule raised accuracy from 63.6% to 75.4%. This is the lexicon's
  counterpart of what word pairs ("not good") added to the model in 09.
- The window is a rough approximation: it errs on sentences such as "not only
  good but great". Real systems (such as VADER) handle negation, intensifiers
  ("very") and capitals with separate rules; all of them are hand-written.

## After "but"

In real reviews the part after "but" often carries the real verdict: "The
screen is nice but the battery dies in a day." So some lexicon methods weigh
what comes after "but" more. Let us try:

```python
def but_score(text, weight=2):
    lower = text.lower()
    if " but " not in lower:
        return negated_score(lower)
    head, tail = lower.rsplit(" but ", 1)
    return negated_score(head) + weight * negated_score(tail)


evaluate("but x2", but_score)
```

```text
but x2 0.726 0.661
```

The rule **did harm** (from 75.4% to 72.6%). In this data the "But ..."
sentence is a **small objection** appended to the end of a review: the start
of the review decides the rating. A rule from other data does not carry over
to this data. This is the weak side of lexicon methods: each rule is a guess
about a language habit, and a guess is only confirmed by measuring.

## Lexicon or model?

Let us compare with the best model of section 09 on the same test data, and
look separately at reviews with negation and irony:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                 ("model", LinearSVC())]).fit(X_train, y_train)
model_pred = pipe.predict(X_test)
print("model", round((model_pred == y_test).mean(), 3))
groups = {"negation": r"\bnot\b|can't",
          "sarcasm": r"great, the|just perfect|wonderful, it"}
for name, pattern in groups.items():
    idx = [i for i, t in enumerate(X_test) if re.search(pattern, t, re.I)]
    lex = (lexicon_pred[idx] == y_test[idx]).mean()
    mod = (model_pred[idx] == y_test[idx]).mean()
    print(name, len(idx), round(lex, 3), round(mod, 3))
```

```text
model 0.916
negation 127 0.827 0.984
sarcasm 17 0.765 1.0
```

- The model gets 91.6%, the lexicon 75.4%. On the 127 reviews with negation,
  the model gets 98.4% and the lexicon 82.7%.
- The model got all 17 reviews with irony right. But careful: these reviews
  come from three patterns ("Great, the ... broke"), and the model memorised
  the patterns. The second note measures what happens on a new ironic
  sentence.
- The lexicon's main error is calling positive reviews neutral: sentences
  such as "Five stars for the strap", with no word from the lexicon, get 0.

With labelled data, the model wins. When is a lexicon useful?

| Situation | Why a lexicon |
|---|---|
| No labelled data at all | The only way to start; it then suggests labels to check |
| The decision must be explained | You can see which word gave how many points |
| Moving outside the domain the model was trained on | A model is tied to the patterns of its training data |

A lexicon depends on the domain too: "loud" can be negative for headphones
and positive for a speaker; "unpredictable" is praise for a film's plot and a
complaint about a car's steering.

## Aspect-based sentiment

If a review says "the strap is great but the screen is weak", a single label
loses information. **Aspect-based sentiment** decides for each feature
separately. A simple way: split the review into sentences and score the
sentence that mentions a feature with the lexicon.

```python
from text_data import PRODUCTS


def aspect_scores(text, aspects):
    found = {}
    for sentence in re.findall(r"[^.!?]+", text.lower()):
        for aspect in aspects:
            if aspect in sentence:
                found[aspect] = found.get(aspect, 0) + negated_score(sentence)
    return found


aspects = PRODUCTS["sports watch"]
print(aspect_scores("The strap is great. The screen is weak.", aspects))
table = {a: [0, 0] for a in aspects}
for r in reviews:
    if r["product"] == "sports watch":
        for aspect, score in aspect_scores(r["text"], aspects).items():
            table[aspect][0] += score > 0
            table[aspect][1] += score < 0
for aspect, (good, bad) in table.items():
    print(f"{aspect:<13} +{good:<3} -{bad}")
```

```text
{'strap': 1, 'screen': -1}
strap         +29  -15
screen        +28  -7
battery       +20  -8
step counter  +22  -15
weight        +32  -12
```

- The number of positive and negative mentions of each feature in the sports
  watch reviews. By ratio, the best liked is the screen (28 to 7), the least
  liked the step counter (22 to 15).
- For a shop this is much more useful than a single star average: it says
  which part needs fixing.
- The method is rough: it misses a sentence that refers back to the feature
  with "it" ("It broke after a week"), and gives a sentence with two features
  the same score for both. Better methods match the feature and the opinion
  word through the structure of the sentence.

## Summary

- Lexicon-based sentiment adds up word scores; it needs no training.
- The negation rule alone raised 63.6% to 75.4%. Weighing what comes after
  "but" did harm on this data: do not adopt rules without measuring.
- With labelled data the model wins by far (91.6%). A lexicon is useful when
  there are no labels, when an explanation is needed and when the domain
  changes.
- Aspect-based sentiment finds separately what a review likes.
