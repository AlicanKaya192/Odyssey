from collections import Counter


def group_sizes(n, pairs):
    parent = list(range(n))

    def find(x):
        # Koke cik, yolu kisalt.
        return x

    # Birlestir; sonra kokleri say.
    return []

pairs = [[0, 1], [1, 2], [3, 4], [5, 5]]
print(group_sizes(7, pairs))
print(group_sizes(3, []))
