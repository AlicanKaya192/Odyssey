import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def day_counts(days, order):
    df = pd.DataFrame({"day": days})
    fig, ax = plt.subplots()
    sns.countplot(df, x="day", ax=ax)
    heights = [int(p.get_height()) for p in ax.patches]
    plt.close(fig)
    return heights

DAYS = ["Tue", "Mon", "Sun", "Mon", "Sat", "Tue", "Mon"]
print(day_counts(DAYS, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))
