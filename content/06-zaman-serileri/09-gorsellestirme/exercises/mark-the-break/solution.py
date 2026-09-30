import matplotlib.pyplot as plt
import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]

base = visits.shift(1).rolling(28)
z = (visits - base.mean()) / base.std()
unusual = z[z.abs() > 3]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(visits.index, visits.values, linewidth=0.9)
for day in unusual.index:
    ax.axvline(day, linestyle="--", color="gray")

change = pd.Timestamp("2024-09-02")
ax.axvspan(change, visits.index[-1], alpha=0.15)
fig.savefig("chart.png")

print(unusual.index.strftime("%m-%d").tolist())
print(len(ax.lines))

before = visits.loc[:"2024-09-01"].median()
after = visits.loc["2024-09-02":].median()
print(round(float(before)), round(float(after)))
