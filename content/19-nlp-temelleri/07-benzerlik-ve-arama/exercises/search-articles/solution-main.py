import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_data import make_articles

articles = make_articles()
texts = [a["title"] + ". " + a["text"] for a in articles]


vectorizer = TfidfVectorizer(stop_words="english").fit(texts)
A = vectorizer.transform(texts)


def search(query, k):
    scores = cosine_similarity(vectorizer.transform([query]), A).ravel()
    best = np.argsort(scores, kind="stable")[::-1][:k]
    return [articles[i]["title"] for i in best if scores[i] > 0]


for query in ["my card was charged two times", "the box came broken", "error E500"]:
    print(query)
    for title in search(query, 2):
        print("-", title)
