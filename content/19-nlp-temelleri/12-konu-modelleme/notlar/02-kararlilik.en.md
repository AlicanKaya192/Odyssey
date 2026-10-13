If you retrain a topic model with a different `random_state`, does it find
the same topics? Let us try NMF and LDA with the lesson's preprocessing and
three seeds, and look at the first three words of each topic:

```python
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import (ENGLISH_STOP_WORDS,
                                             CountVectorizer, TfidfVectorizer)
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
stop = list(ENGLISH_STOP_WORDS | {"ord", "com", "example", "hi", "hello",
                                  "thanks", "thank", "dear", "support",
                                  "regards", "help"})
settings = dict(stop_words=stop, token_pattern=r"[a-z]{2,}", min_df=5)
tfidf, counter = TfidfVectorizer(**settings), CountVectorizer(**settings)
X, C = tfidf.fit_transform(texts), counter.fit_transform(texts)
words = tfidf.get_feature_names_out()


def heads(model):
    return sorted(" ".join(words[r.argsort()[::-1][:3]])
                  for r in model.components_)


for seed in [0, 1, 2]:
    nmf = NMF(n_components=5, random_state=seed, max_iter=500).fit(X)
    lda = LatentDirichletAllocation(n_components=5, random_state=seed).fit(C)
    print(seed, "nmf", heads(nmf)[:2])
    print(seed, "lda", heads(lda)[:2])
```

```text
0 nmf ['account email address', 'app page error']
0 lda ['account log error', 'address account change']
1 nmf ['account email address', 'app page error']
1 lda ['account paid card', 'error login page']
2 nmf ['account email address', 'app page error']
2 lda ['account address wrong', 'account twice tried']
```

- **NMF** found the same topics with all three seeds. By default,
  scikit-learn's NMF does not start from random values but builds its start
  from the matrix itself (with SVD); that is why the seed did not change the
  result.
- **LDA** found different topics with every seed. LDA starts from a random
  point and, on short documents with few words, gets stuck in different local
  solutions.
- We sorted the topics (`sorted`) because topic numbers mean nothing: the
  same topic can be 0 in one run and 3 in another. Compare topics by their
  words, not by their numbers.

Before reporting the result of a topic model, run it with a few seeds. The
topics that come out every time are real; do not trust a topic that appears
once and disappears.
