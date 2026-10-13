import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_reviews


def top_word_changes(n):
    texts = [r["text"] for r in make_reviews(n)]
    plain = TfidfVectorizer().fit_transform(texts)
    return 0


for n in [100, 500, 2000]:
    print(n, top_word_changes(n))
