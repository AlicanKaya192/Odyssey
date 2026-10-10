import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def day_store_table(days, stores, sales, day_order, store_order):
    df = pd.DataFrame({"day": days, "store": stores, "sales": sales})
    table = df.pivot_table(index="day", columns="store", values="sales", aggfunc="mean")
    table = table.loc[day_order, store_order]
    fig, ax = plt.subplots()
    sns.heatmap(table, annot=True, fmt=".0f", ax=ax)
    fig.savefig("heat.png")
    texts = [t.get_text() for t in ax.texts]
    plt.close(fig)
    return {"shape": list(table.shape), "first_row": texts[:len(store_order)]}

result = day_store_table(["Mon", "Mon", "Sat", "Sat"], ["A", "B", "A", "B"],
                         [100, 80, 140, 120], ["Mon", "Sat"], ["A", "B"])
print(result["shape"])
print(result["first_row"])
