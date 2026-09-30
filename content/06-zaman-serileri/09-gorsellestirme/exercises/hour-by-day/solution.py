import matplotlib.pyplot as plt
import pandas as pd

load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)["load_mw"]

grid = load.groupby([load.index.dayofweek, load.index.hour]).mean().unstack()
print(grid.shape)

fig, ax = plt.subplots(figsize=(10, 3.5))
image = ax.imshow(grid.values, aspect="auto")
fig.colorbar(image)
fig.savefig("chart.png")

cells = grid.stack()
day, hour = cells.idxmax()
print(int(day), int(hour), round(float(cells.max())))
day, hour = cells.idxmin()
print(int(day), int(hour), round(float(cells.min())))

print(round(float(grid.loc[0, 13])), round(float(grid.loc[6, 13])))
