import pandas as pd

p = pd.read_csv("pump_pressure.csv", index_col="timestamp", parse_dates=True)
p = p["pressure"]
events = pd.read_csv("pump_events.csv", parse_dates=["timestamp"])["timestamp"]
calm = p.loc[:"2024-10-06"]

profile = calm.groupby(calm.index.hour).median()
resid = calm - profile.reindex(calm.index.hour).to_numpy()
mad = (resid - resid.median()).abs().median()
score = 0.6745 * (resid - resid.median()) / mad


def evaluate(threshold, skip):
    # Alarm sayisi, dogru sayisi, kesinlik, duyarlilik.
    pass


# Esik 3, hicbir sey atlamadan.


# Takili sensor saatleri ayri: esik 2, 2.5, 3, 4, 6.


# Esik 4 iken kacan olaylar.
