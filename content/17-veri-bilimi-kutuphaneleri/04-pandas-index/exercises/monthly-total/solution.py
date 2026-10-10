import pandas as pd


def monthly_total(jan, feb):
    total = pd.Series(jan).add(pd.Series(feb), fill_value=0)
    return {city: int(value) for city, value in total.items()}

result = monthly_total({"Ankara": 120, "Izmir": 80, "Bursa": 50},
                       {"Izmir": 90, "Ankara": 100, "Konya": 40})
for city, value in result.items():
    print(city, value)
