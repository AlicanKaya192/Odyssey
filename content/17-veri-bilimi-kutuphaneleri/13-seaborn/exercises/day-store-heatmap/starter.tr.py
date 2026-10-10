import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def day_store_table(days, stores, sales, day_order, store_order):
    df = pd.DataFrame({"day": days, "store": stores, "sales": sales})
    return {"shape": [], "first_row": []}

result = day_store_table(["Mon", "Mon", "Sat", "Sat"], ["A", "B", "A", "B"],
                         [100, 80, 140, 120], ["Mon", "Sat"], ["A", "B"])
print(result["shape"])
print(result["first_row"])
