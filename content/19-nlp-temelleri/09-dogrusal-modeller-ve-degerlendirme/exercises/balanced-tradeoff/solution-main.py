import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = TfidfVectorizer().fit(X_train)
A, B = vectorizer.transform(X_train), vectorizer.transform(X_test)


def neutral_scores(class_weight):
    model = LogisticRegression(max_iter=1000, class_weight=class_weight).fit(A, y_train)
    pred = model.predict(B)
    precision = ((pred == "neutral") & (y_test == "neutral")).sum() / (pred == "neutral").sum()
    recall = ((pred == "neutral") & (y_test == "neutral")).sum() / (y_test == "neutral").sum()
    return [round(float(precision), 3), round(float(recall), 3)]


print("plain", neutral_scores(None))
print("balanced", neutral_scores("balanced"))
