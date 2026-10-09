def count_groups(n, pairs):
    parent = list(range(n))

    def find(x):
        # Climb to the root (shortening the path).
        return x

    groups = n
    # Merge the roots for each pair.
    return groups

print(count_groups(6, [[0, 1], [2, 3], [1, 2], [4, 5]]))
print(count_groups(4, []))
print(count_groups(5, [[0, 1], [1, 0], [3, 4]]))
