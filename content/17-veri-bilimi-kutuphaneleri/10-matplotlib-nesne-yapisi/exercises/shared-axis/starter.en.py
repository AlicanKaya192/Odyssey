import matplotlib.pyplot as plt


def compare(a, b):
    fig, (left, right) = plt.subplots(1, 2)
    left.plot(a)
    right.plot(b)
    fig.savefig("compare.png")
    same = left.get_ylim() == right.get_ylim()
    low, high = left.get_ylim()
    plt.close(fig)
    return [same, [round(low, 1), round(high, 1)]]

print(compare([10, 20, 15], [100, 120, 90]))
