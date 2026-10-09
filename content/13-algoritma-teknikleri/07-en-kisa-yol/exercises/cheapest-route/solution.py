import heapq
import math


def cheapest_route(graph, start, goal):
    dist, parent = {start: 0}, {start: None}
    heap, done = [(0, start)], set()
    while heap:
        d, node = heapq.heappop(heap)
        if node in done:
            continue
        done.add(node)
        for nxt, w in graph[node].items():
            if d + w < dist.get(nxt, math.inf):
                dist[nxt] = d + w
                parent[nxt] = node
                heapq.heappush(heap, (d + w, nxt))
    if goal not in dist:
        return None
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return [dist[goal], path[::-1]]


graph = {"A": {"B": 4, "C": 2},
         "B": {"A": 4, "C": 1, "D": 5},
         "C": {"A": 2, "B": 1, "D": 8, "E": 10},
         "D": {"B": 5, "C": 8, "E": 2, "F": 6},
         "E": {"C": 10, "D": 2, "F": 3},
         "F": {"D": 6, "E": 3}}
print(cheapest_route(graph, "A", "F"))
print(cheapest_route(graph, "F", "B"))
