from collections import deque


def build_graph(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def shortest_path(edges, start, goal):
    graph = build_graph(edges)
    parent = {start: None}
    queue = deque([start])
    # 1. BFS ile ebeveynleri yaz.  2. Hedeften geriye yuru.
    return None


edges = [["ada", "bora"], ["ada", "cem"], ["bora", "cem"], ["bora", "deniz"],
         ["cem", "deniz"], ["deniz", "ece"], ["ece", "fuat"], ["gul", "hakan"]]
print(shortest_path(edges, "ada", "fuat"))
print(shortest_path(edges, "cem", "ece"))
print(shortest_path(edges, "ada", "hakan"))
