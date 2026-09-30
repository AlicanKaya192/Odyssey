import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


errors = []
for cut in cuts:
    train = s.loc[:cut]
    test = s.loc[cut + pd.Timedelta(days=1):].iloc[:28]
    errors.append(test.to_numpy() - snaive(train, 28))
errors = np.array(errors)

build, check = errors[:9], errors[9:]

coverages = []
inside_all = []
for week in range(4):
    columns = slice(week * 7, week * 7 + 7)
    low, high = np.quantile(build[:, columns], [0.10, 0.90])
    print(week + 1, round(float(low), 1), round(float(high), 1))
    inside = (check[:, columns] >= low) & (check[:, columns] <= high)
    coverages.append(round(float(inside.mean()), 2))
    inside_all.append(inside)

print(coverages)
print(round(float(np.concatenate(inside_all, axis=1).mean()), 3))
