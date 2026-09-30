import pandas as pd

p = pd.read_csv("pump_pressure.csv", index_col="timestamp", parse_dates=True)
p = p["pressure"]
events = pd.read_csv("pump_events.csv", parse_dates=["timestamp"])["timestamp"]
calm = p.loc[:"2024-10-06"]

# Butun seriye z-skoru: 3'u gecen saatler ve kaci events icinde.


# 5 Eylul 03:00: deger, z-skoru, o saatin ortancasi.


# Saat profili, kalinti, dayanikli puan.


# Puani 3'u gecen saat sayisi ve kaci events icinde.


# Isaretlenen ama events icinde olmayan saatlerin gunleri.
