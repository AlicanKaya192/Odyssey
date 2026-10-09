import heapq
import math


def shortest_distances(graph, start):
    dist = {start: 0}
    heap, done = [(0, start)], set()
    # Settle the closest until the heap is empty.
    return dict(sorted(dist.items()))


graph = {"A": {"B": 4, "C": 2},
         "B": {"A": 4, "C": 1, "D": 5},
         "C": {"A": 2, "B": 1, "D": 8, "E": 10},
         "D": {"B": 5, "C": 8, "E": 2, "F": 6},
         "E": {"C": 10, "D": 2, "F": 3},
         "F": {"D": 6, "E": 3}}
for start in ["A", "F"]:
    print(start, list(shortest_distances(graph, start).values()))
