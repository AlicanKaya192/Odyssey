You can put the cleaning function of section 01 inside the vectoriser:
`TfidfVectorizer(preprocessor=clean)`. Then cleaning is part of the Pipeline
too and is not forgotten when the model is used. Let us try it on the messy
reviews:

```python
import html
import re
import unicodedata

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from text_data import messy_reviews

QUOTES = str.maketrans({chr(0x2018): "'", chr(0x2019): "'",
                        chr(0x201C): '"', chr(0x201D): '"'})


def clean(text):
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(QUOTES).replace(chr(0x200B), "")
    return " ".join(text.split()).lower()


reviews = messy_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
for preprocessor in [None, clean]:
    pipe = Pipeline([("tfidf", TfidfVectorizer(preprocessor=preprocessor)),
                     ("model", LogisticRegression(max_iter=1000))]).fit(X_train, y_train)
    size = len(pipe.named_steps["tfidf"].vocabulary_)
    print(preprocessor is not None, round(pipe.score(X_test, y_test), 3), size)
print(TfidfVectorizer().build_analyzer()(texts[3])[:6])
```

```text
False 0.88 328
True 0.878 326
['it', 'does', 'the', 'job', 'br', 'much']
```

- Cleaning did not change the accuracy (88.0% against 87.8%). scikit-learn's
  tokeniser looks for `\w\w+`, so the no-break space, the zero-width space
  and quotes already split words. The cleaning of section 01 was critical
  when splitting with `split(" ")`; not with this tokeniser.
- But look at the last line: without cleaning, the `<br>` tag became a word
  "br". The vocabulary is dirty; on other data (pages with lots of HTML) such
  words can mislead the model. Judge cleaning not only by accuracy but **by
  looking at the vocabulary** too.

## preprocessor, tokenizer, analyzer

| Parameter | When it runs | Note |
|---|---|---|
| `preprocessor` | Before splitting, on the whole text | When given, the default lowercasing is **not** done; the function must do it |
| `tokenizer` | Turns text into a token list | Like `TOKEN.findall` from 02; pass `token_pattern=None` so no warning appears |
| `analyzer` | All the work in one function | You do preprocessing, splitting and n-grams yourself |

If you save a Pipeline that uses your own functions, those functions must be
importable under the same name when loading it; keep the function in a
module.
