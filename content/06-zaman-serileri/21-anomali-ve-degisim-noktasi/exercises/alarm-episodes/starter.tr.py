import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
past = pd.concat([v.shift(7 * k) for k in (1, 2, 3, 4)], axis=1)
deviation = v / past.median(axis=1) - 1
alarm = deviation.abs() > 0.25

# Alarm gunleri.


# Gunleri olaylara ayir (aradaki bosluk en cok 3 gun).


# Her olay: ilk gun, son gun, alarm sayisi, yon, tur.
