import numpy as np
from corpus_data import GENDER_PAIRS, make_corpus, make_jobs

sentences = [s.split() for s in make_corpus(10000) + make_jobs(3000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 3), min(len(s), i + 4)):
            if j != i:
                M[index[w], index[s[j]]] += 1
with np.errstate(divide="ignore"):
    P = np.maximum(np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0))), 0)
U, S, _ = np.linalg.svd(P)
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)
PAIRS = GENDER_PAIRS + [("he", "she"), ("his", "her")]


def gap(a, b):
    g = np.mean([E[index[f]] - E[index[m]] for m, f in PAIRS], axis=0)
    g = g / np.linalg.norm(g)
    return round(float(E[index[a]] @ g - E[index[b]] @ g), 3)


print(gap("nurse", "engineer"))
print(gap("teacher", "writer"))
