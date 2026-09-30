import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


rows = []
for i in range(13):
    cut = pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i)
    train = s.loc[:cut]
    test = s.loc[cut + pd.Timedelta(days=1):].iloc[:28]
    error = test.to_numpy() - snaive(train, 28)
    rows.append({"cut": cut, "mae": float(np.abs(error).mean()), "bias": float(error.mean())})

table = pd.DataFrame(rows).set_index("cut")
m = table["mae"]
print(len(m), round(float(m.mean()), 2), round(float(m.std(ddof=1)), 2),
      round(float(m.min()), 2), round(float(m.max()), 2))

worst = m.sort_values(ascending=False).head(2).index.sort_values()
print(worst.strftime("%Y-%m-%d").tolist())

print(round(float(m.loc["2024-11-05"]), 2), round(float(table["bias"].mean()), 2))

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(m.index.strftime("%m-%d"), m.values)
ax.axhline(m.mean(), linestyle="--", color="gray")
ax.tick_params(axis="x", rotation=45)
fig.tight_layout()
fig.savefig("chart.png")
