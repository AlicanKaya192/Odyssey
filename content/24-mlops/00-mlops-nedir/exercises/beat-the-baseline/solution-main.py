from sklearn.linear_model import LogisticRegression
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(2000))
X_test, y_test = to_xy(make_customers(1000, seed=99))

model = LogisticRegression(max_iter=1000).fit(X, y)
stay = 1 - sum(y_test) / len(y_test)
print("model accuracy:", round(model.score(X_test, y_test), 3))
print("always stay:", round(stay, 3))
