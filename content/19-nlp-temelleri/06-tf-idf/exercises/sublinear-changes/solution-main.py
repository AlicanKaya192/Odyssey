import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_reviews


def top_word_changes(n):
    texts = [r["text"] for r in make_reviews(n)]
    plain = TfidfVectorizer().fit_transform(texts)
    soft = TfidfVectorizer(sublinear_tf=True).fit_transform(texts)
    a = np.asarray(plain.argmax(axis=1)).ravel()
    b = np.asarray(soft.argmax(axis=1)).ravel()
    return int((a != b).sum())


for n in [100, 500, 2000]:
    print(n, top_word_changes(n))
