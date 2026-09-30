import pandas as pd
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


def fit_and_score(data):
    model = LinearRegression().fit(data.loc[:"2023", columns], data.loc[:"2023", "y"])
    predicted = model.predict(data.loc["2024", columns])
    error = float((data.loc["2024", "y"] - predicted).abs().mean())
    return model, error


good_model, good_error = fit_and_score(table)
print(round(good_error, 2))

leaky = table.copy()
leaky["mean7"] = s.rolling(7).mean().reindex(table.index)
bad_model, bad_error = fit_and_score(leaky)
print(round(bad_error, 2))

print(round(float(table["mean7"].corr(table["y"])), 3), round(float(leaky["mean7"].corr(leaky["y"])), 3))

position = columns.index("mean7")
print(round(float(good_model.coef_[position]), 2), round(float(bad_model.coef_[position]), 2))

print(round(float(leaky.loc["2024-03-10", "mean7"]), 1),
      round(float(s.loc["2024-03-04":"2024-03-10"].mean()), 1))
