import matplotlib.pyplot as plt
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

profile = s.groupby(s.index.dayofweek).mean()

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(labels, profile.values)
fig.savefig("chart.png")

print(len(ax.patches))
print(float(ax.get_ylim()[0]))

print(labels[profile.idxmax()], round(float(profile.max()), 1))
print(labels[profile.idxmin()], round(float(profile.min()), 1))

weekend = profile.loc[[5, 6]].mean()
weekday = profile.loc[[0, 1, 2, 3, 4]].mean()
print(round(float(weekend / weekday), 2))
