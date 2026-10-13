The parts of `CountVectorizer` used most often.

## Methods and attributes

| Name | What it does |
|---|---|
| `fit(texts)` | Learns the vocabulary |
| `transform(texts)` | Counts texts with the learned vocabulary (a sparse matrix) |
| `fit_transform(texts)` | Both at once; on training data only |
| `get_feature_names_out()` | The column names (words), in column order |
| `vocabulary_` | A word → column number dictionary |
| `build_analyzer()` | A function that shows how it splits text |
| `inverse_transform(X)` | Back from rows to the words found in each document |

## Parameters

| Parameter | Default | Note |
|---|---|---|
| `lowercase` | `True` | `False` to keep upper case |
| `token_pattern` | words of at least two characters | single letters and the "n't" are dropped (02) |
| `stop_words` | `None` | `"english"` removes negations too (03) |
| `ngram_range` | `(1, 1)` | `(1, 2)` adds pairs (04) |
| `min_df`, `max_df` | `1`, `1.0` | drop rare and very frequent columns |
| `max_features` | `None` | caps it at the k most frequent words |
| `binary` | `False` | presence instead of counts |

## max_features and going back

```python
from sklearn.feature_extraction.text import CountVectorizer

docs = ["the battery is great", "the battery died", "great price great sound"]
vectorizer = CountVectorizer(max_features=4)
X = vectorizer.fit_transform(docs)
print(vectorizer.get_feature_names_out().tolist())
print(vectorizer.inverse_transform(X[2:3])[0].tolist())
```

```text
['battery', 'died', 'great', 'the']
['great']
```

`max_features=4` kept only the 4 most frequent words; "price" and "sound"
were dropped. Going back to the third document leaves only "great": the
document is no longer "great price great sound". Shrinking the vocabulary
always removes something; you can see what with `inverse_transform`.
