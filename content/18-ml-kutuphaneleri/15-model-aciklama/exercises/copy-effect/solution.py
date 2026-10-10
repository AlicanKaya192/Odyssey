import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
df = pd.DataFrame({
    "area": rng.uniform(40, 200, 2000),
    "age": rng.uniform(0, 50, 2000),
    "floor": rng.integers(0, 15, 2000),
    "row_id": rng.permutation(2000),
    "coin": rng.integers(0, 2, 2000),
})
df["price"] = (df["area"] - 0.1 * (df["age"] - 25) ** 2
               + 8 * np.minimum(df["floor"], 8) + rng.normal(0, 15, 2000))
X, y = df.drop(columns="price"), df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
rf = RandomForestRegressor(n_estimators=100, random_state=0).fit(X_train, y_train)
from sklearn.inspection import permutation_importance


def copy_effect(spread):
    noise = np.random.default_rng(1).normal(0, spread, len(X))
    X2 = X.assign(area_copy=X["area"] + noise)
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(X2.loc[X_train.index], y_train)
    result = permutation_importance(model, X2.loc[X_test.index], y_test, n_repeats=5,
                                    random_state=0)
    values = result.importances_mean
    return [round(float(values[0]), 3), round(float(values[-1]), 3)]

print(copy_effect(2.0))
