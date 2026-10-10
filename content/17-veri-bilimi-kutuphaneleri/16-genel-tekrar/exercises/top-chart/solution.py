import matplotlib.pyplot as plt
import pandas as pd


def top_chart(channels, sales):
    totals = pd.Series(sales, index=channels).groupby(level=0).sum().sort_values(ascending=False)
    order = totals.index.tolist()
    fig, ax = plt.subplots()
    bars = ax.barh(order[::-1], totals.values[::-1], color="lightgray")
    bars[-1].set_color("tab:blue")
    labels = [t.get_text() for t in ax.bar_label(bars, padding=3)]
    fig.savefig("top.png")
    plt.close(fig)
    return {"order": order, "labels": labels, "highlight": order[0]}

result = top_chart(["web", "store", "phone", "web", "store", "web"], [5, 3, 2, 4, 6, 1])
print(result["order"])
print(result["labels"])
print(result["highlight"])
