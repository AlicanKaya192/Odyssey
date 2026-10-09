from collections import Counter


def group_sizes(n, pairs):
    parent = list(range(n))

    def find(x):
        # Climb to the root, shorten the path.
        return x

    # Merge; then count the roots.
    return []

pairs = [[0, 1], [1, 2], [3, 4], [5, 5]]
print(group_sizes(7, pairs))
print(group_sizes(3, []))
