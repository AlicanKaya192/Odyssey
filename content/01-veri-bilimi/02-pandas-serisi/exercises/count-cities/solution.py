import pandas as pd

cities = pd.Series(["Ankara", "Izmir", "Ankara", "Bursa", "Izmir", "Ankara"])

counts = cities.value_counts()

print(counts)
print(cities.nunique())
print(counts.idxmax())
