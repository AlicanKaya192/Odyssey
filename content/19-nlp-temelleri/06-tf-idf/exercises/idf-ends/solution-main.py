import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_tickets

vectorizer = TfidfVectorizer().fit([t["text"] for t in make_tickets(2000)])
words = vectorizer.get_feature_names_out()


def idf_ends(k):
    order = np.argsort(vectorizer.idf_, kind="stable")
    return [[str(words[i]) for i in order[:k]], [str(words[i]) for i in order[-k:]]]


low, high = idf_ends(5)
print(", ".join(low))
print(", ".join(high))
