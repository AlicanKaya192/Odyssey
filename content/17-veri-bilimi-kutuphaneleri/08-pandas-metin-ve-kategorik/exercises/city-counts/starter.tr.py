import pandas as pd


def city_counts(names):
    s = pd.Series(names)
    return s.value_counts().sort_index().to_dict()

print(city_counts(["  Izmir", "izmir ", "IZMIR", "Ankara", "ankara"]))
