from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def beats_baseline(weight):
    return {"baseline": 0.0, "model": 0.0, "better": False}

result = beats_baseline(0.9)
print(result["baseline"], result["model"])
print(result["better"])
