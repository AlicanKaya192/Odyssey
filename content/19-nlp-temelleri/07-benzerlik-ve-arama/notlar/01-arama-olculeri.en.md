In the lesson we only looked at the first result. Users often read the first
few results; that is why search is evaluated with several measures.

| Measure | Its question |
|---|---|
| precision@k | Is there a right result among the first k? (a rate) |
| MRR (mean reciprocal rank) | At which position is the first right result? The mean of 1/position |
| recall@k | How many of the right results are in the first k? (when there are several) |

## Let us measure

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_data import make_articles, make_tickets

articles = make_articles()
texts = [a["title"] + ". " + a["text"] for a in articles]
cats = np.array([a["category"] for a in articles])
tickets = make_tickets(1000)
truth = np.array([t["category"] for t in tickets])
vec = TfidfVectorizer().fit(texts)
queries = vec.transform([t["text"] for t in tickets])
S = cosine_similarity(queries, vec.transform(texts))
ranked = np.argsort(S, axis=1)[:, ::-1]
for k in [1, 3, 5]:
    hit = (cats[ranked[:, :k]] == truth[:, None]).any(axis=1)
    print(k, round(float(hit.mean()), 3))
first = (cats[ranked] == truth[:, None]).argmax(axis=1) + 1
print(round(float((1 / first).mean()), 3))
```

```text
1 0.784
3 0.908
5 0.962
0.858
```

- `ranked` is the order of the articles by score for each query.
  `cats[ranked[:, :k]]` gives the categories of the first k articles;
  `truth[:, None]` spreads each query's right category across those k
  columns (broadcasting).
- 78.4% in the first result, 90.8% in the first three, 96.2% in the first
  five. A help centre that shows three results shows the right article for
  90% of tickets.
- `first` is the position of the first right article; **MRR** is the mean of
  1/position: 0.858. Finding it first scores 1, second 0.5. A single number
  answers "how high up is the right result".

## Which one to use?

- If the user looks only at the first result (an automatic reply, "Did you
  mean this?"), precision@1.
- If the user sees a list, precision@3 or @5 and MRR.
- The evaluation queries must look like **real** queries. A search engine
  measured with "easy" hand-written queries can be far worse in reality.
