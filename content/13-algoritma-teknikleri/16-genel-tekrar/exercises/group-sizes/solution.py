from collections import Counter


def group_sizes(n, pairs):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    counts = Counter(find(i) for i in range(n))
    return sorted(counts.values(), reverse=True)

pairs = [[0, 1], [1, 2], [3, 4], [5, 5]]
print(group_sizes(7, pairs))
print(group_sizes(3, []))
