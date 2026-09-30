import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

error = s - s.shift(7)
past = error.loc["2023"]
base = s.shift(7).loc["2024"]
actual = s.loc["2024"]


def cost(order):
    short = (actual - order).clip(lower=0)
    over = (order - actual).clip(lower=0)
    total = 4 * short.sum() + over.sum()
    return int((short > 0).sum()), int(short.sum()), int(over.sum()), int(total)


totals = {}
for q in (0.5, 0.8, 0.9, 0.95):
    result = cost(base + past.quantile(q))
    totals[q] = result[3]
    print(q, result)

print(4 / (4 + 1))

best = min(totals, key=totals.get)
print(best, round((1 - totals[best] / totals[0.5]) * 100))
