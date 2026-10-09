from collections import deque


def count_components(n, edges):
    graph = {i: [] for i in range(n)}
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    seen = set()
    count = 0
    # A new walk from every node not yet visited.
    return count


print(count_components(5, [[0, 1], [1, 2], [3, 4]]))
print(count_components(4, []))
chain = [[i, i + 1] for i in range(199_999)]
print(count_components(200_000, chain))
