from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=10, n_informative=4,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
from scipy.stats import randint
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV


def random_forest_search(n_iter):
    space = {"n_estimators": randint(10, 60), "max_depth": randint(2, 8)}
    search = RandomizedSearchCV(RandomForestClassifier(random_state=0), space,
                                n_iter=n_iter, cv=3, random_state=0).fit(X_train, y_train)
    return [int(search.best_params_["max_depth"]), round(search.best_score_, 3)]

print(random_forest_search(5))
