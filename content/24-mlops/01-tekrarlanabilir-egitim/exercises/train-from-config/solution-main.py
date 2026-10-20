from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


def train(config):
    X, y = to_xy(make_customers(config["rows"], seed=config["data_seed"]))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config["test_share"], random_state=config["split_seed"])
    model = RandomForestClassifier(n_estimators=config["n_estimators"],
                                   random_state=config["model_seed"])
    model.fit(X_train, y_train)
    return round(model.score(X_test, y_test), 3)


CONFIG = {"rows": 800, "data_seed": 7, "test_share": 0.25,
          "split_seed": 0, "n_estimators": 30, "model_seed": 0}
print("accuracy:", train(CONFIG))
print("again:", train(CONFIG))
print("more trees:", train({**CONFIG, "n_estimators": 60}))
