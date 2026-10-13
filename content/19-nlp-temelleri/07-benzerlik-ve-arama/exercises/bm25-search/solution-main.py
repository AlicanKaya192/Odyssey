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
    scores = []
    for doc in tokens:
        tf = Counter(doc)
        norm = k1 * (1 - b + b * len(doc) / avg_len)
        score = 0.0
        for w in analyze(query):
            if w in tf:
                idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                score += idf * tf[w] * (k1 + 1) / (tf[w] + norm)
        scores.append(score)
    return scores


for query in ["tracking number not working", "reset my password"]:
    scores = bm25(query)
    best = max(range(N), key=lambda i: scores[i])
    print(round(scores[best], 3))
    print(articles[best]["title"])
