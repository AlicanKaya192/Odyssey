import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]

window = visits.rolling(7)
print(round(float(window.mean().loc["2024-03-14"])), window.median().loc["2024-03-14"])

base = visits.shift(1).rolling(28)
z = (visits - base.mean()) / base.std()
print(round(float(z.loc["2024-03-14"]), 1))

unusual = z[z.abs() > 3]
print(unusual.index.strftime("%m-%d").tolist())
print(unusual.round(1).tolist())
