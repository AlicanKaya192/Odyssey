import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def weeks_mean(train, h, k):
    pattern = train.iloc[-7 * k:].to_numpy().reshape(k, 7).mean(axis=0)
    return np.array([pattern[i % 7] for i in range(h)])


def score(k, some_cuts):
    values = []
    for cut in some_cuts:
        train = s.loc[:cut]
        test = s.loc[cut + pd.Timedelta(days=1):].iloc[:28]
        values.append(np.abs(test.to_numpy() - weeks_mean(train, 28, k)).mean())
    return float(np.mean(values))


validation = cuts[:10]
test = cuts[10:]

val_scores = {k: score(k, validation) for k in range(1, 9)}
print([round(v, 2) for v in val_scores.values()])

best = min(val_scores, key=val_scores.get)
honest = score(best, test)
print(best, round(val_scores[best], 2), round(honest, 2))

test_scores = {k: score(k, test) for k in range(1, 9)}
cheat = min(test_scores, key=test_scores.get)
print(cheat, round(test_scores[cheat], 2))

print(round(honest - test_scores[cheat], 2))
