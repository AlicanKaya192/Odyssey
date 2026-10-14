from sklearn.feature_extraction.text import TfidfVectorizer

from shop_data import TICKETS

POOL = [t for t in TICKETS if t["id"] % 4 != 0]


def nearest_labels(text, k):
    vectorizer = TfidfVectorizer().fit([t["text"] for t in POOL])
    pool_vectors = vectorizer.transform([t["text"] for t in POOL])
    scores = (pool_vectors @ vectorizer.transform([text]).T).toarray().ravel()
    order = sorted(range(len(POOL)), key=lambda i: -scores[i])
    return [POOL[i]["label"] for i in order[:k]]


print(nearest_labels("My refund has not arrived yet.", 3))
print(nearest_labels("The tent zip is broken.", 2))
