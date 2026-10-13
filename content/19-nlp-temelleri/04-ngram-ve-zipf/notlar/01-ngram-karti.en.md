n-gram and vocabulary settings of scikit-learn's vectorisers.

| Parameter | What it does | Example |
|---|---|---|
| `ngram_range=(1, 2)` | Single words and pairs | "not", "good", "not good" |
| `ngram_range=(2, 2)` | Pairs only | "not good" |
| `analyzer="word"` | Word n-grams (the default) | |
| `analyzer="char"` | Character n-grams, across word borders | "t g" is a piece too |
| `analyzer="char_wb"` | Character n-grams, inside words | " lo", "lov", "ove", "ve " |
| `min_df=2` | Drops what appears in fewer than 2 documents | one-off pairs go |
| `min_df=0.01` | Must appear in at least 1% of documents (a share) | |
| `max_df=0.9` | Drops what appears in more than 90% of documents | acts like a stop list |
| `max_features=1000` | Keeps the 1000 most frequent n-grams | a cap on the column count |

## Pruning the vocabulary with min_df

```python
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
for min_df in [1, 2, 5, 20]:
    vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=min_df).fit(texts)
    print(min_df, len(vectorizer.vocabulary_))
```

```text
1 2737
2 1573
5 901
20 454
```

Dropping n-grams that appear in a single document (`min_df=2`) removes more
than 40% of the columns. They could not have been learned from a single
example anyway. Making `min_df` too big also removes rare but telling
phrases; we choose the right value with validation data (sections 09 and
10).

## Which n?

- **Word 1-2 grams:** the most common starting point for classification;
  catches negations such as "not good".
- **Word 3-grams and up:** the vocabulary explodes and rarely pays off.
- **Character 3-5 grams (`char_wb`):** good for text with many typos,
  suffixes and foreign words (tweets, product names); useful for
  agglutinative languages such as Turkish too.
