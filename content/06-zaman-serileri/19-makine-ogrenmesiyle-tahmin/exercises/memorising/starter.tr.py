import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def features(y):
    X = pd.DataFrame(index=y.index)
    for k in (1, 2, 7, 14):
        X[f"lag{k}"] = y.shift(k)
    X["mean7"] = y.shift(1).rolling(7).mean()
    X["mean28"] = y.shift(1).rolling(28).mean()
    X["dow"] = y.index.dayofweek
    X["month"] = y.index.month
    return X


table = features(s).join(s.rename("y")).dropna()
columns = [c for c in table.columns if c != "y"]
train, test = table.loc[:"2023"], table.loc["2024"]

# Uc model: linear, forest, boosting.


# Her biri: ad, egitim MAE, test MAE, oran.


# Mevsimsel naifi gecen modeller.
