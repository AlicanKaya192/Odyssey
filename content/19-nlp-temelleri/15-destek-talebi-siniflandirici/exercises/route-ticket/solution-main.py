import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
MASKS = [(r"\bORD-\d+\b", " ordernum "), (r"\$[\d,]+(?:\.\d{2})?", " amount "),
         (r"\S+@\S+", " email "), (r"\b\d{4}-\d{2}-\d{2}\b", " date "),
         (r"\bE\d{3,4}\b", " errcode ")]


def mask(text):
    for pattern, placeholder in MASKS:
        text = re.sub(pattern, placeholder, text)
    return " ".join(text.lower().split())
pipe = Pipeline([("tfidf", TfidfVectorizer(preprocessor=mask)),
                 ("model", LinearSVC())]).fit(X_train, y_train)


def route(text):
    return {"category": str(pipe.predict([text])[0]),
            "orders": re.findall(r"\bORD-\d{5}\b", text),
            "urgent": "urgent" in text.lower()}


for key, value in route("Order ORD-55120 arrived damaged. URGENT!").items():
    print(key, value)
