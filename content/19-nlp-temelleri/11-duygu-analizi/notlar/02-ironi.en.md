In the lesson the model got all 17 reviews with irony right. But those
reviews came from three fixed patterns ("Great, the ... broke on day ...").
Let us train the model on all the reviews and give it **new** ironic
sentences:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from text_data import make_reviews

reviews = make_reviews(2000)
pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                 ("model", LinearSVC())])
pipe.fit([r["text"] for r in reviews], [r["label"] for r in reviews])
new = ["Oh great, another broken zipper.", "Perfect, it died in a week.",
       "Lovely, the strap snapped on the first run.",
       "Thanks a lot, the lid leaks."]
for text, label in zip(new, pipe.predict(new)):
    print(label, "|", text)
```

```text
positive | Oh great, another broken zipper.
positive | Perfect, it died in a week.
positive | Lovely, the strap snapped on the first run.
positive | Thanks a lot, the lid leaks.
```

- It found all four positive. The model had learned the patterns in the
  training data, not irony. It never saw the negative words in these
  sentences ("broken", "died", "snapped", "leaks") during training; what is
  left are positive words such as "great" and "perfect".
- The lexicon of the lesson fails too: it gives the four sentences the scores
  `[1, 1, 0, 0]`. "great" and "perfect" are positive in the lexicon, and
  the negative events are not in it.

## Why is irony hard?

- **The words say the opposite.** The word "perfect" is positive; the
  negativity is in the event the sentence describes ("died in a week").
- **It needs world knowledge.** You need to know that a zipper should not
  break and that a watch should not die in a week.
- **The cues are weak and tied to patterns.** Starting with "Oh great,", a
  negative event following a positive word, many exclamation marks. These
  are not always irony.

Detecting irony and sarcasm is still an open research topic; even very large
language models get it wrong without context. In practice: in domains where
irony is common (social media), collect more and more varied labelled
examples, and use the output of a sentiment system for **overall trends**
rather than for single decisions.
