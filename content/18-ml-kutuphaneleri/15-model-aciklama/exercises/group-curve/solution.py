import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

rng = np.random.default_rng(4)
df = pd.DataFrame({"age": rng.uniform(0, 50, 1500),
                   "renovated": rng.integers(0, 2, 1500).astype(float)})
df["price"] = 200 - 3 * df["age"] * (1 - df["renovated"]) + rng.normal(0, 10, 1500)
X, y = df[["age", "renovated"]], df["price"]
rf = RandomForestRegressor(n_estimators=100, random_state=0).fit(X, y)
from sklearn.inspection import partial_dependence


def group_curve(flag):
    result = partial_dependence(rf, X, ["age"], grid_resolution=5, kind="both")
    rows = result["individual"][0][(X["renovated"] == flag).to_numpy()]
    return rows.mean(axis=0).round().astype(int).tolist()

print(group_curve(0.0))
print(group_curve(1.0))
