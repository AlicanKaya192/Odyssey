from sklearn.linear_model import LogisticRegression
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(2000))
model = LogisticRegression(max_iter=1000).fit(X, y)

alarm = None
for month in range(7):
    X_new, y_new = to_xy(make_customers(1000, seed=99, month=month))
    accuracy = round(model.score(X_new, y_new), 3)
    print("month", month, "accuracy:", accuracy)
    if accuracy < 0.75 and alarm is None:
        alarm = month
if alarm is None:
    print("no alarm")
else:
    print("alarm at month:", alarm)
