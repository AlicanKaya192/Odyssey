import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
pipe = None  # adımlar: "tfidf" ve "model"


def predict_labels(sentences):
    return []


print(predict_labels(["Love it.", "It broke after a week."]))
