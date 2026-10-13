import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews

reviews = make_reviews(2000)
labels = np.array([r["label"] for r in reviews])
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([r["text"] for r in reviews])
words = vectorizer.get_feature_names_out()


def indicative(label_a, label_b, k):
    return []


print(", ".join(indicative("neutral", "positive", 5)))
print(", ".join(indicative("positive", "neutral", 5)))
