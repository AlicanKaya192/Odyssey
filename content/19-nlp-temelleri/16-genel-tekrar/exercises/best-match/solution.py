import math
from collections import Counter


def cosine(a, b):
    dot = sum(a[w] * b[w] for w in a)
    norm = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return dot / norm if norm else 0.0


def best_match(query, docs):
    q = Counter(query.lower().split())
    scores = [cosine(q, Counter(d.lower().split())) for d in docs]
    return scores.index(max(scores))

docs = ["refund for my card", "the parcel arrived damaged", "reset my password"]
print(best_match("my parcel is damaged", docs))
print(best_match("password reset please", docs))
