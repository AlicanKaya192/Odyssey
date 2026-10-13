import numpy as np


def rank(doc_vectors, query):
    return []

docs = [[1.0, 0.0], [0.7, 0.7], [0.0, 1.0], [-1.0, 0.0]]
print(rank(docs, [0.9, 0.1]))
print(rank(docs, [0.0, 2.0]))
