import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
change = k.diff().dropna()

print(round(float(k.corr(k.shift(1))), 4), round(float(change.corr(change.shift(1))), 3))

table = pd.DataFrame({
    "actual": k,
    "naive": k.shift(1),
    "mean20": k.shift(1).rolling(20).mean(),
}).dropna()
naive_error = (table["actual"] - table["naive"]).abs().mean()
mean_error = (table["actual"] - table["mean20"]).abs().mean()
print(round(float(naive_error), 2), round(float(mean_error), 2))

up = change > 0
after_up = up[up.shift(1, fill_value=False)]
print(round(float(up.mean()), 3), round(float(after_up.mean()), 3))
