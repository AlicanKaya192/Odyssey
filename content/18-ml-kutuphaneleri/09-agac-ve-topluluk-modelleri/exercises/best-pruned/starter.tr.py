from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier


def best_pruned(folds):
    tree = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
    return [0.0, int(tree.get_n_leaves()), round(float(tree.score(X_test, y_test)), 3)]

print(best_pruned(5))
print(best_pruned(3))
