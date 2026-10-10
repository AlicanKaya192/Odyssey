from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def beats_baseline(weight):
    X, y = make_classification(n_samples=1000, n_features=5, weights=[weight], random_state=3)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3)
    base = DummyClassifier(strategy="most_frequent").fit(X_train, y_train).score(X_test, y_test)
    model = LogisticRegression().fit(X_train, y_train).score(X_test, y_test)
    return {"baseline": round(base, 3), "model": round(model, 3), "better": bool(model - base >= 0.02)}

result = beats_baseline(0.9)
print(result["baseline"], result["model"])
print(result["better"])
