import pandas as pd

data = pd.DataFrame({
    "team": ["A", "A", "A", "A", "B", "B", "B", "B", "C", "C"],
    "minutes": [31, 28, 35, 30, 27, 33, 29, 240, 30, 32],
})

minutes = data["minutes"]
q1 = minutes.quantile(0.25)
q3 = minutes.quantile(0.75)
iqr = q3 - q1
low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

print(minutes[(minutes < low) | (minutes > high)].tolist())
print(round(minutes.mean(), 2), minutes.median())
print(data.groupby("team")["minutes"].agg(["count", "mean"]).round(1))
