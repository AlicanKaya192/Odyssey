from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=8, n_informative=5,
                           n_classes=3, weights=[0.7, 0.2, 0.1], random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3,
                                                    stratify=y)
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


def f1_averages(c):
    pred = LogisticRegression(C=c).fit(X_train, y_train).predict(X_test)
    return {"per_class": [], "macro": 0.0, "weighted": 0.0}

result = f1_averages(1.0)
print(result["per_class"])
print(result["macro"], result["weighted"])
