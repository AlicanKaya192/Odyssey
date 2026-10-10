from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=6, n_informative=3,
                           flip_y=0.1, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
from sklearn.ensemble import RandomForestClassifier


def seed_scores(seeds):
    scores = []
    for seed in seeds:
        forest = RandomForestClassifier(n_estimators=5, random_state=seed).fit(X_train, y_train)
        scores.append(round(forest.score(X_test, y_test), 3))
    return scores

print(seed_scores([0, 1, 2]))
