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
    while queue:
        node = queue.popleft()
        if node == goal:
            break
        for neighbour in sorted(graph[node]):
            if neighbour not in parent:
                parent[neighbour] = node
                queue.append(neighbour)
    if goal not in parent:
        return None
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


edges = [["ada", "bora"], ["ada", "cem"], ["bora", "cem"], ["bora", "deniz"],
         ["cem", "deniz"], ["deniz", "ece"], ["ece", "fuat"], ["gul", "hakan"]]
print(shortest_path(edges, "ada", "fuat"))
print(shortest_path(edges, "cem", "ece"))
print(shortest_path(edges, "ada", "hakan"))
