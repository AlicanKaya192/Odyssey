def count_groups(n, pairs):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    groups = n
    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            groups -= 1
    return groups

print(count_groups(6, [[0, 1], [2, 3], [1, 2], [4, 5]]))
print(count_groups(4, []))
print(count_groups(5, [[0, 1], [1, 0], [3, 4]]))
