import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)


def per_class_hits(ngrams):
    vectorizer = CountVectorizer(ngram_range=tuple(ngrams)).fit(X_train)
    model = MultinomialNB().fit(vectorizer.transform(X_train), y_train)
    pred = model.predict(vectorizer.transform(X_test))
    return {str(c): round(float((pred[y_test == c] == c).mean()), 3) for c in sorted(set(y_test))}


for ngrams in [(1, 1), (1, 2)]:
    print(ngrams)
    for label, hit in per_class_hits(ngrams).items():
        print("  ", label, hit)
