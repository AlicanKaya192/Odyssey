def build_graph(edges):
    graph = {}
    # Yonsuz: iki yone de ekle.
    return graph


def neighbours(edges):
    graph = build_graph(edges)
    return {node: sorted(graph[node]) for node in sorted(graph)}


edges = [["ada", "bora"], ["ada", "cem"], ["bora", "cem"], ["bora", "deniz"],
         ["cem", "deniz"], ["deniz", "ece"], ["ece", "fuat"]]
for node, near in neighbours(edges).items():
    print(node, near)
