from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=8, n_informative=4,
                           weights=[0.8], flip_y=0.05, random_state=6)
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier


def train_test_gap(depth):
    model = DecisionTreeClassifier(max_depth=depth, random_state=0)
    res = cross_validate(model, X, y, cv=5, scoring=["accuracy", "f1"],
                         return_train_score=True)
    return {"train": round(float(res["train_accuracy"].mean()), 3),
            "test": round(float(res["test_accuracy"].mean()), 3),
            "f1": round(float(res["test_f1"].mean()), 3)}

print(train_test_gap(None))
print(train_test_gap(3))
