def first_cycle_edge(n, edges):
    parent = list(range(n))

    def find(x):
        # Climb to the root (shortening the path).
        return x

    # For each edge: are the roots the same?
    return None

print(first_cycle_edge(4, [[0, 1], [1, 2], [2, 0], [2, 3]]))
print(first_cycle_edge(3, [[0, 1], [1, 2]]))
print(first_cycle_edge(5, [[3, 4], [0, 1], [4, 3]]))
