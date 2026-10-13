import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = ["my parcel never arrived", "reset my password please", "the parcel arrived damaged",
        "refund for the damaged parcel", "app crashes on start"]


def rank(query):
    vectorizer = TfidfVectorizer().fit(DOCS)
    scores = cosine_similarity(vectorizer.transform([query]), vectorizer.transform(DOCS)).ravel()
    order = np.argsort(scores, kind="stable")[::-1]
    return [int(i) for i in order if scores[i] > 0]


print(rank("damaged parcel"))
print(rank("password"))
print(rank("weather today"))
