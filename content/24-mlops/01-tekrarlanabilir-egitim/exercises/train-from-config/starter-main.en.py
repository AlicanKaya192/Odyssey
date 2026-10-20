from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


def train(config):
    # Produce the data, split it, train the model, return the accuracy; every setting from config.
    pass


CONFIG = {"rows": 800, "data_seed": 7, "test_share": 0.25,
          "split_seed": 0, "n_estimators": 30, "model_seed": 0}
print("accuracy:", train(CONFIG))
print("again:", train(CONFIG))
print("more trees:", train({**CONFIG, "n_estimators": 60}))
