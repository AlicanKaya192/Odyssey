from collections import Counter

import numpy as np
from corpus_data import make_corpus

sentences = [s.split() for s in make_corpus(5000)]
counts = Counter(w for s in sentences for w in s)
vocab = sorted(counts)
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 2), min(len(s), i + 3)):
            if j != i:
                M[index[w], index[s[j]]] += 1


def similarity(a, b, drop):
    return 0.0


for drop in [0, 5]:
    print(drop, similarity("cat", "dog", drop), similarity("cat", "bread", drop))
