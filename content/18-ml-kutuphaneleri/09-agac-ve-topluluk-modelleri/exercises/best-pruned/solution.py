from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier


def best_pruned(folds):
    full = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
    alphas = full.cost_complexity_pruning_path(X_train, y_train).ccp_alphas
    search = GridSearchCV(DecisionTreeClassifier(random_state=0), {"ccp_alpha": alphas},
                          cv=folds).fit(X_train, y_train)
    tree = search.best_estimator_
    alpha = round(float(search.best_params_["ccp_alpha"]), 4)
    return [alpha, int(tree.get_n_leaves()), round(float(tree.score(X_test, y_test)), 3)]

print(best_pruned(5))
print(best_pruned(3))
