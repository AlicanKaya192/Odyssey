import math


def tfidf_vectors(docs):
    vocab = sorted({w for d in docs for w in d.split()})
    n = len(docs)
    idf = {w: math.log((1 + n) / (1 + sum(w in d.split() for d in docs))) + 1 for w in vocab}
    rows = []
    for d in docs:
        raw = [d.split().count(w) * idf[w] for w in vocab]
        norm = math.sqrt(sum(x * x for x in raw))
        rows.append([round(x / norm, 3) for x in raw])
    return rows


for row in tfidf_vectors(["a b c", "a b", "c c d"]):
    print(row)
