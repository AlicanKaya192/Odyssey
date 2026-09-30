import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

train, test = s.iloc[:-28], s.iloc[-28:]
h = len(test)
future = test.index

mean_fc = pd.Series(train.mean(), index=future)
naive_fc = pd.Series(train.iloc[-1], index=future)

last_week = train.iloc[-7:].to_numpy()
snaive_fc = pd.Series([last_week[i % 7] for i in range(h)], index=future)

slope = (train.iloc[-1] - train.iloc[0]) / (len(train) - 1)
drift_fc = pd.Series(train.iloc[-1] + slope * np.arange(1, h + 1), index=future)

forecasts = {"mean": mean_fc, "naive": naive_fc, "snaive": snaive_fc, "drift": drift_fc}

for name, fc in forecasts.items():
    print(name, round(float((test - fc).abs().mean()), 2))

day = future[0]
print(int(test.loc[day]), *[round(float(fc.loc[day])) for fc in forecasts.values()])

recent = s.iloc[-56:]
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(recent.index, recent.values, color="gray", label="actual")
for name, fc in forecasts.items():
    ax.plot(fc.index, fc.values, label=name)
ax.legend()
fig.savefig("chart.png")
