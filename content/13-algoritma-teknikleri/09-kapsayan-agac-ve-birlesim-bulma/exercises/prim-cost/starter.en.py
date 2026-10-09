import heapq


def prim_cost(graph, start):
    seen = set()
    heap = [(0, start)]
    total = 0
    # Take the cheapest edge from the heap; add it if the node is new.
    return total

graph = {
    "A": [("B", 4), ("C", 3)],
    "B": [("A", 4), ("C", 2), ("D", 5)],
    "C": [("A", 3), ("B", 2), ("D", 7)],
    "D": [("B", 5), ("C", 7)],
}
print(prim_cost(graph, "A"))
print(prim_cost(graph, "D"))
