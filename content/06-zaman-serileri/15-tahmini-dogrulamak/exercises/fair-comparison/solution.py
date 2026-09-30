import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


def weeks_mean(train, h, k):
    pattern = train.iloc[-7 * k:].to_numpy().reshape(k, 7).mean(axis=0)
    return np.array([pattern[i % 7] for i in range(h)])


def errors(forecast):
    rows = []
    for cut in cuts:
        train = s.loc[:cut]
        test = s.loc[cut + pd.Timedelta(days=1):].iloc[:28]
        rows.append(np.abs(test.to_numpy() - forecast(train, 28)))
    return np.array(rows)


e_naive = errors(snaive)
e_weeks = errors(lambda train, h: weeks_mean(train, h, 4))

mae_naive = e_naive.mean(axis=1)
mae_weeks = e_weeks.mean(axis=1)
print(round(float(mae_naive.mean()), 2), round(float(mae_weeks.mean()), 2))

diff = mae_naive - mae_weeks
print(round(float(diff.mean()), 2), round(float(diff.std(ddof=1)), 2), int((diff < 0).sum()))

print(round(float(mae_naive[11]), 2), round(float(mae_weeks[11]), 2))

for e in (e_naive, e_weeks):
    print([round(float(e[:, i:i + 7].mean()), 1) for i in range(0, 28, 7)])
