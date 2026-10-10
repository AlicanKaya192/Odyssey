from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=10, n_informative=4,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV


def best_c(cs):
    search = GridSearchCV(LogisticRegression(), {"C": cs}, cv=5).fit(X_train, y_train)
    return [search.best_params_["C"], round(search.best_score_, 3)]

print(best_c([0.01, 0.1, 1.0, 10.0]))
