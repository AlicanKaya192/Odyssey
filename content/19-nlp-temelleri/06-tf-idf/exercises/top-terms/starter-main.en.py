import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
vectorizer = TfidfVectorizer(min_df=2)
X = vectorizer.fit_transform(texts)
words = vectorizer.get_feature_names_out()


def top_terms(index, k):
    return []


for i in range(3):
    print(i, top_terms(i, 3))
