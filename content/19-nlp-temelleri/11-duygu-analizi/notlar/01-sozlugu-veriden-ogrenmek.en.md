Instead of writing the lexicon by hand you can extract it from labelled data:
a word that appears much more often in positive reviews than in negative
ones counts as positive. The measure is the **log-odds**: the logarithm of
the ratio between how often a word appears in positive reviews and how often
it appears in negative ones. As in 08, we smooth with +1.

```python
import math
import re
from collections import Counter

import numpy as np
from sklearn.model_selection import train_test_split
from text_data import make_reviews

TOKEN = re.compile(r"[a-z']+")
reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
counts = {"positive": Counter(), "negative": Counter()}
for text, label in zip(X_train, y_train):
    if label in counts:
        counts[label].update(set(TOKEN.findall(text.lower())))
sizes = {k: int((y_train == k).sum()) for k in counts}


def log_odds(word):
    pos = (counts["positive"][word] + 1) / (sizes["positive"] + 2)
    neg = (counts["negative"][word] + 1) / (sizes["negative"] + 2)
    return math.log(pos / neg)


common = counts["positive"] + counts["negative"]
frequent = sorted(w for w in common if common[w] >= 5)
ranked = sorted(frequent, key=log_odds)
print("negative:", " ".join(ranked[:10]))
print("positive:", " ".join(ranked[::-1][:10]))
```

```text
negative: terrible honest hate of worse waste box damaged late was
positive: works no expected well totally love too packed loves early
```

- There are real sentiment words ("terrible", "hate", "waste", "love"), but
  also words with no sentiment at all: "of" ("waste of money"), "box" ("the
  box was damaged"), "wife" ("my wife loves it"), "honest" ("not good, to be
  honest"). These are traces not of sentiment but of **the patterns in this
  data**.
- "no" came out positive: the pattern "I expected it to be bad, but no."
  appears only in positive reviews. Negators should not enter the lexicon.
- A learned lexicon is no different from a model: it is a rough form of a
  model's weights. Its advantage is that it is readable; you can look at the
  list and remove wrong words by hand.

## How many words?

Let us take the top k words in each direction and score with the negation
rule of the lesson:

```python
NEGATORS = {"not", "can't", "never", "no", "don't", "didn't"}


def score(text, good, bad):
    total, left = 0, 0
    for word in re.findall(r"[a-z']+|[.,!?]", text.lower()):
        if word in ".,!?":
            left = 0
        elif word in NEGATORS:
            left = 3
        else:
            value = (word in good) - (word in bad)
            total += -value if left else value
            left = max(left - 1, 0)
    return total


for k in [10, 20, 40]:
    good, bad = set(ranked[::-1][:k]), set(ranked[:k])
    pred = ["positive" if s > 0 else "negative" if s < 0 else "neutral"
            for s in (score(t, good, bad) for t in X_test)]
    print(k, round(float(np.mean(np.array(pred) == y_test)), 3))
```

```text
10 0.612
20 0.754
40 0.708
```

- 75.4% with 20 words: the same place as our hand-written lexicon of 38
  words. 10 words are too few; at 40 the accuracy falls again. A longer list
  is not always better.
- Here we compared k by looking at the test data; in real work this is
  leakage. k is a setting and is chosen with validation data (or
  cross-validation); the test is used once at the very end.
