import pandas as pd


def monthly_sum(records):
    long = pd.DataFrame(records, columns=["city", "month", "sales"])
    table = long.pivot_table(index="city", columns="month", values="sales",
                             aggfunc="sum", fill_value=0)
    return table.to_dict(orient="index")

SALES = [["Izmir", "jan", 30], ["Izmir", "jan", 50],
         ["Ankara", "jan", 120], ["Bursa", "feb", 65]]
table = monthly_sum(SALES)
print(table["Izmir"])
print(table["Bursa"])
