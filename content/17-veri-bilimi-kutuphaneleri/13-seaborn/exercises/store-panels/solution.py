import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def store_panels(hours, sales, stores, order):
    df = pd.DataFrame({"hour": hours, "sales": sales, "store": stores})
    grid = sns.relplot(df, x="hour", y="sales", col="store", col_order=order, height=2)
    grid.set_titles("{col_name}")
    grid.figure.savefig("panels.png")
    result = {"shape": list(grid.axes.shape), "titles": [ax.get_title() for ax in grid.axes.flat]}
    plt.close(grid.figure)
    return result

result = store_panels([9, 10, 11, 9, 10, 11], [100, 120, 110, 80, 90, 95],
                      ["Izmir", "Izmir", "Izmir", "Bursa", "Bursa", "Bursa"],
                      ["Izmir", "Bursa"])
print(result["shape"])
print(result["titles"])
