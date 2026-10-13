import numpy as np


def rank(doc_vectors, query):
    D = np.array(doc_vectors, dtype=float)
    D = D / np.linalg.norm(D, axis=1, keepdims=True)
    q = np.array(query, dtype=float)
    sims = D @ (q / np.linalg.norm(q))
    return [int(i) for i in np.argsort(-sims, kind="stable")]

docs = [[1.0, 0.0], [0.7, 0.7], [0.0, 1.0], [-1.0, 0.0]]
print(rank(docs, [0.9, 0.1]))
print(rank(docs, [0.0, 2.0]))
