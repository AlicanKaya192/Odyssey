import matplotlib.pyplot as plt


def weekly_chart(values):
    fig, ax = plt.subplots()
    weeks = list(range(1, len(values) + 1))
    ax.plot(weeks, values)
    ax.set(title="Weekly sales", xlabel="week", ylabel="sales")
    fig.savefig("weekly.png")
    plt.close(fig)
    return [ax.get_title(), ax.get_xlabel(), ax.get_ylabel(), len(ax.lines)]

print(weekly_chart([3, 5, 4, 7]))
