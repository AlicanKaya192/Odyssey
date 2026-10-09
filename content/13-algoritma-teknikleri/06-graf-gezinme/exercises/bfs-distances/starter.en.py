from collections import deque


def build_graph(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def distances(edges, start):
    graph = build_graph(edges)
    distance = {start: 0}
    queue = deque([start])
    # Until the queue is empty.
    return dict(sorted(distance.items()))


edges = [["ada", "bora"], ["ada", "cem"], ["bora", "cem"], ["bora", "deniz"],
         ["cem", "deniz"], ["deniz", "ece"], ["ece", "fuat"], ["gul", "hakan"]]
for node, steps in distances(edges, "ada").items():
    print(node, steps)
print(distances(edges, "gul"))
