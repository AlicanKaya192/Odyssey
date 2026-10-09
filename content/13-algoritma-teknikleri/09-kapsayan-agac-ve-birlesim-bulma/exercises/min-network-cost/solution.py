def min_network_cost(n, roads):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, taken = 0, 0
    for a, b, cost in sorted(roads, key=lambda r: r[2]):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            total += cost
            taken += 1
    return total if taken == n - 1 else None

roads = [[0, 1, 4], [0, 2, 3], [1, 2, 2], [1, 3, 5],
         [2, 3, 7], [2, 4, 6], [3, 4, 1]]
print(min_network_cost(5, roads))
print(min_network_cost(4, [[0, 1, 1], [2, 3, 1]]))
