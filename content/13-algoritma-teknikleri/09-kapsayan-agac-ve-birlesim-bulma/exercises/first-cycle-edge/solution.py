def first_cycle_edge(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for edge in edges:
        ra, rb = find(edge[0]), find(edge[1])
        if ra == rb:
            return edge
        parent[ra] = rb
    return None

print(first_cycle_edge(4, [[0, 1], [1, 2], [2, 0], [2, 3]]))
print(first_cycle_edge(3, [[0, 1], [1, 2]]))
print(first_cycle_edge(5, [[3, 4], [0, 1], [4, 3]]))
