import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_reviews

reviews = make_reviews(2000)
labels = np.array([r["label"] for r in reviews])
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([r["text"] for r in reviews])
words = vectorizer.get_feature_names_out()


def indicative(label_a, label_b, k):
    a = np.asarray(X[labels == label_a].sum(axis=0)).ravel() + 1
    b = np.asarray(X[labels == label_b].sum(axis=0)).ravel() + 1
    log_ratio = np.log((a / a.sum()) / (b / b.sum()))
    return [str(words[i]) for i in np.argsort(log_ratio)[::-1][:k]]


print(", ".join(indicative("neutral", "positive", 5)))
print(", ".join(indicative("positive", "neutral", 5)))
