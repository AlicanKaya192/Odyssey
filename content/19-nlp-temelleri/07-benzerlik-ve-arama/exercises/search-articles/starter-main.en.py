import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_data import make_articles

articles = make_articles()
texts = [a["title"] + ". " + a["text"] for a in articles]


def search(query, k):
    return []


for query in ["my card was charged two times", "the box came broken", "error E500"]:
    print(query)
    for title in search(query, 2):
        print("-", title)
