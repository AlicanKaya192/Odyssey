from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=8, n_informative=4,
                           weights=[0.8], flip_y=0.05, random_state=6)
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier


def train_test_gap(depth):
    return {"train": 0.0, "test": 0.0, "f1": 0.0}

print(train_test_gap(None))
print(train_test_gap(3))
