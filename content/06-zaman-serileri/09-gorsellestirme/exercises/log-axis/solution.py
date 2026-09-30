import matplotlib.pyplot as plt
import pandas as pd

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)["passengers"]

by_year = p.groupby(p.index.year).agg(["min", "max"])
first = by_year.loc[2013]
last = by_year.loc[2024]

print(int(first["max"] - first["min"]), int(last["max"] - last["min"]))
print(round(float(first["max"] / first["min"]), 2), round(float(last["max"] / last["min"]), 2))

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].plot(p.index, p.values)
axes[1].plot(p.index, p.values)
axes[1].set_yscale("log")
fig.savefig("chart.png")

print([ax.get_yscale() for ax in axes])
