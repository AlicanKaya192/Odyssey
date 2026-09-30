import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

error = s - s.shift(7)
past = error.loc["2023"]
future = error.loc["2024"]

low = float(past.quantile(0.10))
high = float(past.quantile(0.90))
print(round(low, 1), round(high, 1))

day = "2024-03-15"
forecast = float(s.shift(7).loc[day])
print(round(forecast), round(forecast + low), round(forecast + high), int(s.loc[day]))


def coverage(level):
    lower = past.quantile((1 - level) / 2)
    upper = past.quantile(1 - (1 - level) / 2)
    inside = (future >= lower) & (future <= upper)
    return round(float(inside.mean()), 3)


print(coverage(0.5), coverage(0.8), coverage(0.95))
