import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from text_data import make_tickets

tickets = make_tickets(2000)
vectorizer = TfidfVectorizer(min_df=2)
X = vectorizer.fit_transform([t["text"] for t in tickets])
model = LogisticRegression(max_iter=1000).fit(X, [t["category"] for t in tickets])
words = vectorizer.get_feature_names_out()


def top_words(label, k):
    row = model.coef_[list(model.classes_).index(label)]
    return [str(words[i]) for i in np.argsort(row)[::-1][:k]]


for label in model.classes_:
    print(label, ", ".join(top_words(label, 3)))
