import math
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_articles

articles = make_articles()
analyze = CountVectorizer().build_analyzer()
tokens = [analyze(a["title"] + ". " + a["text"]) for a in articles]
avg_len = sum(len(t) for t in tokens) / len(tokens)
df = Counter(w for t in tokens for w in set(t))
N = len(tokens)


def bm25(query, k1=1.5, b=0.75):
    return [0.0] * N


for query in ["tracking number not working", "reset my password"]:
    scores = bm25(query)
    best = max(range(N), key=lambda i: scores[i])
    print(round(scores[best], 3))
    print(articles[best]["title"])
