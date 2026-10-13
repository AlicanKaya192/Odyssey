import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from text_data import make_reviews

reviews = make_reviews(1000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])


def cv_mean(C):
    return 0.0


print(cv_mean(1))
print(cv_mean(10))
