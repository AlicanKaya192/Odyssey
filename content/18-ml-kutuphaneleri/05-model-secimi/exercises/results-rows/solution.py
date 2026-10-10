from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=10, n_informative=4,
                           flip_y=0.05, random_state=10)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV


def results_rows(cs):
    search = GridSearchCV(LogisticRegression(), {"C": cs}, cv=5).fit(X_train, y_train)
    res = search.cv_results_
    rows = []
    for params, mean, std in zip(res["params"], res["mean_test_score"], res["std_test_score"]):
        rows.append([params["C"], round(float(mean), 3), round(float(std), 3)])
    return rows

print(*results_rows([0.001, 0.1, 10.0]), sep="\n")
