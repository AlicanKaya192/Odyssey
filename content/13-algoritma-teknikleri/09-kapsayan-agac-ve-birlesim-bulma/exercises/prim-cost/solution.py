import heapq


def prim_cost(graph, start):
    seen = set()
    heap = [(0, start)]
    total = 0
    while heap and len(seen) < len(graph):
        w, node = heapq.heappop(heap)
        if node in seen:
            continue
        seen.add(node)
        total += w
        for nxt, w2 in graph[node]:
            if nxt not in seen:
                heapq.heappush(heap, (w2, nxt))
    return total

graph = {
    "A": [("B", 4), ("C", 3)],
    "B": [("A", 4), ("C", 2), ("D", 5)],
    "C": [("A", 3), ("B", 2), ("D", 7)],
    "D": [("B", 5), ("C", 7)],
}
print(prim_cost(graph, "A"))
print(prim_cost(graph, "D"))
