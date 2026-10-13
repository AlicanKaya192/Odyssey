# Overall Review

You have reached the end of the NLP Fundamentals module. From cleaning raw,
messy text to counting words, from turning documents into vectors to
classification, from finding topics and clusters in unlabelled text to
pulling information out of text, you saw the whole toolbox of classic NLP and
built a support system. This section walks the road once more; at the end is
a small example where the parts of the module work together.

<figure class="fig">
  <div class="flow">
    <span class="node">Text<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Vectors<br><small>05–07</small></span><span class="arrow">→</span>
    <span class="node">Classification<br><small>08–11</small></span><span class="arrow">→</span>
    <span class="node">Unlabelled<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Extraction<br><small>14–15</small></span>
  </div>
  <figcaption>The road of the module: prepare the text, turn it into numbers, classify, group unlabelled text, pull information out of it.</figcaption>
</figure>

## 1. Preparing text (Sections 0–4)

| Job | Tool |
|---|---|
| Encoding and cleaning | bytes and code points, `unicodedata.normalize("NFKC")`, `html.unescape`, the Turkish case trap |
| Splitting | `re.findall`, your own pattern, splitting into sentences, apostrophes in Turkish |
| Normalising | stop words, stemming, lemmatisation, placeholders |
| Counting | n-grams, character n-grams, PMI, Zipf's law |

Look at the text first; cleaning is chosen for the task. "not" may be in a
stop word list, but in sentiment analysis it carries the meaning.

## 2. From text to vectors (Sections 5–7)

| Job | Tool |
|---|---|
| Bag of words | `CountVectorizer`, sparse matrix, out-of-vocabulary words, counts or presence |
| Weighting | `TfidfVectorizer`: IDF, `l2` per row, the length effect |
| Similarity and search | cosine similarity, precision@1, BM25 |

The vectoriser is built **with the training data only**; new text comes in
with `transform`.

## 3. Classification (Sections 8–11)

| Job | Tool |
|---|---|
| Probabilistic | `MultinomialNB`, Laplace smoothing |
| Linear | `LogisticRegression`, `LinearSVC`, `coef_`, `class_weight` |
| Measuring | confusion matrix, precision, recall, F1, macro F1, decision threshold |
| Structure | `Pipeline`, `cross_val_score`, `GridSearchCV` (`step__parameter`) |
| Sentiment | lexicon + negation, aspect-based sentiment |

Word pairs catch negation; `best_score_` is optimistic; with labelled data a
model clearly beats a lexicon.

## 4. Unlabelled text (Sections 12–13)

| Job | Tool |
|---|---|
| Topics | `NMF` (TF-IDF), `LatentDirichletAllocation` (counts) |
| Clusters | `KMeans`, silhouette score, purity |
| Near duplicates | character n-gram sets, Jaccard, MinHash, LSH |

Topics are not your categories; choose the number of topics and clusters by
readability; use a stable hash function for lasting signatures.

## 5. Information extraction and the project (Sections 14–15)

| Job | Tool |
|---|---|
| Formatted fields | regular expressions, `\b`, `(?:...)`, named groups, a gold standard |
| Lists of names | gazetteer, ambiguity |
| Project | baseline, masking, error analysis, an "I am not sure" gate |

## All together

A small system that takes a ticket, predicts its category, pulls out the
order number and suggests the best help-centre article:

```python
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from text_data import make_articles, make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])


def mask(text):
    text = re.sub(r"\bORD-\d+\b", " ordernum ", text)
    return " ".join(text.lower().split())


vectorizer = TfidfVectorizer(preprocessor=mask, ngram_range=(1, 2))
pipe = Pipeline([("tfidf", vectorizer), ("model", LinearSVC())])
scores = cross_val_score(pipe, texts, labels, cv=5, scoring="f1_macro")
print(round(scores.mean(), 3))
pipe.fit(texts, labels)
articles = make_articles()
search = TfidfVectorizer(stop_words="english")
A = search.fit_transform([a["title"] + " " + a["text"] for a in articles])
question = "My parcel ORD-55120 arrived damaged, can I get a refund?"
best = cosine_similarity(search.transform([question]), A).argmax()
print(pipe.predict([question])[0], re.findall(r"\bORD-\d{5}\b", question))
print(articles[best]["title"])
```

```text
0.962
refund ['ORD-55120']
Lost, late or damaged parcels
```

- **Preparation:** masking turned order numbers into one placeholder and
  lowercased the text (01, 15).
- **Classification:** TF-IDF + word pairs + a linear SVM in one Pipeline;
  measured as macro F1 with 5-fold cross-validation (09, 10).
- **Search:** articles are TF-IDF vectors; the question goes to the nearest
  article by cosine similarity (07).
- **Extraction:** the order number with a regular expression (14).

The system classified the ticket as a refund, pulled out the order number and
suggested the "lost, late or damaged parcels" article. The "refund or
replacement for a damaged item" article might have fit better; but search
only looks at word overlap, and "parcel" appears only in the chosen article.
Each part was built separately in this module; together they do real work,
limits included.

## Next

In this module we represented text with **word counts**. This
representation has limits you know: "car" and "automobile" are two separate
columns with nothing in common; the order of words is lost. In the
**Embeddings and Language Models** module we go from vectors that capture
the meaning of words, through language models that model order, to the
attention mechanism and the transformer. The notes hold a one-page summary of
the whole module and where to go from here.
