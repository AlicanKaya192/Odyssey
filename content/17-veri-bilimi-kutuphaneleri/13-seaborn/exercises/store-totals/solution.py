import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def store_totals(stores, sales, order):
    df = pd.DataFrame({"store": stores, "sales": sales})
    fig, ax = plt.subplots()
    sns.barplot(df, x="store", y="sales", order=order, estimator="sum", errorbar=None, ax=ax)
    fig.savefig("totals.png")
    heights = [round(float(p.get_height()), 1) for p in ax.patches]
    plt.close(fig)
    return heights

STORES = ["Izmir", "Ankara", "Izmir", "Bursa", "Ankara", "Izmir"]
SALES = [100, 80, 120, 90, 70, 110]
print(store_totals(STORES, SALES, ["Izmir", "Ankara", "Bursa"]))
