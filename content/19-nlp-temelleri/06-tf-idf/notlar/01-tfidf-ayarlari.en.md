`TfidfVectorizer` takes every parameter of `CountVectorizer`; on top of them
come the settings of the weighting.

| Parameter | Default | What it does |
|---|---|---|
| `use_idf` | `True` | With `False`, only TF + normalisation |
| `smooth_idf` | `True` | The +1s in the IDF formula; with `False`, $\ln\frac{n}{\text{df}} + 1$ |
| `sublinear_tf` | `False` | $1 + \ln(\text{tf})$ instead of TF: softens the effect of repetition |
| `norm` | `"l2"` | Brings rows to unit length; `"l1"` sums to 1, `None` no normalisation |
| `min_df`, `max_df`, `ngram_range` | | As in `CountVectorizer` (04, 05) |

## sublinear_tf: softening repetition

In the lesson's review "the" was third even with TF-IDF because it appears
four times. `sublinear_tf=True` uses the logarithm of the count instead of the
count itself: once → 1, four times → 2.39, ten times → 3.30.

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
for sublinear in [False, True]:
    vectorizer = TfidfVectorizer(sublinear_tf=sublinear)
    X = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names_out()
    row = X[7].toarray().ravel()
    print(sublinear, [str(words[i]) for i in np.argsort(row)[::-1][:4]])
```

```text
False ['colour', 'love', 'the', 'buttons']
True ['colour', 'love', 'buttons', 'loud']
```

"the" left the list and "loud" came in. In long documents (emails,
articles) a word appearing 20 times is not ten times more important than
one appearing twice; that is why `sublinear_tf` is common on long texts.

## Which settings to start with?

A solid start for text classification:

```text
TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
```

Then try `min_df`, `ngram_range` and `sublinear_tf` with validation data
(09, 10). A stop list is usually not needed: IDF already pushes frequent
words down.
