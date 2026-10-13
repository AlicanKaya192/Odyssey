The second common use of similarity is finding **duplicate** documents: a
customer who sends the same ticket twice, two listings of the same product.
Let us compare each of 300 tickets with every other one:

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(300)]
X = TfidfVectorizer().fit_transform(texts)
S = (X @ X.T).toarray()
np.fill_diagonal(S, 0)
i, j = np.unravel_index(S.argmax(), S.shape)
print(round(float(S[i, j]), 3))
print(texts[i][:60])
print(texts[j][:60])
pairs = int((np.triu(S) > 0.8).sum())
print(pairs)
```

```text
1.0
The app does not load my order history.
The app does not load my order history.
35
```

- `np.fill_diagonal(S, 0)` removes each document's similarity with itself
  (1); otherwise the largest value would always be on the diagonal.
- `np.unravel_index` turns the position of the largest value in the flat
  array into a (row, column) pair.
- The most similar pair is exactly the same text: similarity 1. `np.triu`
  takes the upper triangle of the table (so each pair is counted once); there
  are **35 pairs** above 0.8.

## Threshold and scale

- The **threshold** (such as 0.8) is chosen for the task: a low threshold
  takes different tickets for duplicates too, a high one only finds exact
  copies. Choose it by looking at a few pairs by hand.
- Comparing every document with every document is **n²** work: 300 tickets
  are 90 thousand comparisons, 1 million tickets 10¹² comparisons. Finding
  duplicates in a large corpus needs approximate methods such as MinHash;
  the topic of section 13.
