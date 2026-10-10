from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=5000, n_features=20, n_informative=6,
                           flip_y=0.1, random_state=5)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=5)
from sklearn.ensemble import HistGradientBoostingClassifier


def early_trees(rate):
    model = HistGradientBoostingClassifier(learning_rate=rate, max_iter=1000, random_state=0)
    model.fit(X_train, y_train)
    return [int(model.n_iter_), round(float(model.score(X_test, y_test)), 3)]

print(early_trees(0.1))
print(early_trees(0.3))
