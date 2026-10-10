from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=6, n_informative=3,
                           flip_y=0.1, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression


def tuned_copy(c):
    return [0.0, 0.0, True]

print(tuned_copy(5.0))
