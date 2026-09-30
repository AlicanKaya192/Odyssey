import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

forecasts = {
    "mean so far": s.shift(1).expanding().mean(),
    "mean of 7": s.shift(1).rolling(7).mean(),
    "naive": s.shift(1),
    "seasonal naive": s.shift(7),
    "mean of 4 weeks": (s.shift(7) + s.shift(14) + s.shift(21) + s.shift(28)) / 4,
}

actual = s.loc["2024"]
scores = {}
for name, fc in forecasts.items():
    error = actual - fc.loc["2024"]
    scores[name] = float(error.abs().mean())
    print(name, round(scores[name], 2), round(float(error.mean()), 2))

best = min(scores.values())
print(round(1 - best / scores["naive"], 2))

leaky = (s + s.shift(7) + s.shift(14) + s.shift(21)) / 4
print(round(float((actual - leaky.loc["2024"]).abs().mean()), 2))
