from sklearn.linear_model import LogisticRegression
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(2000))
model = LogisticRegression(max_iter=1000).fit(X, y)

# Measure and print the accuracy for each month, then print the alarm.
