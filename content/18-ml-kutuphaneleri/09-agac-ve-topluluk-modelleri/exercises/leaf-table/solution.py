from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier


def leaf_table(sizes):
    rows = []
    for size in sizes:
        model = DecisionTreeClassifier(min_samples_leaf=size, random_state=0)
        score = cross_val_score(model, X_train, y_train, cv=5).mean()
        leaves = model.fit(X_train, y_train).get_n_leaves()
        rows.append([size, int(leaves), round(float(score), 3)])
    return rows

print(*leaf_table([1, 10, 30]), sep="\n")
