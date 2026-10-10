import pandas as pd


def to_long(rows, months):
    wide = pd.DataFrame(rows, columns=["city", *months])
    long = wide.melt(id_vars="city", var_name="month", value_name="sales")
    return long.values.tolist()

ROWS = [["Izmir", 80, 95], ["Ankara", 120, 110]]
print(*to_long(ROWS, ["jan", "feb"]), sep="\n")
