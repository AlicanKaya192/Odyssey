import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score

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

model = HistGradientBoostingRegressor(random_state=0)

for cv in (KFold(5, shuffle=True, random_state=0), TimeSeriesSplit(5)):
    scores = -cross_val_score(model, table[columns], table["y"], cv=cv,
                              scoring="neg_mean_absolute_error")
    print([round(float(v), 1) for v in scores], round(float(scores.mean()), 2))

splits = list(TimeSeriesSplit(5).split(table))
for train_idx, test_idx in (splits[0], splits[-1]):
    print(len(train_idx), len(test_idx))
