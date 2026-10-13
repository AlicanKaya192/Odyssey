import numpy as np
from corpus_data import CAPITALS, make_corpus

sentences = [s.split() for s in make_corpus(10000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 2), min(len(s), i + 3)):
            if j != i:
                M[index[w], index[s[j]]] += 1
total = M.sum()
with np.errstate(divide="ignore"):
    P = np.maximum(np.log(M * total / np.outer(M.sum(1), M.sum(0))), 0)
U, S, _ = np.linalg.svd(P)


def capital_score(k):
    return 0


for k in [5, 20, 100]:
    print(k, capital_score(k))
