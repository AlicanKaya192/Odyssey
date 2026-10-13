import math


def tfidf_vectors(docs):
    vocab = sorted({w for d in docs for w in d.split()})
    return [[d.split().count(w) for w in vocab] for d in docs]


for row in tfidf_vectors(["a b c", "a b", "c c d"]):
    print(row)
