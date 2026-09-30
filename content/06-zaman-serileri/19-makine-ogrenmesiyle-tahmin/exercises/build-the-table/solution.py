import pandas as pd

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
print(table.shape, table.index[0].date())
print(table.columns.tolist())

row = table.loc["2024-03-10"]
print(int(row["y"]), int(row["lag1"]), int(row["lag7"]), round(float(row["mean7"]), 1))

print(round(float(s.loc["2024-03-03":"2024-03-09"].mean()), 1))
