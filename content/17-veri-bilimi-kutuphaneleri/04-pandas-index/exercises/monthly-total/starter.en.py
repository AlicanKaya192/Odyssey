import pandas as pd


def monthly_total(jan, feb):
    a, b = pd.Series(jan), pd.Series(feb)
    total = a.values + b.values
    return dict(zip(a.index, total.tolist()))

result = monthly_total({"Ankara": 120, "Izmir": 80, "Bursa": 50},
                       {"Izmir": 90, "Ankara": 100, "Konya": 40})
for city, value in result.items():
    print(city, value)
