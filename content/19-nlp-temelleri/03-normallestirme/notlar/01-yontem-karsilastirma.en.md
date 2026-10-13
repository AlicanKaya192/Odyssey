Four normalisation tools, what they do and what they cost.

| Method | What it does | Example | The price | When |
|---|---|---|---|---|
| Stop words | Removes frequent words with no meaning on their own | "the", "is" go | Negation and intensity words can go too | Topic discovery, search; careful in sentiment analysis |
| Stemming | Cuts suffixes by rules | "loves" → "love" | Inconsistent stems, over- and under-stemming | Fast, rough joining |
| Lemmatisation | The base form in the dictionary | "was" → "be" | Needs a dictionary and grammar, slow | When accuracy matters |
| Placeholder | Turns variable information into one token | ORD-48213 → `<order>` | The information itself is lost | Classification; not in information extraction |

## A stop list that keeps negation

If you use the ready-made list, take the negation and intensity words out of
it:

```python
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

KEEP = {"not", "no", "never", "nor", "very", "too"}
STOP = ENGLISH_STOP_WORDS - KEEP
print(len(STOP))
tokens = "the fit is not good at all".split()
print([t for t in tokens if t not in STOP])
```

```text
312
['fit', 'not', 'good']
```

`ENGLISH_STOP_WORDS` is a `frozenset`; taking the difference with `-` gives a
new set and leaves the original list unchanged. "not" is kept now: "fit not
good".

## In scikit-learn

| Parameter | What it does |
|---|---|
| `CountVectorizer(stop_words="english")` | Uses the ready-made English list (removes negations too) |
| `CountVectorizer(stop_words=list(STOP))` | Uses your own list |
| `CountVectorizer(lowercase=False)` | Keeps upper case |
| `CountVectorizer(tokenizer=function)` | Your own tokeniser; it can stem too |
| `CountVectorizer(preprocessor=function)` | Applied to the text before splitting (cleaning, placeholders) |

## The order

Cleaning → placeholders → splitting → lowercasing → stop words → stemming.
Placeholders come **before** splitting: emails and amounts have to be caught
before they fall apart.
