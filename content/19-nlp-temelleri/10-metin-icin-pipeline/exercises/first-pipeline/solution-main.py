import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
pipe = Pipeline([("tfidf", TfidfVectorizer()),
                 ("model", LogisticRegression(max_iter=1000))])
pipe.fit(texts, labels)


def predict_labels(sentences):
    return pipe.predict(sentences).tolist()


print(predict_labels(["Love it.", "It broke after a week."]))
