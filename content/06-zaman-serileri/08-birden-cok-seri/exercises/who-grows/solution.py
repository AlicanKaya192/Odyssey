import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales")

monthly = wide.resample("ME").mean()
index = monthly / monthly.loc["2024-05-31"] * 100
print(index.loc["2024-12-31"].round(1).to_dict())

quarterly = wide.resample("QE").sum()
share = quarterly.div(quarterly.sum(axis=1), axis=0) * 100
print(share.iloc[-1].round(1).to_dict())
print(round(float(share["A"].iloc[-1] - share["A"].iloc[0]), 1))
