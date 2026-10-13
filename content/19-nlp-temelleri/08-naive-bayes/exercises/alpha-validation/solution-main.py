import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_rest, X_test, y_rest, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
X_train, X_val, y_train, y_val = train_test_split(
    X_rest, y_rest, test_size=0.25, random_state=0, stratify=y_rest)
vectorizer = CountVectorizer().fit(X_train)


def best_alpha(alphas):
    A, V = vectorizer.transform(X_train), vectorizer.transform(X_val)
    scores = [round(MultinomialNB(alpha=a).fit(A, y_train).score(V, y_val), 3) for a in alphas]
    best = scores.index(max(scores))
    return [alphas[best], scores[best]]


alpha, val = best_alpha([0.01, 0.03, 0.1, 0.3, 1.0, 3.0])
model = MultinomialNB(alpha=alpha).fit(vectorizer.transform(X_train), y_train)
print(alpha, val, round(model.score(vectorizer.transform(X_test), y_test), 3))
