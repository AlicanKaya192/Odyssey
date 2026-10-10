import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def raw_points(hours, sales):
    df = pd.DataFrame({"hour": hours, "sales": sales})
    fig, ax = plt.subplots()
    sns.lineplot(df, x="hour", y="sales", estimator=None, ax=ax)
    count = len(ax.lines[0].get_xdata())
    plt.close(fig)
    return count

print(raw_points([9, 9, 10, 10, 11], [100, 120, 110, 90, 130]))
