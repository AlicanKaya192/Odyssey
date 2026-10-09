import heapq


def cheapest(n, roads, start, goal):
    out = [[] for _ in range(n)]
    for a, b, cost in roads:
        out[a].append((b, cost))
    dist = {start: 0}
    heap = [(0, start)]
    # Heap bosalana kadar en ucuzu al ve gevset.
    return -1

roads = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1], [2, 3, 5]]
print(cheapest(4, roads, 0, 3))
print(cheapest(3, [[0, 1, 2]], 0, 2))
