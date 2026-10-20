from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(1000))

for attempt in [1, 2, 3]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
    model = RandomForestClassifier(n_estimators=30, random_state=0)
    model.fit(X_train, y_train)
    print("attempt", attempt, "accuracy:", round(model.score(X_test, y_test), 3))
