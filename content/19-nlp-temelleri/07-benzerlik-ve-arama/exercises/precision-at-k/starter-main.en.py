import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_data import make_articles, make_tickets

articles = make_articles()
texts = [a["title"] + ". " + a["text"] for a in articles]
cats = np.array([a["category"] for a in articles])
tickets = make_tickets(1000)
truth = np.array([t["category"] for t in tickets])
vectorizer = TfidfVectorizer(stop_words="english").fit(texts)
S = cosine_similarity(vectorizer.transform([t["text"] for t in tickets]), vectorizer.transform(texts))


def precision_at_k(k):
    return 0.0


for k in [1, 2, 3]:
    print(k, precision_at_k(k))
